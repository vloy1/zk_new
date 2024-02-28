import time
import random
import multiprocessing

from modules.odos import swap_obos
from modules.across import arcoss_in_arb
from modules.transfet_in_okx import send_birg_arb
from modules.transfer_s_okx_v_zk import okx_withdraw
from modules.standart import *
from modules.mute import mute_swap
from modules.spase_fi import spase_fi_swap
from modules.zk_swap import zk_swap_swap

amount_dep = [0.01,0.02] # min,max кол-во ЕТН для вывода
amount_swap = [0.0003,0.0004] # min,max кол-во ЕТН для свапов woofi\1inch
protsent_swap_ = [0.6,0.7] # % от денег на аке которое будем свапать maverik\obos
ostatok= [0.0014,0.0018] # остаток денег на кошельке
time_tx = [10,50] #задержка между транзакциями 
time_akks = [10,50] #задержка между аками
time_potok = 10 #задержка между запусками потоков
n_swap = 4
n_g = [3,5] # количество свапов
max_gas = 40 # лимит газа для транзакций 
file_birgh = 'adres_birgh.txt' # адреса okx для выода на них
file_wal_1 = 'wal.txt' # файл аков которые будем прогонять
n_potok = 1 # количество потоков

OKX_KEYS = {
    'account_1' : {
        'api_key'   : '-ab66-45bd-8452-e19c235df717',
        'api_secret': '',
        'password'  : '!',
    }
}

def swwaps_(wal:Wal,w3:Web3):
    balanse_usdc = balanse_token(wal,w3,usdc.contract)
    swpalki = [spase_fi_swap,zk_swap_swap]
    if balanse_usdc > 0:
        amount = 0
        res = random.choice(swpalki)(wal,usdc.contract,eth.contract,amount)
        if res != 1:
            time.sleep(57)
            res = random.choice(swpalki)(wal,usdc.contract,eth.contract,amount)
    else:
        amount = int(random.uniform(amount_swap[0],amount_swap[1])*10**18)
        res = random.choice(swpalki)(wal,eth.contract,usdc.contract,amount)
        if res != 1:
            time.sleep(57)
            res = random.choice(swpalki)(wal,eth.contract,usdc.contract,amount)
    return res

def swawps_osnova(wal:Wal,w3:Web3):
    balanse_usdc = balanse_token(wal,w3,usdc.contract)
    swpalki = [swap_obos,mute_swap]
    if balanse_usdc > 1000000:
        amount = balanse_usdc
        res = random.choice(swpalki)(wal,usdc.contract,eth.contract,amount)
        if res != 1:
            time.sleep(57)
            res = random.choice(swpalki)(wal,usdc.contract,eth.contract,amount)
            if res == 0:
                res = swap_obos(wal,usdc.contract,eth.contract,amount)
    else:
        amount = int(w3.eth.get_balance(wal.adress) * random.uniform(protsent_swap_[0],protsent_swap_[1]))
        res = random.choice(swpalki)(wal,eth.contract,usdc.contract,amount)
        if res != 1:
            time.sleep(57)
            res = random.choice(swpalki)(wal,eth.contract,usdc.contract,amount)
            if res == 0:
                res = swap_obos(wal,eth.contract,usdc.contract,amount)
    return res


def run(wal:Wal):
    n_swaps = n_swap
    
    w3 = Web3(Web3.HTTPProvider('https://mainnet.era.zksync.io'))
    #balanse_usdc = balanse_token(wal,w3,usdc.contract)
    #maverick(wal,usdc.contract,eth.contract,1)
    #swap_woofi(wal,usdc.contract,eth.contract,1)
    #swap_obos(wal,usdc.contract,eth.contract,1)
    #arcoss_in_arb(wal,ostatok[0])
    #time.sleep(60)
    #res_transfer = send_birg_arb(wal,file_birgh)
    #return 1
    #zk_swap_swap(wal,usdc.contract,eth.contract,1)
    balanse = w3.eth.get_balance(wal.adress)
    if balanse < int(amount_dep[0]*10**18):
        okx = okx_withdraw(wal.adress,amount_dep[0],amount_dep[1],OKX_KEYS)
        if okx == 0:
            time.sleep(random.randint(30,80))
            okx = okx_withdraw(wal.adress,amount_dep[0],amount_dep[1],OKX_KEYS)
            if okx == 0:
                return 'okx error'
        time_m(wal,int(amount_dep[0]*10**18))
    n = 0
    while True:
        try:
            gass(max_gas)
            res = swawps_osnova(wal,w3)
            rand_massovka = random.randint(2,4)
            g = 0
            while True:
                time.sleep(random.randint(time_tx[0],time_tx[1]))
                if rand_massovka > g:
                    try:
                        gass(max_gas)
                        swwaps_(wal,w3)
                        g = g +1
                    except Exception as a:
                        logging.error(f'{wal.adress} {str(a)}')
                else:
                    break
            n  = n + res
            time.sleep(random.randint(time_tx[0],time_tx[1]))
            if n == n_swaps:
                break
        except Exception as a:
            logging.error(f'{wal.adress} {str(a)}')
    gass(max_gas)
    res_arcos = arcoss_in_arb(wal,random.uniform(ostatok[0],ostatok[1]))
    nonce = w3.eth.get_transaction_count(wal.adress)
    logging.info(f'{wal.adress} n_swap {n_swaps} nonce {nonce} ----------------------------------------------------------------')
    time_m(wal,int((amount_dep[0]*0.8)*10**18),arb)
    gass(max_gas)
    res_transfer = send_birg_arb(wal,file_birgh)
    return res_transfer
    
def main(q):
    while True:
        time.sleep(q*time_potok)
        prvat_key = wallett(file_wal_1)
        #wallett_del(file_wal_1)
        wal = aka(prvat_key,zk)
        logging.info(f'{wal.adress} start')
        #try:
        n = run(wal)
        #except Exception as a:
            #n = 0
            #print(a)
        tex = f'{wal.adress}:{wal.key}#{n}'
        if n == 1:
            write_t(tex)
        else:
            write_f(tex)
        time.sleep(random.randint(time_akks[0],time_akks[1]))

if __name__ == '__main__':
    if n_potok == 1:
        main(1)
    pool = multiprocessing.Pool(processes=n_potok)
    p = [] 
    n = 0
    while len(p) != n_potok:
        p.append(n)
        n = n + 1
    results = pool.map(main, p)




