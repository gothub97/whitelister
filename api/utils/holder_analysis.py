from web3 import Web3
from decouple import config
from collections import defaultdict
import time

from api.models import Holder, HolderAddress, HolderTokenLink, TokenComplianceProfile
from .funny_name import generate_random_holder_name

w3 = Web3(Web3.HTTPProvider(config("ETH_RPC_URL")))
TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

BLOCK_LOOKBACK_WINDOW = 100_000
BLOCK_CHUNK_SIZE = 5_000

def _normalize_block(block):
    if isinstance(block, int):
        return hex(block)
    if isinstance(block, str) and block.isdigit():
        return hex(int(block))
    if block in ["latest", "earliest", "pending"]:
        return block
    if isinstance(block, str) and block.startswith("0x"):
        return block
    raise ValueError(f"Invalid block format: {block}")

def save_holders_to_db(token: TokenComplianceProfile, holder_data: list):
    for entry in holder_data:
        address = entry["address"]
        balance = int(entry["balance"])

        holder_address = HolderAddress.objects.filter(address=address).first()
        if not holder_address:
            holder = Holder.objects.create(name=generate_random_holder_name())
            holder_address = HolderAddress.objects.create(holder=holder, address=address)

        HolderTokenLink.objects.get_or_create(
            holder_address=holder_address,
            token=token,
            defaults={"balance": balance}
        )

def analyze_token_holders(token_address: str, from_block=None, to_block=None, top_n=10):
    address = Web3.to_checksum_address(token_address)

    if from_block is None or to_block is None:
        latest_block = w3.eth.block_number
        to_block = latest_block if to_block is None else to_block
        from_block = latest_block - BLOCK_LOOKBACK_WINDOW if from_block is None else from_block

    from_block = int(from_block)
    to_block = int(to_block)

    all_logs = []

    for start in range(from_block, to_block + 1, BLOCK_CHUNK_SIZE):
        end = min(start + BLOCK_CHUNK_SIZE - 1, to_block)
        payload = {
            "fromBlock": hex(start),
            "toBlock": hex(end),
            "address": address,
            "topics": [TRANSFER_TOPIC],
        }

        try:
            logs = w3.eth.get_logs(payload)
            all_logs.extend(logs)
            time.sleep(0.1)
        except Exception as e:
            continue

    balances = defaultdict(int)
    for log in all_logs:
        try:
            topics = log.get("topics", [])
            if len(topics) < 3:
                continue
            sender = Web3.to_checksum_address("0x" + topics[1].hex()[-40:])
            recipient = Web3.to_checksum_address("0x" + topics[2].hex()[-40:])
            amount = int(log["data"].hex(), 16)
            balances[sender] -= amount
            balances[recipient] += amount
        except Exception:
            continue

    filtered = {k: v for k, v in balances.items() if v > 0}
    sorted_balances = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
    top_holders = sorted_balances[:top_n]

    total_supply = sum(filtered.values()) or 1
    top_percent = sum(b for _, b in top_holders) / total_supply * 100

    anomalies = []
    if top_percent > 80:
        anomalies.append("whale_owned")
    if len(filtered) <= 50:
        anomalies.append("low_distribution")
    if top_holders and top_holders[0][1] / total_supply > 0.5:
        anomalies.append("majority_owned_by_one_wallet")

    result = {
        "top_holders": [{"address": addr, "balance": bal} for addr, bal in top_holders],
        "centralization_score": round(top_percent, 2),
        "anomalies": anomalies,
        "total_holders": len(filtered),
        "total_supply_calculated": total_supply,
    }

    # Persist holder data to DB
    token_obj = TokenComplianceProfile.objects.filter(token_address=token_address).first()
    if token_obj:
        save_holders_to_db(token=token_obj, holder_data=result["top_holders"])

    return result