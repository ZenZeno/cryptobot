import market
import portfolio
import pandas as pd
import numpy as np

class Strategy():
    def __init__(self, market):
        self.market = market
        self.portfolio = portfolio.Portfolio(10000)

    def generate_signals(self):
        self.market.calculate_moving_avg(10,20)

        #generate signal of 1 when short average crosses above long average,
        #-1 when short average crosses below long average
        self.market.ticker['signals'] = np.where(
                self.market.ticker['shortAvg'] > self.market.ticker['longAvg'], 1.0,-1.0) 
        self.market.ticker['signals'] = np.sign(self.market.ticker['signals'].diff())
            
    def trade(self):
        order_number = 1

        for row, data in self.market.ticker.iterrows():
            if data['signals'] == 1.0:
                self.portfolio.buy_order(order_number, 1, data['weightedAverage'])
                order_number += 1
            elif data['signals'] == -1.0 and data['weightedAverage'] > self.portfolio.positions.iloc[-1]['price']:
                volume = self.portfolio.positions.iloc[-1]['holdings']
                self.portfolio.sell_order(order_number, volume, data['weightedAverage'])
                order_number += 1

        print(self.portfolio.positions)
