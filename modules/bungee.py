from eth_abi import encode
from web3 import Web3
import random
import requests
import json

from modules import standart
from modules.apruve import apruve

def get_bungee_data():
    url = "https://refuel.socket.tech/chains"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data

def get_bungee_limits():

    from_chain_id   = 324
    to_chain_id     = 100

    data = get_bungee_data()

    for i in range(len(data['result'])):
        if data['result'][i]['chainId'] == from_chain_id:
            infos = data['result'][i]['limits']
            if  [x for x in infos if x['chainId'] == to_chain_id][0] \
            and [x for x in infos if x['chainId'] == to_chain_id][0]['isEnabled'] == True:
                
                info = [x for x in infos if x['chainId'] == to_chain_id][0]
                return int(info['minAmount']), int(info['maxAmount'])
            else:
                print('error')
                return 0, 0

def bungee_gnosis(wal:standart.Wal):
        w3 = Web3(Web3.HTTPProvider('https://mainnet.era.zksync.io'))
        contractSwap = Web3.to_checksum_address('0x7Ee459D7fDe8b4a3C22b9c8C7aa52AbadDd9fFD5')
        contract = w3.eth.contract(address=contractSwap, abi='[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"destinationReceiver","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"destinationChainId","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Donation","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"}],"name":"GrantSender","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"}],"name":"RevokeSender","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"receiver","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"srcChainTxHash","type":"bytes32"}],"name":"Send","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"receiver","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdrawal","type":"event"},{"inputs":[{"components":[{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"bool","name":"isEnabled","type":"bool"}],"internalType":"struct GasMovr.ChainData[]","name":"_routes","type":"tuple[]"}],"name":"addRoutes","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address payable[]","name":"receivers","type":"address[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"bytes32[]","name":"srcChainTxHashes","type":"bytes32[]"},{"internalType":"uint256","name":"perUserGasAmount","type":"uint256"},{"internalType":"uint256","name":"maxLimit","type":"uint256"}],"name":"batchSendNativeToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"chainConfig","outputs":[{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"bool","name":"isEnabled","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"destinationChainId","type":"uint256"},{"internalType":"address","name":"_to","type":"address"}],"name":"depositNativeToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"chainId","type":"uint256"}],"name":"getChainData","outputs":[{"components":[{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"bool","name":"isEnabled","type":"bool"}],"internalType":"struct GasMovr.ChainData","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"}],"name":"grantSenderRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"processedHashes","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"}],"name":"revokeSenderRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address payable","name":"receiver","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes32","name":"srcChainTxHash","type":"bytes32"},{"internalType":"uint256","name":"perUserGasAmount","type":"uint256"},{"internalType":"uint256","name":"maxLimit","type":"uint256"}],"name":"sendNativeToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"senders","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"bool","name":"_isEnabled","type":"bool"}],"name":"setIsEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"setPause","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"setUnPause","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdrawBalance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"}],"name":"withdrawFullBalance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]')
        nonce = w3.eth.get_transaction_count(wal.adress)
        adress = Web3.to_checksum_address(wal.adress)
        limits = get_bungee_limits()
        amount = random.randint(10000000000000,60000000000000)
        min_limits = limits[0]
        if amount < min_limits:
            print(f'{amount} < {limits} ')
            amount = min_limits
        tx = contract.functions.depositNativeToken(
            100,
            adress
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
        gas_gas = int(tx['gas'] * tx['maxFeePerGas'])
        tx['value'] = tx['value'] + gas_gas
        
        res = standart.sing_tx(w3,tx,wal,modul='bungee')
        return res