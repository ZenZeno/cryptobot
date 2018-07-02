import market
import portfolio
import pandas as pd
import numpy as np
import os

class Strategy():
    def __init__(self, market):
        self.market = market
        self.portfolio = portfolio.Portfolio(0.0028)

    def trade(self):
        self.market.update()
        self.market.calculate_moving_avg(5, 15)
        
        if len(self.market.ticker) > 15:
            decision_frame = self.market.ticker.tail(15)
            print(decision_frame.iloc[-1]['lowestAsk'])

            if (decision_frame.iloc[-1]['shortAvg'] > decision_frame.iloc[-1]['longAvg'] 
                    and decision_frame.iloc[-2]['shortAvg'] <= decision_frame.iloc[-2]['longAvg']):
                self.portfolio.buy_order(0.01, decision_frame.iloc[-1]['lowestAsk'])

    def display(self):
        print('\033c')
        print(self.market.ticker.tail(20))
        print()
        print(self.portfolio.positions.tail(20))
    
    def simulate(self, short_window, long_window):
        self.market.calculate_moving_avg(short_window, long_window)

        print('Simulating market strategy ')

        for i in range(len(self.market.ticker) - 2):
            decision_frame = self.market.ticker.iloc[i:i+2]

        #TODO: refactor this to use trade() function:
            if (decision_frame.iloc[-1]['shortAvg'] > decision_frame.iloc[-1]['longAvg'] 
                    and decision_frame.iloc[-2]['shortAvg'] <= decision_frame.iloc[-2]['longAvg']):
                volume = self.portfolio.get_capital() / decision_frame.iloc[-1]['weightedAverage'] 
                self.portfolio.buy_order(volume, decision_frame.iloc[-1]['weightedAverage'])
            elif (decision_frame.iloc[-1]['shortAvg'] < decision_frame.iloc[-1]['longAvg'] 
                    and decision_frame.iloc[-2]['shortAvg'] >= decision_frame.iloc[-2]['longAvg']
                    and decision_frame.iloc[-1]['weightedAverage'] > self.portfolio.positions.iloc[-1]['price']):
                volume = self.portfolio.get_holdings()
                self.portfolio.sell_order(volume, decision_frame.iloc[-1]['weightedAverage'])

        print(self.portfolio.positions.tail())

        #calculate returns for simply holding initial purchase for the period:
        holding_volume = self.portfolio.positions.iloc[0]['capital'] / self.market.ticker.iloc[0]['weightedAverage']
        end_value = holding_volume * self.market.ticker.iloc[-1]['weightedAverage']

        print(end_value)
