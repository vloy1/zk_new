from web3 import Web3
import time
import requests
import json

from modules import standart
from modules.odos import swap_obos

suggested_fees_base_api = 'https://across.to/api/suggested-fees'

abi_arcoss = [{"inputs": [{"internalType": "address","name": "recipient","type": "address"},{"internalType": "address","name": "originToken","type": "address"},{"internalType": "uint256","name": "amount","type": "uint256"},{"internalType": "uint256","name": "destinationChainId","type": "uint256"},{"internalType": "int64","name": "relayerFeePct","type": "int64"},{"internalType": "uint32","name": "quoteTimestamp","type": "uint32"},{"internalType": "bytes","name": "message","type": "bytes"},{"internalType": "uint256","name": "maxCount","type": "uint256"}],"name": "deposit","outputs": [],"stateMutability": "payable","type": "function"}]

def calculate_suggested_fees(amount,wal:standart.Wal):

    params = {
        'token': '0x5aea5775959fbc2557cc8789bc1bf90a239d9a91',
        'destinationChainId': 42161,
        'originChainId': 324,
        'recipient': wal.adress,
        'amount': amount,
        'skipAmountLimit': 'true'
    }
    response = requests.get(suggested_fees_base_api, params)
    if response.status_code == 200:
        parsed_data = json.loads(response.text)
        timestamp = parsed_data['timestamp']
        relay_fee_pact = parsed_data['relayFeePct']
        return timestamp, relay_fee_pact
    else:
        raise Exception(f'got non 200 status code from across suggested-fees API - {response.status_code}')
    
def reserv_swap(wal:standart.Wal,w3):
    balanse_usdc = standart.balanse_token(wal,w3,standart.usdc.contract)
    if balanse_usdc >0:
        swap_obos(wal,standart.usdc.contract,standart.eth.contract,1)
        time.sleep(40)
        

def arcoss_in_arb(wal:standart.Wal, ostatok:float): 
        w3 = Web3(Web3.HTTPProvider('https://mainnet.era.zksync.io'))
        contractSwap = Web3.to_checksum_address('0xE0B015E54d54fc84a6cB9B666099c46adE9335FF')
        reserv_swap(wal,w3)
        contract = w3.eth.contract(address=contractSwap, abi=abi_arcoss)
        nonce = w3.eth.get_transaction_count(wal.adress)
        eth_balance = w3.eth.get_balance(wal.adress)
        amount = eth_balance - int(ostatok*10**18)
        data = calculate_suggested_fees(amount,wal)
        if data:
            timestamp, relay_fee_pact = data
            x =  2 ** 256 -1
        
        tx = contract.functions.deposit(
            Web3.to_checksum_address(wal.adress), 
            Web3.to_checksum_address('0x5aea5775959fbc2557cc8789bc1bf90a239d9a91'),
            amount, 
            42161,
            int(relay_fee_pact), 
            int(timestamp), 
            b"", 
            x
        ).build_transaction(
            {
            'from': wal.adress,
            'value': amount, 
            'gas': 0,
            'nonce': nonce,
            'maxFeePerGas':0,
            'maxPriorityFeePerGas': 0,
            })
    
        gas_ = standart.gas()
        tx['maxPriorityFeePerGas'] = int(gas_[0]*1.05)
        tx['maxFeePerGas'] = int(gas_[1]*1.05)
        tx = standart.add_gas_limit(w3, tx)

        res = standart.sing_tx(w3,tx,wal,modul='arcoss_in_arb')
        return res

if __name__ =='__main__':
    privat_key = ''
    wal = standart.aka(privat_key,standart.zk)
    arcoss_in_arb(wal,0.0014)
