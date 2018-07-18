import datetime as dt
import time

import portfolio_constructor as pc
import alpha_model as am
import risk_model as rm
import market_model as mm
import kraken as kr

class ExecutionModel():
    def __init__(self, time_delta):
        self.time_delta = time_delta
        self.market = mm.KrakenMarketModel()
        self.api = kr.Kraken.from_key_file('keys')
        self.portfolio = pc.BTC_ETH_MovingAverageCrossover(1000,  2, 10, 3, 'last')
        self.performance = 0

    def execute(self, verbose = False):
        while True:
            self.tick()
            self.display()
            time.sleep(self.time_delta)

    def tick(self):
        self.market.update('ETHXBT') 
        self.portfolio.update(self.market.last('XETHXXBT'))
        self.portfolio.current_portfoio = self.portfolio.target_portfolio

    def calculate_performance(self, label):
        market_open = self.market.data.iloc[0].loc[label]
        market_close = self.market.data.iloc[-1].loc[label]
        self.market_return = (market_close - market_open) / market_open

        strategy_open = self.portfolio.initial_capital
        strategy_close = self.portfolio.current_portfolio['BTC Value'].sum()
        self.strategy_return = (strategy_close - strategy_open) / strategy_open

    def display(self):
        output_str = '\033c' +  str(self.market.last('XETHXXBT')) + '\n' +  str(self.portfolio) + '\n'
        output_str += 'Target Portfolio\n' + str(self.portfolio.target_portfolio) + '\n'

        print(output_str)

if __name__ == '__main__':
    executive = ExecutionModel(1)

    executive.execute()
