import market
import portfolio
import pandas as pd
import numpy as np

class Strategy():
    def __init__(self, market, initial_capital = 1000, decision_length = 1):
        self.market = market
        self.decision_length = decision_length
        self.portfolio = portfolio.Portfolio(initial_capital)
        self.decision_frame = pd.DataFrame()

    def tick(self):
        self.market.update()
        self.decision_frame = self.market.tail(self.decision_length)
        self.trade()
        self.display()

    def trade(self, test = False):
        if test:
            price = self.decision_frame.iloc[-1]['weightedAverage']
        else:
            price = self.decision_frame.iloc[-1]['last']

        #buy or sell all, randomly:
        signal = np.random.randint(-1,2)
        if signal == 1 and self.portfolio.get_capital() > 0:
            volume = self.portfolio.get_capital() / price
            self.portfolio.buy_order(volume, price, test)
        elif signal == -1:
            volume = self.portfolio.get_holdings()
            self.portfolio.sell_order(volume, price, test)

    def display(self):
        print('\033c')
        print(self.market.ticker.tail(20))
        print()
        print(self.portfolio.positions.tail(20))
    
    def simulate(self, short_window, long_window):
        self.market.calculate_moving_avg(short_window, long_window)

        print('Simulating market strategy ')

        for i in range(len(self.market.ticker)):
            self.decision_frame = self.market.ticker.iloc[i:i+self.decision_length]
            self.trade(True)

        print(self.portfolio.positions.tail())
        print()

        #calculate returns for simply holding initial purchase for the period:
        holding_volume = self.portfolio.positions.iloc[0]['capital'] / self.market.ticker.iloc[0]['weightedAverage']
        end_value = holding_volume * self.market.ticker.iloc[-1]['weightedAverage']

        print(end_value)
