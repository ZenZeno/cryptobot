import market
import portfolio
import pandas as pd
import numpy as np

class Strategy():
    def __init__(self, market):
        self.market = market
        self.portfolio = portfolio.Portfolio(10000)

    def generate_signals(self):
        self.market.ticker['signals'] = np.sign(np.random.randn(len(self.market.ticker))) 
        self.market.ticker['signals'] = np.sign(self.market.ticker['signals'].diff())

    def trade(self):
        order_number = 1

        for row, data in self.market.ticker.iterrows():
            if data['signals'] == 1.0:
                self.portfolio.buy_order(order_number, 1, data['weightedAverage'])
                order_number += 1
            elif data['signals'] == -1.0:
                self.portfolio.sell_order(order_number, 1, data['weightedAverage'])
                order_number += 1

        print(self.portfolio.positions)
