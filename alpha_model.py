import numpy as np
import datetime as dt
import pandas as pd

import poloniex

class AlphaModel():
    def __init__(self, name):
        self.name = name

    def generate_signals(self):
        pass

class MovingAverageCrossover(AlphaModel):
    def __init__(self, name, short_window, long_window, period = 300):
        AlphaModel.__init__(self, name)
        self.short_window = short_window
        self.long_window = long_window
        self.price_history = [] 
        self.short_avg = 0
        self.long_avg = 0
        self.signal = 0.0

    def generate_signals(self, last_price):
        #bring in new market data:
        self.price_history.append(last_price)
        if len(self.price_history) > self.long_window:
            del self.price_history[0]

        #calculate the appropriate rolling averages:
        if len(self.price_history) == self.long_window:
            new_long_avg = sum(self.price_history) / self.long_window
            new_short_avg = sum(self.price_history[(-1 * self.short_window):]) / self.short_window
            
            #generate signal 1.0 if the new short average crossed above the new long average,
            #generate -1.0 if new short average crossed below the new long average
            if new_short_avg > new_long_avg and self.short_avg <= self.long_avg:
                self.signal = 1.0
            elif new_short_avg < new_long_avg and self.short_avg >= self.long_avg:
                self.signal = -1.0
            else:
                self.signal = 0.0

            self.short_avg = new_short_avg
            self.long_avg = new_long_avg 

    def __str__(self):
        output = self.name + ':\n'
        output += str(self.price_history) + '\n' 
        output += 'Short Average: ' + str(self.short_avg) + '\n'
        output += 'Long Average: ' + str(self.long_avg) + '\n'
        output += str(self.signal)
        
        return output

#TEST SUITE:
if __name__ == '__main__':
    #fetch test market data from poloniex
    DATE_FMT = '%Y-%m-%d %H:%M:%S'
    start = dt.datetime.strptime('2018-05-01 00:00:00', DATE_FMT)
    end = dt.datetime.strptime('2018-05-30 00:00:00', DATE_FMT)
    api = poloniex.Poloniex('key', 'secret')
    market_data = api.chart_data('BTC_ETH', start.timestamp(), end.timestamp(), 300)

    #simulate signal generation for test data
    mac_strategy = MovingAverageCrossover('MAC 2/10', 2, 10)
    for i in range(len(market_data)):
        mac_strategy.generate_signals(market_data.iloc[i]['weightedAverage'])
        print(mac_strategy)
