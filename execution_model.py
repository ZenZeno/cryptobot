import datetime as dt

import portfolio_constructor as pc
import alpha_model as am
import risk_model as rm
import market_model as mm
import poloniex

class ExecutionModel():
    def __init__(self, time_delta, market, portfolio):
        self.time_delta = time_delta
        self.market = market
        self.portfolio = portfolio
        self.performance = 0

    def execute(self, verbose = False):
        if self.time_delta == False:
            for i in range(len(self.market.data)):
                self.tick('weightedAverage')
                if verbose:
                    self.calculate_performance('weightedAverage')
                    self.display()

        elif type(time_delta) == 'int':
            while True:
                self.tick('last')
                dt.time.sleep(time_delta)
                if verbose:
                    self.calculate_performance('last')
                    self.display()

    def tick(self, label):
        new_market_data = self.market.next()
        
        self.portfolio.update(new_market_data)
        self.portfolio.current_portfoio = self.portfolio.target_portfolio

    def calculate_performance(self, label):
        market_open = self.market.data.iloc[0].loc[label]
        market_close = self.market.data.iloc[-1].loc[label]
        self.market_return = (market_close - market_open) / market_open

        strategy_open = self.portfolio.initial_capital
        strategy_close = self.portfolio.current_portfolio['BTC Value'].sum()
        self.strategy_return = (strategy_close - strategy_open) / strategy_open

    def display(self):
        output_str = '\033c' + str(self.market) + '\n' + str(self.portfolio) + '\n'
        output_str += 'Target Portfolio\n' + str(self.portfolio.target_portfolio) + '\n'
        output_str += 'Market Performance\n' + str(self.market_return) + '\n'
        output_str += 'Strategy Performance\n' + str(self.strategy_return) 

        print(output_str)

if __name__ == '__main__':
    portfolio = pc.BTC_ETH_MovingAverageCrossover(1000, 2, 10, 30, 'weightedAverage')

    #Construct default test market data:
    DATE_FMT = '%Y-%m-%d %H:%M:%S'
    start = dt.datetime.strptime('2018-05-01 00:00:00', DATE_FMT)
    end = dt.datetime.strptime('2018-05-30 00:00:00', DATE_FMT)
    api = poloniex.Poloniex('key', 'secret')
    market = mm.TestMarket(api, 'BTC_ETH', start.timestamp(), end.timestamp())
    
    executive = ExecutionModel(False, market, portfolio)

    executive.execute()
