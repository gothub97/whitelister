from web3 import Web3
from decouple import config

w3 = Web3(Web3.HTTPProvider(config('ETH_RPC_URL')))

ERC20_ABI = [
    {"constant": True, "name": "name", "inputs": [], "outputs": [{"name": "", "type": "string"}], "type": "function"},
    {"constant": True, "name": "symbol", "inputs": [], "outputs": [{"name": "", "type": "string"}], "type": "function"},
    {"constant": True, "name": "decimals", "inputs": [], "outputs": [{"name": "", "type": "uint8"}], "type": "function"},
]

def fetch_token_metadata(token_address: str):
    address = Web3.to_checksum_address(token_address)
    contract = w3.eth.contract(address=address, abi=ERC20_ABI)
    return {
        "name": contract.functions.name().call(),
        "symbol": contract.functions.symbol().call(),
        "decimals": contract.functions.decimals().call()
    }

def get_bytecode_for_address(address):
    bytecode = w3.eth.get_code(Web3.to_checksum_address(address))
    if not bytecode or bytecode == b'':  # Empty contract or error
        raise ValueError("No bytecode found")
    return bytecode.hex()