#Python Libraries:
import pandas
import datetime

#local includes:
import poloniex

class Market():
    def __init__(self, pair = 'BTC_ETH', period = 300):
        self.api = poloniex.Poloniex('key', 'secret')
        self.period = period
        self.pair = pair
        self.ticker = pandas.DataFrame()

class LiveMarket(Market):
    def __init__(self, pair = 'BTC_ETH', period = 300):
        Market.__init__(self, pair, period)
        self.ticker = self.api.returnTicker(self.pair)     

    def update(self):
        self.ticker = pandas.concat([self.ticker, self.api.returnTicker(self.pair)])
    
    def calculate_moving_avg(self, short_window, long_window):
        self.ticker['shortAvg'] = self.ticker['last'].rolling(short_window).mean()
        self.ticker['longAvg'] = self.ticker['last'].rolling(long_window).mean()

class TestMarket(Market):
    def __init__(self, pair = 'BTC_ETH', start = '2018-05-01 00:00:00', end = '2018-05-31 00:00:00', period = 300):
        Market.__init__(self, pair, period)
        self.start = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S') 
        self.end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')  
        self.ticker = self.api.returnChartData(self.pair, self.start.timestamp(), self.end.timestamp(), self.period)

    def calculate_moving_avg(self, short_window, long_window):
        self.ticker['shortAvg'] = self.ticker['weightedAverage'].rolling(short_window).mean()
        self.ticker['longAvg'] = self.ticker['weightedAverage'].rolling(long_window).mean()
