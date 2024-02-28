from web3 import Web3
from web3.middleware import geth_poa_middleware
import time

from modules import standart
from modules.apruve import apruve
from modules.inch1 import swap_1inch

abi_woofi = '[{"inputs":[{"internalType":"address","name":"_weth","type":"address"},{"internalType":"address","name":"_pool","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"newPool","type":"address"}],"name":"WooPoolChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"enum IWooRouterV2.SwapType","name":"swapType","type":"uint8"},{"indexed":true,"internalType":"address","name":"fromToken","type":"address"},{"indexed":true,"internalType":"address","name":"toToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"fromAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"toAmount","type":"uint256"},{"indexed":false,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"address","name":"rebateTo","type":"address"}],"name":"WooRouterSwap","type":"event"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"approveTarget","type":"address"},{"internalType":"address","name":"swapTarget","type":"address"},{"internalType":"address","name":"fromToken","type":"address"},{"internalType":"address","name":"toToken","type":"address"},{"internalType":"uint256","name":"fromAmount","type":"uint256"},{"internalType":"uint256","name":"minToAmount","type":"uint256"},{"internalType":"address payable","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"externalSwap","outputs":[{"internalType":"uint256","name":"realToAmount","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"stuckToken","type":"address"}],"name":"inCaseTokenGotStuck","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"isWhitelisted","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"fromToken","type":"address"},{"internalType":"address","name":"toToken","type":"address"},{"internalType":"uint256","name":"fromAmount","type":"uint256"}],"name":"querySwap","outputs":[{"internalType":"uint256","name":"toAmount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"quoteToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newPool","type":"address"}],"name":"setPool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"target","type":"address"},{"internalType":"bool","name":"whitelisted","type":"bool"}],"name":"setWhitelisted","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"fromToken","type":"address"},{"internalType":"address","name":"toToken","type":"address"},{"internalType":"uint256","name":"fromAmount","type":"uint256"},{"internalType":"uint256","name":"minToAmount","type":"uint256"},{"internalType":"address payable","name":"to","type":"address"},{"internalType":"address","name":"rebateTo","type":"address"}],"name":"swap","outputs":[{"internalType":"uint256","name":"realToAmount","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"fromToken","type":"address"},{"internalType":"address","name":"toToken","type":"address"},{"internalType":"uint256","name":"fromAmount","type":"uint256"}],"name":"tryQuerySwap","outputs":[{"internalType":"uint256","name":"toAmount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"wooPool","outputs":[{"internalType":"contract IWooPPV2","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]'

def swap_woofi(wal:standart.Wal,token1:str,token2:str,amount:int): 
    try:
        w3 = Web3(Web3.HTTPProvider('https://mainnet.era.zksync.io'))
        contractSwap = Web3.to_checksum_address('0xfd505702b37Ae9b626952Eb2DD736d9045876417')
        contract = w3.eth.contract(address=contractSwap, abi=abi_woofi)
        nonce = w3.eth.get_transaction_count(wal.adress)
        new_adress_token1 = Web3.to_checksum_address(token1)
        new_adress_token2 = Web3.to_checksum_address(token2)
        if token1 == '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE': 
            value = amount
        else:
            balanse = apruve(new_adress_token1,contractSwap,wal)
            if amount == 1:
                amount = balanse
            value = 0
            time.sleep(60)
            nonce = w3.eth.get_transaction_count(wal.adress)
        minToAmount = contract.functions.tryQuerySwap(
            new_adress_token1,
            new_adress_token2,
            amount
        ).call()
        tx = contract.functions.swap(
            new_adress_token1,
            new_adress_token2,
            amount,
            minToAmount,
            wal.adress,
            wal.adress
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
        tx['maxPriorityFeePerGas'] = int(gas_[0]*1.05)
        tx['maxFeePerGas'] = int(gas_[1]*1.05)
        tx = standart.add_gas_limit(w3, tx)

        res = standart.sing_tx(w3,tx,wal,modul='swap woofi')
        return res
    except Exception as a:
        standart.logging.error(f'{wal.adress}:woofi:{str(a)}')
        res = swap_1inch(wal,token1,token2,amount)
        return res