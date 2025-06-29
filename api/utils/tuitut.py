import time
from collections import defaultdict
from web3 import Web3
from pprint import pprint

# === CONFIGURATION ===
ETH_RPC_URL = "https://rpc.flashbots.net"

# --- EXAMPLE SHITCOIN (MAGA VP) ---
# Found via DexScreener, created recently.
TOKEN_ADDRESS = "0x767A98A4F0Ac1D1c09E93e97C752f357B8F86976"

# --- IMPORTANT: We now look back a fixed number of blocks ---
# Instead of starting at block 0, we'll look at the last N blocks.
# 100,000 blocks is ~1.5 days on Ethereum. Perfect for new tokens.
# You can increase this if the token is a bit older.
BLOCK_LOOKBACK_WINDOW = 100_000

# The number of blocks to query in each RPC call. 5,000 is a safe number.
BLOCK_CHUNK_SIZE = 5_000
TOP_N = 10

# === Setup ===
w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
# This hash is the same for ALL standard ERC-20 Transfer events. It does not change.
TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"


def analyze_token_holders(token_address: str, from_block: int, to_block: int, top_n: int = 10):
    address = Web3.to_checksum_address(token_address)

    all_logs = []
    print(f"Starting log fetch from block {from_block} to {to_block}...")
    print(f"Total blocks to scan: {to_block - from_block}")

    # Process logs in chunks to avoid overwhelming the RPC node
    for start in range(from_block, to_block + 1, BLOCK_CHUNK_SIZE):
        end = min(start + BLOCK_CHUNK_SIZE - 1, to_block)
        payload = {
            "fromBlock": hex(start),
            "toBlock": hex(end),
            "address": address,
            "topics": [TRANSFER_TOPIC]
        }

        print(f"  Querying chunk: blocks {start} to {end}...")
        try:
            logs = w3.eth.get_logs(payload)
            if logs:
                all_logs.extend(logs)
                print(f"    -> Found {len(logs)} transfer events in this chunk.")
            # Be kind to the RPC provider
            time.sleep(0.1)
        except Exception as e:
            error_message = e.args[0] if e.args and isinstance(e.args[0], dict) else str(e)
            print(f"    ! Failed to fetch logs for chunk {start}-{end}: {error_message}")
            continue

    print(f"\nFetched a total of {len(all_logs)} Transfer events.")

    if not all_logs:
        print("No transfer events found in the specified block range.")
        return {
            "top_holders": [],
            "centralization_score": 0,
            "anomalies": ["no_transfers_found"],
            "total_holders": 0,
            "total_supply_calculated": 0
        }

    balances = defaultdict(int)

    for log in all_logs:
        try:
            from_address = Web3.to_checksum_address("0x" + log['topics'][1].hex()[-40:])
            to_address = Web3.to_checksum_address("0x" + log['topics'][2].hex()[-40:])
            amount = int(log['data'].hex(), 16)

            balances[from_address] -= amount
            balances[to_address] += amount
        except (IndexError, ValueError) as e:
            print(f"Skipping a malformed log: {log} | Error: {e}")
            continue

    filtered_balances = {k: v for k, v in balances.items() if v > 0}
    sorted_balances = sorted(filtered_balances.items(), key=lambda item: item[1], reverse=True)
    top_holders = sorted_balances[:top_n]

    total_supply = sum(filtered_balances.values())
    if total_supply == 0:
        top_percent = 0
    else:
        top_percent = sum(b for _, b in top_holders) / total_supply * 100

    anomalies = []
    if top_percent > 80:
        anomalies.append("highly_centralized")
    if len(filtered_balances) <= 50:  # New tokens have few holders
        anomalies.append("low_holder_count")
    if top_holders and top_holders[0][1] / total_supply > 0.5:
        anomalies.append("majority_owned_by_one_wallet")

    return {
        "top_holders": [{"address": addr, "balance": bal} for addr, bal in top_holders],
        "centralization_score": round(top_percent, 2),
        "anomalies": anomalies,
        "total_holders": len(filtered_balances),
        "total_supply_calculated": total_supply
    }


if __name__ == "__main__":
    # --- DYNAMIC BLOCK CALCULATION ---
    latest_block = w3.eth.block_number
    from_block = latest_block - BLOCK_LOOKBACK_WINDOW

    print("=" * 50)
    print(f"Analyzing token: {TOKEN_ADDRESS}")
    print(f"Current latest block: {latest_block}")
    print(f"Analyzing from block: {from_block} (looking back {BLOCK_LOOKBACK_WINDOW} blocks)")
    print("=" * 50)

    result = analyze_token_holders(
        token_address=TOKEN_ADDRESS,
        from_block=from_block,
        to_block=latest_block,
        top_n=TOP_N
    )
    pprint(result)