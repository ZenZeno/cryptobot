import pandas as pd
import time

class Portfolio:
    def __init__(self, initial_capital):
        self.positions = pd.DataFrame({'capital' : initial_capital, 
                                       'trade volume' : 0, 'price': 0,
                                       'holdings' : 0, 'value' : 0}, 
                                        index = [0])
        print(self.positions)

    def get_capital(self):
        return self.positions.iloc[-1]['capital']
    
    def get_holdings(self):
        return self.positions.iloc[-1]['holdings']
    
    def get_total(self):
        return self.positions.iloc[-1]['total']

    def buy_order(self, volume, price, date, test):
            capital = self.positions.iloc[-1]['capital'] - (volume * price)
            holdings = self.positions.iloc[-1]['holdings'] + volume
            value = holdings * price
            
            data = {
                'capital' : capital,
                'trade volume' : volume, 'price' : price,
                'holdings' : holdings, 'value' : value,
                'total': value + capital
            }

            self.positions = self.positions.append(pd.DataFrame(data, index = [date]))

    def sell_order(self, volume, price, date, test):
            capital = self.positions.iloc[-1]['capital'] + (volume * price)
            holdings = self.positions.iloc[-1]['holdings'] - volume
            value = holdings * price
            
            data = {
                'capital' : capital,
                'trade volume' : volume, 'price' : price,
                'holdings' : holdings, 'value' : value,
                'total' : value + capital
            }
            
            self.positions = self.positions.append(pd.DataFrame(data, index = [date]))

