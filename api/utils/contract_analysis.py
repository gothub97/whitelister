import hashlib
import math
from web3 import Web3
from evmdasm import EvmBytecode
from decouple import config

# Setup Web3
w3 = Web3(Web3.HTTPProvider(config("ETH_RPC_URL")))

# Entropy calculation
def calculate_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    entropy = 0
    length = len(data)
    freq = {}
    for b in data:
        freq[b] = freq.get(b, 0) + 1
    for b in freq.values():
        p = b / length
        entropy -= p * math.log2(p)
    return round(entropy, 2)

# Static signature matching
def extract_selectors(bytecode_hex: str) -> list:
    known_selectors = {
        "a9059cbb": "transfer(address,uint256)",
        "095ea7b3": "approve(address,uint256)",
        "23b872dd": "transferFrom(address,address,uint256)",
        "40c10f19": "mint(address,uint256)",
        "f2fde38b": "owner()",
        "8da5cb5b": "renounceOwnership()",
        "a457c2d7": "setBot(address)",
        "dd62ed3e": "allowance(address,address)"
    }
    return [fn for sig, fn in known_selectors.items() if sig in bytecode_hex]

# Main analysis logic
def run_contract_analysis(address: str) -> dict:
    address = Web3.to_checksum_address(address)
    bytecode = w3.eth.get_code(address)

    if not bytecode or bytecode == b'':
        raise Exception("Address has no deployed bytecode")

    bytecode_hex = bytecode.hex()
    bytecode_md5 = hashlib.md5(bytecode).hexdigest()
    entropy = calculate_entropy(bytecode)

    # Disassembly
    disasm = EvmBytecode(bytecode_hex).disassemble()
    opcodes = [instr.name for instr in disasm]

    flags = []
    evidence = []

    if "DELEGATECALL" in opcodes:
        flags.append("proxy_detected")
        evidence.append("DELEGATECALL instruction found in bytecode")

    if "CREATE" in opcodes or "CREATE2" in opcodes:
        flags.append("contract_factory_detected")
        evidence.append("CREATE/CREATE2 instruction found (contract factory behavior)")

    if "CALLCODE" in opcodes:
        flags.append("deprecated_callcode_used")
        evidence.append("CALLCODE is deprecated and unsafe")

    if "a9059cbb" not in bytecode_hex:
        flags.append("nonstandard_transfer")
        evidence.append("Missing ERC20 transfer(address,uint256) selector")

    if entropy > 7.5:
        flags.append("obfuscated_code")
        evidence.append(f"Bytecode entropy is high ({entropy}), may be obfuscated")

    # Signature detection
    functions = extract_selectors(bytecode_hex)

    score = max(0, 100 - len(flags) * 15)

    return {
        "score": score,
        "flags": flags,
        "evidence": evidence,
        "bytecode_hash": bytecode_md5,
        "bytecode_entropy": entropy,
        "functions": functions,
        "opcodes": opcodes[:100]  # limit output
    }