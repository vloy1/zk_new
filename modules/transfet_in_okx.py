from eth_abi import encode
from web3 import Web3

from modules import standart

def send_birg_arb(wal:standart.Wal,file):
    w3 = Web3(Web3.HTTPProvider(standart.arb.rpc))
    wal_birg = standart.wallett(file)
    standart.wallett_del(file)
    adress_to = Web3.to_checksum_address(wal_birg)
    eth_balance = w3.eth.get_balance(wal.adress)
    nonce = w3.eth.get_transaction_count(wal.adress)
    tx = {
        'chainId': 42161,
        'from': wal.adress,
        'to': adress_to,
        'value': eth_balance, 
        'gas': 700000,
        'nonce': nonce,
        'maxFeePerGas':0,
        'maxPriorityFeePerGas': 0,
        }
    gas_ = standart.gas(standart.arb.rpc)
    tx['maxPriorityFeePerGas'] = int(gas_[0]*1.05)
    tx['maxFeePerGas'] = int(gas_[1]*1.05)
    gas_gas = int(tx['gas'] * tx['maxFeePerGas'])
    tx['value'] = tx['value'] - int(gas_gas*1.05)
    res = standart.sing_tx(w3,tx,wal,standart.arb,'transfer na birgy')
    return res