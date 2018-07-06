import market
import portfolio
import pandas as pd
import numpy as np
import time

class Strategy():
    def __init__(self, market, initial_capital = 1000, decision_length = 1):
        self.market = market
        self.decision_length = decision_length
        self.portfolio = portfolio.Portfolio(initial_capital)
        self.decision_frame = pd.DataFrame()

    def tick(self):
        #prepare new market data for trading:
        self.market.update()
        self.decision_frame = self.market.ticker.tail(self.decision_length)
        
        #trade, if we have enough data to decide on strategy:
        if len(decision_frame) == decision_length:
            self.trade()

        self.display()

    def trade(self, test = False):
        if test:
            price = self.decision_frame.iloc[-1]['weightedAverage']
        else:
            price = self.decision_frame.iloc[-1]['last']

    
        #buy or sell all, randomly:
        signal = np.random.randint(-1,2)
        date = self.decision_frame.iloc[-1].name #.iloc[-1].name == index of last row

        if signal == 1 and self.portfolio.get_capital() > 0:
            volume = self.portfolio.get_capital() / price
            self.portfolio.buy_order(volume, price, date, test)
        elif signal == -1:
            volume = self.portfolio.get_holdings()
            self.portfolio.sell_order(volume, price, date, test)

    def display(self):
        print('\033c')
        print(self.market.ticker.tail(20))
        print()
        print(self.portfolio.positions.tail(20))
    
    def simulate(self, save = False):
        print('Simulating market strategy')

        #step through historic market data:
        for i in range(len(self.market.ticker)):
            self.decision_frame = self.market.ticker.iloc[i:i+self.decision_length]
            self.trade(True)

        if save:
            self.save_state()
        
        #calculate returns for simply holding initial purchase for the period:
        holding_volume = self.portfolio.positions.iloc[0]['capital'] / self.market.ticker.iloc[0]['weightedAverage']
        end_value = holding_volume * self.market.ticker.iloc[-1]['weightedAverage']

        #return percent difference from simple holding value:
        percent_diff = (self.portfolio.get_total() - end_value) / end_value
        print(percent_diff)

        return percent_diff

    def save_state(self):
        filename = time.strftime('%Y-%m-%d-%M-%S') 
        state = self.market.ticker.append(self.portfolio.positions)
        state.to_csv(filename)

    def get_stats(self, label):
        percent_gain = (self.portfolio.get_total() 
                      - self.portfolio.initial_capital) / self.portfolio.initial_capital
        market_percent_diff = (self.market.ticker.iloc[-1][label] 
                    - self.market.ticker.iloc[0][label]) / self.market.ticker.iloc[0][label]

        data = {'strategy return (%)' : percent_gain,
                'start': self.market.start,
                'end': self.market.end,
                'market performance (%)': market_percent_diff,
                'strategy relative performance (%)' : percent_gain - market_percent_diff}
        order = ['start', 'end', 'market performance (%)', 
                'strategy return (%)', 'strategy relative performance (%)']

        data_frame = pd.DataFrame(data, index = [0])
        data_frame = data_frame[order]

        return data_frame
