from eth_abi import encode
from web3 import Web3
import time
import json

from modules import standart
from modules.apruve import apruve

with open("modules/mute_abi.json", "r") as file:
    mute_abi = json.load(file)

def mute_swap(wal:standart.Wal,token1:str,token2:str,amount:int): 
    w3 = Web3(Web3.HTTPProvider('https://mainnet.era.zksync.io'))
    contractSwap = Web3.to_checksum_address('0x8B791913eB07C32779a16750e3868aA8495F5964')
    contract = w3.eth.contract(address=contractSwap, abi=mute_abi)
    
    if token1 == '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE':
        token1 = '0x5aea5775959fbc2557cc8789bc1bf90a239d9a91'
        value = amount
    elif token2 == '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE':
        token2 = '0x5aea5775959fbc2557cc8789bc1bf90a239d9a91'
        value = 0
        amount = apruve(token1,contractSwap,wal)
        time.sleep(15)

    new_adress_token1 = Web3.to_checksum_address(token1)
    new_adress_token2 = Web3.to_checksum_address(token2)
    min_amount_out = contract.functions.getAmountOut(
            amount,
            new_adress_token1,
            new_adress_token2
        ).call()
    min_amount =int(min_amount_out[0] - (min_amount_out[0] / 100 * 3))
    nonce = w3.eth.get_transaction_count(wal.adress)
    deadline = int(time.time()) + 1000000
    if token1 == '0x5aea5775959fbc2557cc8789bc1bf90a239d9a91':
        tx = contract.functions.swapExactETHForTokens(
            min_amount,
            [new_adress_token1,
            new_adress_token2],
            wal.adress,
            deadline,
            [False, False]
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
            min_amount,
            [new_adress_token1,
            new_adress_token2],
            wal.adress,
            deadline,
            [True, False]
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

    res = standart.sing_tx(w3,tx,wal,modul='mute')
    return res