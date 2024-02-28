from eth_abi import encode
from web3 import Web3
import time
import json

from modules import standart
from modules.apruve import apruve

with open("modules/zk_swap_abi.json", "r") as file:
    zk_swap_abi = json.load(file)

def zk_swap_swap(wal:standart.Wal,token1:str,token2:str,amount:int): 
    w3 = Web3(Web3.HTTPProvider('https://mainnet.era.zksync.io'))
    contractSwap = Web3.to_checksum_address('0x18381c0f738146Fb694DE18D1106BdE2BE040Fa4')
    contract = w3.eth.contract(address=contractSwap, abi=zk_swap_abi)
    
    if token1 == '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE':
        token1 = '0x5aea5775959fbc2557cc8789bc1bf90a239d9a91'
        value = amount
    elif token2 == '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE':
        token2 = '0x5aea5775959fbc2557cc8789bc1bf90a239d9a91'
        value = 0
        amount = int(apruve(token1,contractSwap,wal)*0.2)
        time.sleep(15)

    new_adress_token1 = Web3.to_checksum_address(token1)
    new_adress_token2 = Web3.to_checksum_address(token2)
    
    nonce = w3.eth.get_transaction_count(wal.adress)
    deadline = int(time.time()) + 1000000
    if token1 == '0x5aea5775959fbc2557cc8789bc1bf90a239d9a91':
        tx = contract.functions.swapExactETHForTokens(
            0,
            [new_adress_token1,
            new_adress_token2],
            wal.adress,
            deadline,
        ).build_transaction(
            {
            'from': wal.adress,
            'value': value, 
            'gas': 0,
            'nonce': nonce,
            'maxFeePerGas':0,
            'maxPriorityFeePerGas': 0,
            })
    else:
        
        tx = contract.functions.swapExactTokensForETH(
            amount,
            0,
            [new_adress_token1,
            new_adress_token2],
            wal.adress,
            deadline,
        ).build_transaction(
            {
            'from': wal.adress,
            'value': value, 
            'gas': 0,
            'nonce': nonce,
            'maxFeePerGas':0,
            'maxPriorityFeePerGas': 0,
            })

   
    gas_ = standart.gas()
    tx['maxPriorityFeePerGas'] = 0
    tx['maxFeePerGas'] = int(gas_[1]*1.05)
    tx = standart.add_gas_limit(w3, tx)

    res = standart.sing_tx(w3,tx,wal,modul='zk_swap')
    return res