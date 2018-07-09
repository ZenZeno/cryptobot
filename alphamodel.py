import numpy as np
import datetime as dt
import pandas as pd

import poloniex
    
pd.set_option('display.width', None)

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
        self.tick = 0

    def generate_signals(self, market_data, label):
        #calculate the appropriate rolling averages:
        market_data['short avg'] = market_data[label].rolling(self.short_window).mean()
        market_data['long avg'] = market_data[label].rolling(self.long_window).mean()

        #generate a 1 when short average crosses above long average, -1 when it crosses below
        market_data['signal'] = np.where(market_data['short avg'] > market_data['long avg'], 1.0, -1.0)
        market_data['signal'] = np.sign(market_data['signal'].diff())

        #return no signal when there is not enough data
        market_data.loc[0:self.long_window, 'signal'] = 0.0
        return market_data['signal']

if __name__ == '__main__':
    #fetch test market data from poloniex
    start = dt.datetime.strptime('2018-05-01 00:00:00', STR_FMT)
    end = dt.datetime.strptime('2018-05-30 00:00:00', STR_FMT)
    api = poloniex.Poloniex('key', 'secret')
    market_data = api.chart_data('BTC_ETH', start.timestamp(), end.timestamp(), 300)

    #generate signals over the weighted average of test market data
    mac_strategy = MovingAverageCrossover(2, 10)
    signals = mac_strategy.generate_signals(market_data, 'weightedAverage')
    
    print(market_data)
