import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv(os.path.expanduser('~/.env.sonic'))
private_key = os.getenv('PRIVATE_KEY')

w3 = Web3(Web3.HTTPProvider("https://rpc.soniclabs.com"))
account = w3.eth.account.from_key(private_key)
treasury_addr = '0x22d5598d45651eB117D00b38DdC679fa208493Ad'

abi = [{"name": "claimReward", "type": "function", "stateMutability": "nonpayable", "inputs": [], "outputs": []}]
contract = w3.eth.contract(address=w3.to_checksum_address(treasury_addr), abi=abi)

print("Attempting to claim reward...")
try:
    nonce = w3.eth.get_transaction_count(account.address)
    txn = contract.functions.claimReward().build_transaction({
        'chainId': 146,
        'nonce': nonce,
        'gas': 200000,
        'gasPrice': w3.eth.gas_price,
    })
    signed_txn = w3.eth.account.sign_transaction(txn, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"Success! Hash: {tx_hash.hex()}")
except Exception as e:
    print(f"Claim failed: {e}")
