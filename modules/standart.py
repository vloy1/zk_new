from web3 import Web3
import time
import random
from web3.middleware import geth_poa_middleware
import requests
import datetime 
import logging

class Chain:

    def __init__(self,name = None,rpc = None,) -> None:
        self.name= name
        self.rpc = rpc

    def __str__(self) -> str:
        return str(self.name)
    
class Wal:

    def __init__(self,adress,key,api) -> None:
        self.adress = adress
        self.key = key
        self.api = api

    def __str__(self) -> str:
        return str(self.adress)
    
class Token:
    def __init__(self, contract, name):
        self.contract = contract
        self.name = name
    def __str__(self) -> str:
        return str(self.name)
    
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="a")
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logging.getLogger('').addHandler(console_handler)

eth = Token('0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE','eth')
usdc = Token('0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4','usdc')
usdt = Token('0x493257fd37edb34451f62edf8d2a0c418852ba4c','usdt')
    
zk = Chain('zk','https://mainnet.era.zksync.io')
arb = Chain('arb','https://arb1.arbitrum.io/rpc')

def status(tx_hash,wal,set= zk ,uts = 3):
    time.sleep(35)
    w3 = Web3(Web3.HTTPProvider(set.rpc)) 
    try:
        status_ = w3.eth.wait_for_transaction_receipt(tx_hash)
        status  = status_["status"]
        return status
    except:
        time.sleep(60)
        try:
            status_ = w3.eth.get_transaction_receipt(tx_hash)
            status  = status_["status"]
            return status
        except:
            time.sleep(30)
            start_time = datetime.datetime.now() 
            start_time = start_time - datetime.timedelta(hours=uts, minutes=7) 
            re = requests.get(f'https://block-explorer-api.mainnet.zksync.io/transactions?address={wal.adress}&pageSize=1&page=1')
            text_request = re.text.split(',')
            for time_tx in text_request:
                if 'receivedAt' in time_tx:
                    time_tx = time_tx.split('":"')
                    time_tx = datetime.datetime.strptime(time_tx[1][0:19], "%Y-%m-%dT%H:%M:%S")
                    break
            if start_time > time_tx:
                tx_hash_re = re.text[19:85] 
                status_ = w3.eth.get_transaction_receipt(tx_hash_re)
                status  = status_["status"]
                return status
            else:
                logging.info(f'и request не спас')
                return 0
        
def res_balance(adres,set,min_token = 0):
    w3 = Web3(Web3.HTTPProvider(set.rpc)) 
    eth_balance = w3.eth.get_balance(adres)
    min_tokenn = int(min_token*0.9)
    if eth_balance > min_tokenn:
        return 1
    else:
        return 0
        
def aka(privat,set:Chain,api_key = ['Fa6cunfuKw69hLx4y6jFOCbReTsoQAJ5','ybyVh5urU6XmJX4r5t44GD47Pe582CBP']):
    w3 = Web3(Web3.HTTPProvider(set.rpc))
    account = w3.eth.account.from_key(privat)
    adress = account.address
    api = random.choice(api_key)
    wal = Wal(adress,privat,api)
    return wal
    
def wallett(file):
    try:
        private = open(file,'r').read().splitlines()
        wallet = private[00]
        return wallet
    except:
        logging.error(f'Кошельки кончились {file}')

def wallett_del(file):
    ish = open(file,'r').readlines()
    del ish[00]
    with open(file, "w") as file:
        file.writelines(ish)

def write_t(text):
    with open('wal_true.txt', 'a') as f:
        f.write(f'{text}\n')

def write_f(text):
    with open('wal_false.txt', 'a') as f:
        f.write(f'{text}\n')


def balanse_token(wal:Wal,w3,token:str):
    adres_token = Web3.to_checksum_address(token) 
    contrakt = w3.eth.contract(address=adres_token,abi='[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_upgradedAddress","type":"address"}],"name":"deprecate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"deprecated","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_evilUser","type":"address"}],"name":"addBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"upgradedAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balances","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"maximumFee","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_maker","type":"address"}],"name":"getBlackListStatus","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowed","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"who","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newBasisPoints","type":"uint256"},{"name":"newMaxFee","type":"uint256"}],"name":"setParams","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"issue","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"redeem","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"basisPointsRate","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"isBlackListed","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_clearedUser","type":"address"}],"name":"removeBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"MAX_UINT","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_blackListedUser","type":"address"}],"name":"destroyBlackFunds","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_initialSupply","type":"uint256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Issue","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Redeem","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"newAddress","type":"address"}],"name":"Deprecate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"feeBasisPoints","type":"uint256"},{"indexed":false,"name":"maxFee","type":"uint256"}],"name":"Params","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_blackListedUser","type":"address"},{"indexed":false,"name":"_balance","type":"uint256"}],"name":"DestroyedBlackFunds","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"AddedBlackList","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"RemovedBlackList","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"}]') 
    balanse = contrakt.functions.balanceOf(wal.adress).call()
    return balanse

def gass(quantity_gas):
    n = 0
    while True:
        web3 = Web3(Web3.HTTPProvider('https://ethereum-mainnet.core.chainstack.com/802200266e05423a9b080969fea23ea3'))
        gas_price = web3.eth.gas_price
        gwei_gas_price = web3.from_wei(gas_price, 'gwei')
        if int(gwei_gas_price.real) < quantity_gas:
            break
        time.sleep(25)
        n = n + 1 
        if n == 20:
            logging.info(f'gas')
            n = 0
    return int(gwei_gas_price.real)

def adress_birgh():
    try:
        ish = open('adres_birgh.txt','r').readlines() #  Открываем файл
        private = open('adres_birgh.txt','r').read().splitlines() #  
        wallet = private[00]
        del ish[00] 
        with open("adres_birgh.txt", "w") as file:
            file.writelines(ish)
        return wallet
    except:
        logging.error(f'Кошельки для вывода кончились')

def time_m(wal:Wal,min_token,set=zk): 
    min_tokenn = int(min_token*0.85)
    while True:
        try:
            w3 = Web3(Web3.HTTPProvider(set.rpc)) 
            eth_balance = w3.eth.get_balance(wal.adress)
            if eth_balance > min_tokenn:
                break
            else: 
                time.sleep(5)
        except:
            time.sleep(60)

def add_gas_limit(web3, contract_txn):
    pluser = [1.02, 1.05]
    try:
        gasLimit = web3.eth.estimate_gas(contract_txn)
    except:
        gasLimit = 4000000
    contract_txn['gas'] = int(gasLimit * random.uniform(pluser[0], pluser[1]))
    return contract_txn

def add_gas_price(web3, contract_txn):
    gas_price = web3.eth.gas_price
    contract_txn['gasPrice'] = int(gas_price * random.uniform(1.01, 1.02))
    return contract_txn


def gas(rpc = zk.rpc):

    try:

        tx ={}
        max_priority_fee_per_gas = None
        max_fee_per_gas = None

        w3 = Web3(provider=Web3.HTTPProvider(rpc))

        last_block = w3.eth.get_block('latest')
        if not max_priority_fee_per_gas:
            block_number = last_block['number']
            latest_block_transaction_count = w3.eth.get_block_transaction_count(block_number)
            max_priority_fee_per_gas_lst = []
            for i in range(latest_block_transaction_count):
                try:
                    transaction = w3.eth.get_transaction_by_block(block_number, i)
                    if 'maxPriorityFeePerGas' in transaction:
                        max_priority_fee_per_gas_lst.append(transaction['maxPriorityFeePerGas'])
                except Exception:
                    continue

            if not max_priority_fee_per_gas_lst:
                max_priority_fee_per_gas = 250000000
            else:
                max_priority_fee_per_gas_lst.sort()
                max_priority_fee_per_gas = max_priority_fee_per_gas_lst[len(max_priority_fee_per_gas_lst) // 2]
        if not max_fee_per_gas:
            base_fee = int(last_block['baseFeePerGas'] * 1)
            max_fee_per_gas = base_fee + max_priority_fee_per_gas
        tx['maxPriorityFeePerGas'] = max_priority_fee_per_gas
        tx['maxFeePerGas'] = max_fee_per_gas
    except:
        max_priority_fee_per_gas = 0
        max_fee_per_gas = 300000000

    return max_priority_fee_per_gas,max_fee_per_gas

def sing_tx(w3,tx,wal:Wal,set = zk, modul = 'sing_tx'):
    signed_txn = w3.eth.account.sign_transaction(tx, private_key=wal.key)
    try:
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        statu = status(tx_hash,wal,set,wal)
        logging.info(f'{wal.adress} {modul} ({statu})')
        return statu
    except Exception as a:
        logging.error(f'{wal.adress}:{modul}:{str(a)}')
        time.sleep(30)
        signed_txn = w3.eth.account.sign_transaction(tx, private_key=wal.key)
        try:
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            statu = status(tx_hash,set,wal)
            logging.info(f'{wal.adress} {modul} ({statu})')
            return statu
        except Exception as a:
            logging.error(f'{wal.adress}:{modul}:{str(a)}')
            return 0



