from eth_abi import encode
from web3 import Web3
import requests

from modules import standart
from modules.apruve import apruve

proxy = {'https': 'http://nyRg8C2D:irqski6G@45.152.227.246:63788'}

def quote(wal:standart.Wal, from_token: str, to_token: str, amount: int, slippage: float):
        url = "https://api.odos.xyz/sor/quote/v2"

        data = {
            "chainId": 324,
            "inputTokens": [
                {
                    "tokenAddress": Web3.to_checksum_address(from_token),
                    "amount": f"{amount}"
                }
            ],
            "outputTokens": [
                {
                    "tokenAddress": Web3.to_checksum_address(to_token),
                    "proportion": 1
                }
            ],
            "slippageLimitPercent": slippage,
            "userAddr": wal.adress,
            "referralCode": 4174109901,
            "compact": True
        }

        response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json=data,
        proxies = proxy
        )

        if response.status_code == 200:
            response_data = response.json()

            return response_data
        else:
            standart.logging.error(f'{wal} Bad Odos request')

def assemble(wal:standart.Wal, path_id):
        url = "https://api.odos.xyz/sor/assemble"

        data = {
            "userAddr": wal.adress,
            "pathId": path_id,
            "simulate": False,
        }

        response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json=data,
        proxies = proxy
        )

        if response.status_code == 200:
            response_data = response.json()

            return response_data
        else:
            standart.logging.error(f'{wal.adress}  Bad Odos request')

def get_tx_data(wal:standart.Wal,w3):
        tx = {
            "chainId": w3.eth.chain_id,
            "from": wal.adress,
            "gasPrice": w3.eth.gas_price,
            "nonce": w3.eth.get_transaction_count(wal.adress),
        }
        return tx

def swap_obos(wal:standart.Wal,token1:str,token2:str,amount:int):
    w3 = Web3(Web3.HTTPProvider('https://mainnet.era.zksync.io'))
    if token1 == standart.usdc.contract:
        amount = standart.balanse_token(wal,w3,token1)
        value = 0
    else:
        value = amount
        token1 = '0x0000000000000000000000000000000000000000'
    if token2 == standart.eth.contract:
        token2 = '0x0000000000000000000000000000000000000000'
    quote_data =quote(wal,token1,token2,amount,1)
    transaction_data = assemble(wal,quote_data["pathId"])
    transaction = transaction_data["transaction"]
    wal_to = Web3.to_checksum_address(transaction["to"])
    if value == 0:
        apruve(token1,wal_to,wal)
    tx = get_tx_data(wal,w3)
    tx.update(
            {
                "to": wal_to,
                "data": transaction["data"],
                "value": value,
                'gas': 4000000
            }
        )
    res = standart.sing_tx(w3,tx,wal,modul='Obos')
    return res

if __name__ == '__main__':
    privat_key = ''
    wal = standart.aka(privat_key,standart.zk)
    swap_obos(wal,standart.eth.contract,standart.usdc.contract,60000000000000)