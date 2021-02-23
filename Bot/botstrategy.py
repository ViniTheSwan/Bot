from botindicators import BotIndicators
from bottrade import BotTrade
import time
from colorit import color_back, color_front, bold

# from botlog import BotLog


class BotStrategy(object):
    def __init__(self, period, log, api, checker, stopLoss=0, startBalance=100):
        self.highs = {}
        self.lows = {}
        self.closes = {}
        self.dates = []
        self.volumes = {}
        self.MFIs = {}
        self.MACD = {}
        self.MovingAverage = {}
        self.output = log
        self.api = api
        self.fee = {}
        self.fee['BTC'] = self.api.getFee('ETHBTC')
        self.fee['BNB'] = self.api.getFee('BNBBTC')
        self.fee['USDT'] = self.api.getFee('BTCUSDT')
        self.pairs = checker.pairs

        self.coins = checker.coins
        self.indicators = BotIndicators(period, self.pairs)
        # unused, but find application
        self.stopLoss = stopLoss

        # self.balance = {i: 0 for i in checker.coins} # disable (it has to be in the tick method below)

        # setting start values for USDT
        # self.balance['USDT'] = startBalance
        self.oldValue = 0
        self.ovrValue = 0

        self.MFIs = {}
        self.MovingAverage = {}
        self.MFI = None

        self.period = period
        self.counter = 0

    def tick(self, history, timestamp, initialize_live):

        # are all dictionaries, with timestamp as 1st level key and pair becomes 2nd level key (nested dictionary)
        self.highs[timestamp] = {}
        self.lows[timestamp] = {}
        self.closes[timestamp] = {}
        self.dates.append(timestamp)
        self.volumes[timestamp] = {}
        self.MFIs[timestamp] = {}
        self.MovingAverage[timestamp] = {}
        self.MACD[timestamp] = {}

        for pair in self.pairs:
            self.highs[timestamp][pair] = history[timestamp][pair]['high']
            self.lows[timestamp][pair] = history[timestamp][pair]['low']
            self.closes[timestamp][pair] = history[timestamp][pair]['close']
            self.volumes[timestamp][pair] = history[timestamp][pair]['volume']
            self.MovingAverage[timestamp][pair] = self.indicators.movingAverage(closes=self.closes, dates=self.dates,
                                                                                pair=pair, length=5)

            self.MFI = self.indicators.moneyFlowIndex(period=self.period, dates=self.dates,
                                                      highs=self.highs, lows=self.lows,
                                                      closes=self.closes,
                                                      volumes=self.volumes, pair=pair)
            self.MFIs[timestamp][pair] = self.MFI

            self.MACD[timestamp][pair] = self.indicators.MACD_Histogram(period=self.period, dates=self.dates,
                                                                        closes=self.closes, pair=pair)
        if not initialize_live:
            self.evaluatePositions(timestamp)
            self.giveInfo()

    def evaluatePositions(self, timestamp):
        # self.balances is a dictionary with balance for each coin
        self.balances = self.api.getBalance()
        BuyOptions = []
        SellOptions = []
        list_of_trades = []
        notTraded = []
        # latest overall value becomes old value

        self.oldValue = self.ovrValue
        self.ovrValue = 0

        # loops through pairs and checks if MFI indicates a buy or sell option
        for pair in self.pairs:
            if self.MFIs[timestamp][pair]:
                if self.MFIs[timestamp][pair] < 30:
                    BuyOptions.append((pair, self.MFIs[timestamp][pair]))
                if self.MFIs[timestamp][pair] > 70:
                    SellOptions.append(pair)

            # buy if MACD overtakes MACD Signal Line, sell if MACD gets overtaken by MACD Signal Line
            if len(self.MACD[timestamp][pair]) > int(86400 / self.period):
                if (0 > self.MACD[timestamp][pair][-2]) and (self.MACD[timestamp][pair][-1] > 0):
                    # BuyOptions.append(pair)
                    print("According to MACD buy!", self.MACD[timestamp][pair][-2], self.MACD[timestamp][pair][-1],
                          pair)
                '''
                if (0 < self.MACD[timestamp][pair][-2]) and (self.MACD[timestamp][pair][-1] < 0):
                    # SellOptions.append(pair)
                    SellOptions.append(pair)
                '''
        # sorts the definitive buy options starting with lowest MFI and takes the 5 with lowest MFI
        # todo: used for MFI, improve by spliting the money to different coins, somehow a voting system by different indicators
        definitiveBuyOptions = sorted(BuyOptions, key=lambda tup: tup[1])[:5]
        # definitiveBuyOptions = BuyOptions
        ## definitiveSellOptions.append(sorted(BuyOptions,key=lambda tup:tup[1])[-5:])
        ## definitiveSellOptions=sorted(BuyOptions,key=lambda tup:tup[1])

        # takes all Sell options as definitive (can be further improved)
        definitiveSellOptions = SellOptions

        print('MFIs:', self.MFIs[timestamp])
        counter = 0
        #########################################SELL###################################
        for sell in definitiveSellOptions:
            if sell ==  "BTCUSDT":
                continue
            other = sell[:-3] #other currency
            BTC = sell[-3:] #Bitcoin
            quantityTemp = self.balances[other]
            print(f"sell {sell}")
            quantity = self.api.filterSell(quantity=quantityTemp, pair=sell,closes=self.closes[timestamp])
            if quantity:
                counter += 1
                status, sellPrice = self.api.Sell(pair=sell, quantity=quantity)
                if status == "FILLED":
                    list_of_trades.append(status)
                    print(f'sold {sell} at {sellPrice}')
                else:
                    notTraded.append(status, pair)
                    print(status, pair)
            else:
                print(f"Would have sold but no coins of this currency, {sell}")

        # if there is any buy option, only the best option should be taken


        #########################Buy###################################
        print(f"Buy options look like (first pair, second MFI): {definitiveBuyOptions} ")
        for i, buy in enumerate(definitiveBuyOptions):
            number_of_buys = len(definitiveBuyOptions)
            fraction = 1 / 5   # applied 10.September
            if buy[0] == "BTCUSDT":
                continue
            buy = buy[0]
            other = buy[:-3]  # other currency
            BTC = buy[-3:]  # Bitcoin
            quantityTemp = self.balances[BTC] * fraction

            if "BNB" not in [BTC, other]:
                quantityTemp = quantityTemp * (1 - self.fee['BTC'])
            else:
                quantityTemp = quantityTemp * (1 - self.fee['BNB'])

            print(f"quantityTemp is: {quantityTemp}")
            quantity = self.api.filterBuy(quantityBTCstart=quantityTemp, pair=buy,closes=self.closes[timestamp])
            if quantity:
                counter += 1
                status, buyPrice = self.api.Buy(pair=buy, quantity=quantity)
                if status == "FILLED":
                    list_of_trades.append(status)
                    print(f'bought {buy} at {buyPrice}')
                else:
                    notTraded.append(status, buy)
                    print(status, buy)
            else:
                print(f"Would have bought but no coins (BTC (or USDT)) to buy this currency, {buy}")

        # evaluate the portfolio value called overall

        if len(list_of_trades) == counter:
            self.balances = self.api.getBalance()
        else:
            print(f'{notTraded} is the list of not Traded pairs')
            time.sleep(10)
            print(f'{notTraded} is the list of not Traded pairs after additional 10 seconds, however the balance gets estimated now!')
            self.balances = self.api.getBalance()

        for pair in self.pairs:
            if pair == 'BTCUSDT':
                other = 'USDT'
            else:
                other = pair[:-3]  # other currency

            self.ovrValue += self.balances[other] * self.closes[timestamp][pair] * self.closes[timestamp]['BTCUSDT']

        self.ovrValue += self.balances['USDT']
        self.ovrValue += self.balances['BTC'] * self.closes[timestamp]['BTCUSDT']
        print('USDT:', self.balances['USDT'], 'BTC:', self.balances['BTC'], 'overall value:', self.ovrValue)
        self.counter += self.period

    def giveInfo(self):
        Yield = self.ovrValue - self.oldValue
        if Yield > 1:
            print("The overall Value is:" + str(self.ovrValue) + color_front("The yield is: " + str(Yield), 0,153,76))
        elif Yield > 0:
            print("The overall Value is:" + str(self.ovrValue) + color_front("The yield is: " + str(Yield), 0,255,0))
        elif Yield < -1:
            print("The overall Value is:" + str(self.ovrValue) + color_front("The yield is: " + str(Yield), 255,0,0))
        else:
            print("The overall Value is:" + str(self.ovrValue) + color_front("The yield is: " + str(Yield), 255,128,0))

        print("{} days passed".format(self.counter / 86400))
