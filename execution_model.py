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

    def execute(self):
        if self.time_delta == False:
            for i in range(len(self.market.data)):
                self.tick('weightedAverage')
        elif type(time_delta) == 'int':
            while True:
                self.tick('last')
                dt.time.sleep(time_delta)

    def tick(self, label):
        new_market_data = market.next()

        for alpha_model in portfolio.alpha_models:
            alpha_model.generate_signals(new_market_data, label)
        
if __name__ == '__main__':
    portfolio = pc.BTC_ETH_MovingAverageCrossover(1000)

    #Construct default test market data:
    DATE_FMT = '%Y-%m-%d %H:%M:%S'
    start = dt.datetime.strptime('2018-05-01 00:00:00', DATE_FMT)
    end = dt.datetime.strptime('2018-05-30 00:00:00', DATE_FMT)
    api = poloniex.Poloniex('key', 'secret')
    market = mm.TestMarket(api, 'BTC_ETH', start.timestamp(), end.timestamp())
    
    executive = ExecutionModel(False, market, portfolio)

    executive.tick('weightedAverage')

    print(executive.portfolio.current_portfolio)
    [print(alpha_model.signal()) for alpha_model in executive.portfolio.alpha_models]
