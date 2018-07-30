import pandas 

import kraken
import poloniex

class Portfolio():
    def __init__(self, name, market, 
                 alpha_models, risk_models, trading_algorithm):

        self.name = name
        self.market = market
        self.alpha_models = alpha_models
        self.risk_models = risk_models
        self.generate_target = trading_algorithm

    def update_signals(self):
        raise NotImplementedError

class PoloniexTestPortfolio(Portfolio):
    def __init__(self, name, pairs, 
                 start, end, period, 
                 alpha_models, risk_models, trading_algorithm):

        self.market = poloniex.TestMarket(pairs, start, end, period)
        Portfolio.__init__(self, name, self.market, alpha_models, risk_models, trading_algorithm)

    def update_signals(self):
        print('here')
