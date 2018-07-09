import numpy as np

import poloniex
import market

class AlphaModel():
    def __init__(self):
        pass

    def generate_signals(self):
        pass

class MovingAverageCrossover(AlphaModel):
    def __init__(self, short_window, long_window, period = 300):
        market_data['short avg'] = market_data[label].rolling(self.short_window).mean()
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, market_data, label):
        #calculate the appropriate rolling averages:
        market_data['short avg'] = market_data[label].rolling(self.short_window).mean()
        market_data['long avg'] = market_data[label].rolling(self.long_window).mean()

        market_data['signal'] = np.where(market_data['short avg'] > market_data['long avg'], 1.0, -1,0)
        market_data['signal'] = np.sign(market_data['signal'].diff())

        return market_data

if __name__ = '__main__':
    api = poloniex.Poloniex('key', 'secret')
    market_data = api.returnChartData('')
    mac_strategy = MovingAverageCrossover(2, 10)

        
