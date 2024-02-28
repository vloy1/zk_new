from web3 import Web3
from web3.middleware import geth_poa_middleware
import time
import requests
import random

from modules import standart
from modules.apruve import apruve

api_1inch = ['Fa6cunfuKw69hLx4y6jFOCbReTsoQAJ5',
            'ybyVh5urU6XmJX4r5t44GD47Pe582CBP',
            'fImQ04xxfSW1IfM6TnvyqN2DQpdJNjRS',
            'uwmALfN7JJu5XCaE0UJp57sB7ixMFHyt',
            '2fiGT9A9NktnkA1eyDAf88yuCwaK6rwy',
            'RfnYTJWnIgGKRJoGZnsoiDHZsAC4FQS3',
            'VBGk0ZSLGVVUaNa14smrjRfSZagVRH4Y',
            'r2PjhdFihUZyx4GJEidZmcvovxnsFeTt',
            '8s6UEmo3tbZnv0p99xfoPvirK8xU6IAy',
            '5Y50N1l5kT3RVWQ3JbFHVNmp5r6HCZfl',
            'ESd6qzSr9XipzIYXXFK89pFzKybKjsv2'] 

def swap_1inch(wal:standart.Wal,token1:str,token2:str,amount:int):
    w3 = Web3(Web3.HTTPProvider('https://mainnet.era.zksync.io'))

    headers = { "Authorization": f"Bearer {wal.api}", "accept": "application/json" }

    new_adress_token1 = Web3.to_checksum_address(token1)
    swap_contract= Web3.to_checksum_address('0x6e2B76966cbD9cF4cC2Fa0D76d24d5241E0ABC2F')

    if token1 != '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE': 
        amount = apruve(new_adress_token1,swap_contract,wal)

    slippage = 1 # слиппейдж, дефолт от 1 до 3

    _1inchurl = f'https://api.1inch.dev/swap/v5.2/324/swap?src={token1}&dst={token2}&amount={amount}&from={wal.adress}&slippage={slippage}'

    call_data = requests.get(url = _1inchurl, headers= headers)

    if call_data.status_code == 200:
        api_data = call_data.json()
    try:
        tx  = api_data['tx']
    except:
        time.sleep(60)
        call_data = requests.get(_1inchurl)
        if call_data.status_code == 200:
            api_data = call_data.json()
            tx  = api_data['tx']
    try:  
        tx['from']      = w3.to_checksum_address(tx['from'])    
        tx['chainId']   = 324
        tx['nonce']     = w3.eth.get_transaction_count(wal.adress)
        tx['to']        = w3.to_checksum_address(tx['to'])
        tx['gasPrice']  = int(tx['gasPrice'])
        tx['gas']       = int(tx['gas'])
        tx['value']     = int(tx['value'])
        try:
            signed_txn = w3.eth.account.sign_transaction(tx, private_key=wal.key)
        except Exception as a:
            if 'from field must match' in a.args[0]:
                s = a.args[0]
                start_index = s.find("key's ") + len("key's ")
                end_index = s.find(",", start_index)
                result = s[start_index:end_index]
                tx['from'] = result
                signed_txn = w3.eth.account.sign_transaction(tx, private_key=wal.key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        stat = standart.status(tx_hash,wal,standart.zk)
        standart.logging.info(f'{wal.adress} swap 1inch ({stat})')
        return stat
    except Exception as a:
        if len(call_data.text) > 60:
            standart.logging.error(f'{wal} {str(a)}')
            return 0
        else :
            if 'error' in call_data.text:
                time.sleep(random.randint(30,60))
                api_key = random.choice(api_1inch)
                if wal.api == api_key:
                    api_key = random.choice(api_1inch)
                headers = { "Authorization": f"Bearer {api_key}", "accept": "application/json" }
                _1inchurl = f'https://api.1inch.dev/swap/v5.2/324/swap?src={token1}&dst={token2}&amount={amount}&from={wal.adress}&slippage={slippage}'

                call_data = requests.get(url = _1inchurl, headers= headers)

                if call_data.status_code == 200:
                    api_data = call_data.json()
                try:
                    tx  = api_data['tx']
                except:
                    time.sleep(60)
                    call_data = requests.get(_1inchurl)
                    if call_data.status_code == 200:
                        api_data = call_data.json()
                        tx  = api_data['tx']
                try:        
                    tx['chainId']   = 324
                    tx['nonce']     = w3.eth.get_transaction_count(wal.adress)
                    tx['to']        = w3.to_checksum_address(tx['to'])
                    tx['gasPrice']  = int(tx['gasPrice'])
                    tx['gas']       = int(tx['gas'])
                    tx['value']     = int(tx['value'])

                    signed_txn = w3.eth.account.sign_transaction(tx, private_key=wal.key)
                    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                    stat = standart.status(tx_hash,wal,standart.zk)
                    standart.logging.info(f'{wal.adress} swap 1inch ({stat})')
                    return stat
                except:
                    standart.logging.error(f'{wal.adress} {str(a)}')
                    return 0
            else:
                standart.logging.error(f'{wal.adress} {call_data.text} ')
                return 0