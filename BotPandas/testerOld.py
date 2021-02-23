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
from datetime import datetime
import time
import talib

api_key = "oH06ES95OuUn9X87CPmC0xvJfhmh5bL2O9nfFhMkngHPdjlM5lYXvBWSKuOAaIvH"
api_secret = "1VClNkmSGB5N6kQgsk2ZkSNoa9qzZVQzbH8UXlFr6gJVlGIIg47Y5tWYgHNDSTPH"
client=Client(api_key,api_secret,{"verify": False, "timeout": 30})
period_dict = {60: "1m", 180: "3m", 300: "5m", 900: "15m", 1800: "30m", 3600: "1h", \
                            7200: "2h", 14400: "4h", 21600: "6h", 28800: "8h", 43200: "12h", 86400: "1d", \
                            259200: "3d", 1209600: "1w"}

pairs=['BTCUSDT','DASHBTC', 'DOGEBTC', 'LTCBTC', 'XEMBTC', 'XRPBTC',  'ETHBTC', 'SCBTC', 'DCRBTC', 'LSKBTC',
                    'STEEMBTC', 'ETCBTC', 'REPBTC', 'ARDRBTC', 'ZECBTC', 'STRATBTC', 'GNTBTC', 'ZRXBTC', 'CVCBTC', 'OMGBTC',
                    'STORJBTC', 'EOSBTC', 'SNTBTC', 'KNCBTC', 'BATBTC', 'LOOMBTC', 'QTUMBTC', 'MANABTC', 'BNTBTC', 'POLYBTC',
                    'ATOMBTC', 'TRXBTC', 'LINKBTC', 'XTZBTC', 'SNXBTC', 'MATICBTC', 'MKRBTC', 'NEOBTC',
                    'AVABTC', 'CHRBTC', 'BNBBTC', 'MDTBTC', 'LENDBTC', 'RENBTC', 'LRCBTC', 'WRXBTC', 'SXPBTC', 'STPTBTC']

'''
print(pd.Int64Index([1607]))

jump=20
timeperiod=14
testA=np.arange(0,timeperiod*jump*3,1)
volume=[]
close = np.arange(0, 1000, 1, dtype=np.float64)
macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

print( macdhist[-2:])
data=[[1,2,3,4,5]]
lis=[[1,2,3,4,5],
     [2,3,4,5,6]]
addLis=[[11,22,33,44,55],
        [22,33,44,55,66]]
lis+=data[0]
print(lis)

for i in range(10):
    try:
        info = client.get_symbol_info(symbol='EOSBTC')
        break
    except:
        time.sleep(1)
print(info)
minNotional = float(info['filters'][3]['minNotional'])
'''
timePeriod=14
period=300
jump=int(86400/period)
close=np.arange(0,10000,1)
pos=-3
for pos in range(10):
    if pos >= 0:
        pos = pos - len(close)+jump*timePeriod
    print(pos)
    print(close[-jump*timePeriod-1::jump])
    print(close[np.arange(-jump*timePeriod+pos,pos+1,jump)])