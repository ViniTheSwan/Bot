# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 15:07:51 2020

@author: vinmue
"""
# from binance.client import Client
import binance
from poloniex import Poloniex
# from binance.websockets import BinanceSocketManager
import requests
import ast
import math
import hashlib, hmac
import json
import urllib
import time
from binance.client import Client
from decimal import Decimal
from decimal import getcontext
from decimal import ROUND_DOWN


class API(object):
    def __init__(self):
        # from account yvieboy
        self.api_key = "oH06ES95OuUn9X87CPmC0xvJfhmh5bL2O9nfFhMkngHPdjlM5lYXvBWSKuOAaIvH"
        self.api_secret = "1VClNkmSGB5N6kQgsk2ZkSNoa9qzZVQzbH8UXlFr6gJVlGIIg47Y5tWYgHNDSTPH"
        self.client = Client(api_key=self.api_key, api_secret=self.api_secret)
        # for changing periods in seconds binance accepted strings
        self.period_dict = {60: "1m", 180: "3m", 300: "5m", 900: "15m", 1800: "30m", 3600: "1h", \
                            7200: "2h", 14400: "4h", 21600: "6h", 28800: "8h", 43200: "12h", 86400: "1d", \
                            259200: "3d", 1209600: "1w"}


    def getFee(self, pair):
        fee = self.client.get_trade_fee(symbol=pair)["tradeFee"][0]["taker"]
        return fee

    def returnTicker(self):
        # returns a list of dictionaries with key symbol and price for each pair
        ###url="https://api.binance.com/api/v3/ticker/price?"
        for k in range(10):
            try:
                request = self.client.get_all_tickers()
                ###request = requests.get(url, timeout=1)
                ###request.raise_for_status()
                break
            except:
                print('request failed')
                time.sleep(1)
        ticker = {pair.pop('symbol'): pair for pair in request}
        #{'ETHBTC': {'price': '0.03380000'},
        return ticker

    def returnCurrentPrice(self, pair):
        # gives dictionary with keys symbol (pair) and price
        ###url="https://api.binance.com/api/v3/ticker/price?symbol={}".format(pair)
        for k in range(10):
            try:
                request = self.client.get_symbol_ticker(symbol=pair)
                ###request = requests.get(url, timeout=1)
                ###request.raise_for_status()
                break
            except:
                print('request failed')
                time.sleep(1)
        # request = requests.get("https://api.binance.com/api/v3/ticker/price?symbol={}".format(pair))
        currentPrice = request['price']
        return currentPrice

    def returnChartData(self, pair, start, end, period):
        chart_lis = []
        period_str = self.period_dict[period]
        # the pairs are written in poloniex convention with quote_base and therefore have to be reversed
        # binance works with timestamps in miliseconds so our timestamps have to be converted
        start = 1000 * start
        end = 1000 * end
        # split the request in chunks that have in maximum 1000 datapoints
        numParts = math.ceil((end - start) / (period * 1e6))
        print('pair:', pair, 'numparts:', numParts)
        for i in range(numParts):
            subStart = start + i * (end - start) / numParts
            subEnd = start + (i + 1) * (end - start) / numParts
            print('start:', start, 'end:', end, 'subStart:', subStart, 'subEnd:', subEnd)
            url = 'https://api.binance.com/api/v1/klines?symbol={}&interval={}&startTime={}&endTime={}&limit=1000'.format( \
                pair, period_str, int(subStart), int(subEnd))
            for k in range(10):
                try:
                    # request = self.client.get_historical_klines(pair, period, int(subStart),
                    # int(subEnd), 1000)
                    request = requests.get(url, timeout=1)
                    request.raise_for_status()
                    break
                except Exception as Error:
                    print(Error)
                    print('request failed')
                    time.sleep(1)
            # request = requests.get(url)
            chart_lis += request.json()

        # chart_lis is a list of lists, highest in hierarchy are the timestamps
        # chart becomes a list of dictionaries, a dictionary for each timestamp
        chart = []
        for i in chart_lis:
            chart.append({})
            chart[-1]['date'] = int(i[0]) / 1000
            chart[-1]['open'] = float(i[1])
            chart[-1]['high'] = float(i[2])
            chart[-1]['low'] = float(i[3])
            chart[-1]['close'] = float(i[4])
            chart[-1]['volume'] = float(i[5])
            chart[-1]['closeTime'] = i[6]
            chart[-1]['quoteAssetVolume'] = i[7]
            chart[-1]['numberOfTrades'] = i[8]
            chart[-1]['takerBuyBaseAssetVolume'] = i[9]
            chart[-1]['takerBuyQuoteAssetVolume'] = i[10]
        return chart

    def Buy(self, pair, quantity):

        print("buy: ", quantity, pair)
        for k in range(5):
            try:
                request = self.client.create_order(symbol=pair, side='buy', type='MARKET', quantity=quantity,
                                                   recvWindow=5000, newOrderRespType='FULL')
                break
            except Exception as error:
                print(f'request failed, {error}')
                if k >= 5:
                    return "CANCELED",0
                time.sleep(1)


        print(f"the buy request looks like: {request}")
        status = request['status']
        buyPrice = float(request['price'])
        # todo: print the difference between price of our deal vs. ticker price
        return status, buyPrice

    def Sell(self, pair, quantity):
        for k in range(5):
            try:
                request = self.client.create_order(symbol=pair, side='sell', type='MARKET', quantity=quantity,
                                                   recvWindow=5000, newOrderRespType='FULL')
                break
            except:
                print('request failed')
                time.sleep(1)

        print(f"the sell request looks like: {request}")
        # request = requests.get("https://api.binance.com/api/v3/time")
        # serverTime = request.json()['serverTime']
        # request = requests.get(f"https://api.binance.com/api/v3/order?symbol={pair}&side=sell&type=MARKET&quantity={quantity}&recvWindow=5000&timestamp={serverTime}")
        status = request['status']
        sellPrice = float(request['price'])
        return status, sellPrice


    def getBalance(self):
        for k in range(10):
            try:
                request = self.client.get_account(recvWindow=5000)
                break
            except:
                print('request failed')
                time.sleep(1)

        # tempBalances is a list of dictionaries
        tempBalances = request['balances']
        balances = {}
        for dictionary in tempBalances:
            coin = dictionary['asset']
            balance = float(dictionary['free'])
            if float(dictionary['locked']) > 0:
                print(f"{dictionary['locked']} is locked in coin {coin}")
            balances[coin] = balance
        return balances
    def filterBuy(self, pair, quantityBTCstart,closes):
        # minNotional and priceFilter can also requested by get_symbol_info
        for i in range(10):
            try:
                info = self.client.get_symbol_info(symbol=pair)
                break
            except:
                time.sleep(1)
        minNotional=float(info['filters'][3]['minNotional'])
        '''
        for i in range(10):
            try:
                price = float(self.client.get_symbol_ticker(symbol=pair)["price"])
                break
            except:
                time.sleep(1)
        '''
        quantity =  quantityBTCstart / float(closes[pair])
        lotSize = info['filters'][2]
        minQty = float(lotSize['minQty'])
        stepSize = Decimal(lotSize['stepSize'])
        getcontext().prec = 100
        getcontext().rounding = ROUND_DOWN
        quantity = stepSize * Decimal(math.floor(Decimal(quantity) / stepSize))
        quantityBTC=quantity *Decimal(closes[pair])
        print(f"quantity: {quantity} vs minQty: {minQty}")
        print(f"quantityBtc: {quantityBTC} vs minNotional: {minNotional}")
        if quantityBTC < minNotional or quantity < minQty:
            return False
        #quantity = Decimal(int(quantity * 1000000)) / 1000000
        return quantity



    def filterSell(self, pair, quantity,closes):
        for i in range(10):
            try:
                info = self.client.get_symbol_info(symbol=pair)
                break
            except:
                time.sleep(1)
        lotSize = info['filters'][2]
        minQty = float(lotSize['minQty'])
        stepSize = Decimal(lotSize['stepSize'])
        getcontext().prec = 100
        getcontext().rounding = ROUND_DOWN
        quantity = stepSize * Decimal(math.floor(Decimal(quantity) / stepSize))
        minNotional = float(info['filters'][3]['minNotional'])
        '''
        for i in range(10):
            try:
                price = float(self.client.get_symbol_ticker(symbol=pair)["price"])
                break
            except:
                time.sleep(1)
        '''
        quantityBTC=quantity*Decimal(closes[pair])
        print(f"quantity: {quantity} vs minQty: {minQty}")
        print(f"quantityBtc: {quantityBTC} vs minNotional: {minNotional}")
        if quantity < minQty or quantityBTC < minNotional:
            return False
        print("filter: ", quantity, pair)
        return quantity