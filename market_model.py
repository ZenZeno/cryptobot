import datetime as dt
import pandas as pd

import poloniex

class MarketModel():
    def __init__(self, api, pair):
        self.pair = pair
        self.api = api
        
        #self.tick = -1 so that the first time next() is called, tick will equal 0
        self.tick = -1

    def next(self):
        pass

class TestMarket(MarketModel):
    def __init__(self, api, pair, start, end, period = 300):
        MarketModel.__init__(self, api, pair)
        self.start = dt.datetime.fromtimestamp(start)
        self.end = dt.datetime.fromtimestamp(end)
        self.data = self.api.chart_data(pair, start, end, period)
        
    def next(self):
        self.tick += 1
        return self.data.iloc[self.tick]
    
    def __str__(self):
        DATE_FMT = '%Y-%m-%d %H:%M:%S'

        output = ('Test Market from ' + dt.datetime.strftime(self.start, DATE_FMT) 
                + ' to ' + dt.datetime.strftime(self.end, DATE_FMT))

        return output

class LiveMarket(MarketModel):
    def __init__(self, api, pair):
        MarketModel.__init__(self, api, pair)
        self.data = pd.DataFrame()

    def next(self):
        self.tick += 1
        new_row = self.api.ticker(self.pair)
        self.data = self.data.append(new_row)

        return new_row

if __name__ == '__main__':
    DATE_FMT = '%Y-%m-%d %H:%M:%S'
    start = dt.datetime.strptime('2018-05-01 00:00:00', DATE_FMT)
    end = dt.datetime.strptime('2018-05-30 00:00:00', DATE_FMT)
    api = poloniex.Poloniex('key', 'secret')

    test_market = TestMarket(api, 'BTC_ETH', start.timestamp(), end.timestamp())

    print(test_market.data)

    for i in range(20):
        print(test_market.next())

    live_market = LiveMarket(api, 'BTC_ETH')

    for i in range(20):
        print(live_market.next())
        print(live_market.data)
