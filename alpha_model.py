import numpy as np
import datetime as dt
import pandas as pd

import poloniex

STR_FMT = '%Y-%m-%d %H:%M:%S'

class AlphaModel():
    def __init__(self):
        pass

    def generate_signals(self):
        pass

class MovingAverageCrossover(AlphaModel):
    def __init__(self, short_window, long_window, period = 300):
        self.short_window = short_window
        self.long_window = long_window
        self.market_data = pd.DataFrame()

    def generate_signals(self, market_data, label):
        #bring in new market data:
        self.market_data = self.market_data.append(market_data)

        #calculate the appropriate rolling averages:
        self.market_data['short avg'] = self.market_data[label].rolling(self.short_window).mean()
        self.market_data['long avg'] = self.market_data[label].rolling(self.long_window).mean()

        #generate a 1 when short average crosses above long average, -1 when it crosses below
        self.market_data['signal'] = np.where(self.market_data['short avg'] > self.market_data['long avg'], 
                1.0, -1.0)
        self.market_data['signal'] = np.sign(self.market_data['signal'].diff())

        #return no signal when there is not enough data
        self.market_data.loc[0:self.long_window, 'signal'] = 0.0

    def data(self): 
        return self.market_data

    def signal(self):
        return self.market_data.iloc[-1].loc['signal']

if __name__ == '__main__':
    pd.set_option('display.width', None)

    #fetch test market data from poloniex
    start = dt.datetime.strptime('2018-05-01 00:00:00', STR_FMT)
    end = dt.datetime.strptime('2018-05-30 00:00:00', STR_FMT)
    api = poloniex.Poloniex('key', 'secret')
    market_data = api.chart_data('BTC_ETH', start.timestamp(), end.timestamp(), 300)

    #generate signals over the weighted average of test market data
    mac_strategy = MovingAverageCrossover(2, 10)
    mac_strategy.generate_signals(market_data, 'weightedAverage')
    
    print(mac_strategy.data())
    print(mac_strategy.signal())
