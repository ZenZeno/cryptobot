import pandas as pd
from subprocess import Popen, PIPE
import os

class Portfolio:
    def __init__(self, initial_capital):
        self.positions = pd.DataFrame({'capital' : initial_capital, 
                                       'trade volume' : 0, 'price': 0,
                                       'holdings' : 0, 'value' : 0}, 
                                        index = pd.RangeIndex(0, 1))

    def buy_order(self, order_number, volume, price, mode):
        if mode == 'test':
            capital = self.positions.iloc[-1]['capital'] - (volume * price)
            holdings = self.positions.iloc[-1]['holdings'] + volume
            value = holdings * price
            
            data = {
                'order number' : order_number,
                'capital' : capital,
                'trade volume' : volume, 'price' : price,
                'holdings' : holdings, 'value' : value 
            }

            self.positions = self.positions.append(pd.DataFrame(data, index = [0]), ignore_index = True)

