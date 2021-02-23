#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 11:48:55 2020

@author: christophboomer
"""


import pandas as pd
import requests
import hashlib,hmac
import json
import urllib
import numpy as np
import math
from binance.client import Client

api_key = "oH06ES95OuUn9X87CPmC0xvJfhmh5bL2O9nfFhMkngHPdjlM5lYXvBWSKuOAaIvH"
api_secret = "1VClNkmSGB5N6kQgsk2ZkSNoa9qzZVQzbH8UXlFr6gJVlGIIg47Y5tWYgHNDSTPH"
client=Client(api_key,api_secret,{"verify": False, "timeout": 30})
'''
print(client.get_account(recvWindow=5000))

print(request)
'''

from decimal import Decimal
from decimal import getcontext
from decimal import ROUND_DOWN
import time


'''
precision = 0.00003000

price=0.0026531930000


price=precision *round(price/precision)
#price=float("%.8f" % price)
print(str(price))
print(price)
print(price%precision)




price=precision *round(price/precision)
getcontext().prec = 100
getcontext().rounding = ROUND_DOWN
numCoins = Decimal(int(price*1000000))/1000000
precision=Decimal(int(precision*1000000))/1000000
print(numCoins)
print(numCoins%precision)
'''

'''

print(price)
print(value)

amount = balances['BTC']
info = client.get_symbol_info(symbol="BTCUSDT")
quantity = (1 / price) * amount
lotSize = info['filters'][2]
minQty = float(lotSize['minQty'])
stepSize = float(lotSize['stepSize'])
quantity = stepSize * round(quantity / stepSize)
getcontext().prec = 100
getcontext().rounding = ROUND_DOWN
quantity = Decimal(int(quantity * 1000000)) / 1000000

print(minQty)
print(stepSize)
print(quantity)
'''

'''
request = client.get_account(recvWindow=5000)
tempBalances = request['balances']
balances = {}
for dictionary in tempBalances:
    coin = dictionary['asset']
    balance = float(dictionary['free'])
    if float(dictionary['locked']) > 0:
        print(f"{dictionary['locked']} is locked in coin {coin}")
    balances[coin] = balance

quantityBTC = balances['BTC']

fee = client.get_trade_fee(symbol='XEMBTC')["tradeFee"][0]["taker"]
quantityBTC = quantityBTC * (1-fee)

info = client.get_symbol_info(symbol='XEMBTC')

print(info['filters'][3]['minNotional'])

price = float(client.get_symbol_ticker(symbol="TRXBTC")["price"])
quantity = (1 / price) * quantityBTC
lotSize = info['filters'][2]
minQty = float(lotSize['minQty'])
stepSize = float(lotSize['stepSize'])

print(stepSize)

quantity = stepSize * math.floor(quantity / stepSize)
getcontext().prec = 100
getcontext().rounding = ROUND_DOWN
quantity = Decimal(int(quantity * 1000000)) / 1000000
print(f"quantity {quantity} vs minQty {minQty}")
print(stepSize)
print(type(math.floor(1.3352)))
'''

quantityBTC=0.000110704185
info = client.get_symbol_info(symbol='BNBBTC')
minNotional = float(info['filters'][3]['minNotional'])
print(minNotional)
if quantityBTC <= minNotional:
    print('right')
if 0.1 < Decimal(0.103):
    print('yes')

if Decimal(0.0002290799999999999984004884611560326490575789648573845624923706054687500000000)< 0.0001:
    print('verdammi nei')