import requests, time
from loguru import logger
from web3 import Web3
import random
import hmac, base64

list_send = []
RETRY = 0 
sub = False # True or False

def okx_data(api_key, secret_key, passphras, request_path="/api/v5/account/balance?ccy=USDT", body='', meth="GET"):

    try:
        import datetime
        def signature(
            timestamp: str, method: str, request_path: str, secret_key: str, body: str = ""
        ) -> str:
            if not body:
                body = ""

            message = timestamp + method.upper() + request_path + body
            mac = hmac.new(
                bytes(secret_key, encoding="utf-8"),
                bytes(message, encoding="utf-8"),
                digestmod="sha256",
            )
            d = mac.digest()
            return base64.b64encode(d).decode("utf-8")

        dt_now = datetime.datetime.utcnow()
        ms = str(dt_now.microsecond).zfill(6)[:3]
        timestamp = f"{dt_now:%Y-%m-%dT%H:%M:%S}.{ms}Z"

        base_url = "https://www.okex.com"
        headers = {
            "Content-Type": "application/json",
            "OK-ACCESS-KEY": api_key,
            "OK-ACCESS-SIGN": signature(timestamp, meth, request_path, secret_key, body),
            "OK-ACCESS-TIMESTAMP": timestamp,
            "OK-ACCESS-PASSPHRASE": passphras,
            'x-simulated-trading': '0'
        }
    except Exception as ex:
        logger.error(ex)
    return base_url, request_path, headers

def evm_wallet(key):

    try:
        web3 = Web3(Web3.HTTPProvider('https://arb1.arbitrum.io/rpc'))
        wallet = web3.eth.account.from_key(key).address
        return wallet
    except:
        return key

def value_okx():

    '''
    OKX
    BSC
    ERC20
    TRC20
    Polygon
    Avalanche C-Chain
    Avalanche X-Chain
    Arbitrum One
    Optimism
    Fantom
    '''
                  
    
    SUB_ACC = sub # True / False

    return SUB_ACC

def okx_withdraw(wallet, amount_min, amount_max,OKX_KEYS):

    CHAIN = 'ERC20'
    SYMBOL = 'MEME'
    FEE = 401.60 # комса на вывод
    amount_from = amount_min
    amount_to = amount_max
    SUB_ACC = value_okx()
    AMOUNT = round(random.uniform(amount_from, amount_to), 7)

    api_key = OKX_KEYS["account_1"]['api_key']
    secret_key = OKX_KEYS["account_1"]['api_secret']
    passphras = OKX_KEYS["account_1"]['password']

    try:
        
        if SUB_ACC == True:

            try:

                _, _, headers = okx_data(api_key, secret_key, passphras, request_path=f"/api/v5/users/subaccount/list", meth="GET")
                list_sub =  requests.get("https://www.okx.cab/api/v5/users/subaccount/list", timeout=10, headers=headers) 
                list_sub = list_sub.json()

                
                for sub_data in list_sub['data']:

                    name_sub = sub_data['subAcct']

                    _, _, headers = okx_data(api_key, secret_key, passphras, request_path=f"/api/v5/asset/subaccount/balances?subAcct={name_sub}&ccy={SYMBOL}", meth="GET")
                    sub_balance = requests.get(f"https://www.okx.cab/api/v5/asset/subaccount/balances?subAcct={name_sub}&ccy={SYMBOL}",timeout=10, headers=headers)
                    sub_balance = sub_balance.json()
                    sub_balance = sub_balance['data'][0]['bal']

                    logger.info(f'{name_sub} | sub_balance : {sub_balance} {SYMBOL}')

                    body = {"ccy": f"{SYMBOL}", "amt": str(sub_balance), "from": 6, "to": 6, "type": "2", "subAcct": name_sub}
                    _, _, headers = okx_data(api_key, secret_key, passphras, request_path=f"/api/v5/asset/transfer", body=str(body), meth="POST")
                    a = requests.post("https://www.okx.cab/api/v5/asset/transfer",data=str(body), timeout=10, headers=headers)
                    a = a.json()
                    time.sleep(1)

            except Exception as error:
                logger.error(f'{error}. list_sub : {list_sub}')

        try:
            _, _, headers = okx_data(api_key, secret_key, passphras, request_path=f"/api/v5/account/balance?ccy={SYMBOL}")
            balance = requests.get(f'https://www.okx.cab/api/v5/account/balance?ccy={SYMBOL}', timeout=10, headers=headers)
            balance = balance.json()
            balance = balance["data"][0]["details"][0]["cashBal"]
            # print(balance)

            if balance != 0:
                body = {"ccy": f"{SYMBOL}", "amt": float(balance), "from": 18, "to": 6, "type": "0", "subAcct": "", "clientId": "", "loanTrans": "", "omitPosRisk": ""}
                _, _, headers = okx_data(api_key, secret_key, passphras, request_path=f"/api/v5/asset/transfer", body=str(body), meth="POST")
                a = requests.post("https://www.okx.cab/api/v5/asset/transfer",data=str(body), timeout=10, headers=headers)
        except Exception as ex:
            pass

        body = {"ccy":SYMBOL, "amt":AMOUNT, "fee":FEE, "dest":"4", "chain":f"{SYMBOL}-{CHAIN}", "toAddr":wallet}
        _, _, headers = okx_data(api_key, secret_key, passphras ,request_path=f"/api/v5/asset/withdrawal", meth="POST", body=str(body))
        a = requests.post("https://www.okx.cab/api/v5/asset/withdrawal",data=str(body), timeout=10, headers=headers)
        result = a.json()
        # cprint(result, 'blue')

        if result['code'] == '0':
            logger.success(f"withdraw success => {wallet} | {AMOUNT} {SYMBOL}")
            list_send.append(f'{1 }okx_withdraw | {AMOUNT} {SYMBOL}')
            return AMOUNT
        else:
            error = result['msg']
            logger.error(f"withdraw unsuccess => {wallet} | error : {error}")
            list_send.append(f"{0 }okx_withdraw :  {result['msg']}")
            return 0

    except Exception as error:
        logger.error(f"withdraw unsuccess => {wallet} | error : {error}")
        return 0 
    
def wallett(file):
    try:
        private = open(file,'r').read().splitlines()
        wallet = private[00]
        return wallet
    except:
        print(f'Кошельки кончились {file}')

def wallett_del(file):
    ish = open(file,'r').readlines()
    print(f'удалил кошелек {ish[00]}')
    del ish[00]
    with open(file, "w") as file:
        file.writelines(ish)
    
if __name__=='__main__':
    while True:
        wal = wallett('wal.txt')
        okx_withdraw(wal,100,101)
        wallett_del('wal.txt')

