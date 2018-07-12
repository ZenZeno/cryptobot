import pandas as pd
import datetime as dt

import risk_model as rm
import alpha_model as am
import market_model as mm
import poloniex

class PortfolioConstructor():
    def __init__(self, initial_capital, coins, alpha_models, risk_models):
        self.alpha_models = alpha_models
        self.risk_models = risk_models
        
        #initialize database with bitcoin starting capital 
        self.current_portfolio = pd.DataFrame(columns = ['Type', 
                                                         'Amount',
                                                         'BTC Value'], 
                                              index = coins)

        self.current_portfolio.loc['BTC', 'Amount'] = initial_capital
        self.current_portfolio.loc['BTC', 'Type'] = 'Long'
        self.target_portfolio = self.current_portfolio

    def update(self, market_data, label):
        [alpha_model.generate_signals(market_data, label) 
                for alpha_model in self.alpha_models]
        self.update_signals()
        self.generate_target_portfolio()

    def update_signals(self):
        self.signals = [(alpha_model.name, alpha_model.signal()) 
                for alpha_model in self.alpha_models]

        self.signals = dict(self.signals)

    def generate_target_portfolio(self):
        pass

class BTC_ETH_MovingAverageCrossover(PortfolioConstructor):
    def __init__(self, initial_capital):
        alpha_models = [am.MovingAverageCrossover('MAC 2/10', 2, 10)]
        risk_models = [rm.Limiter(3)]

        PortfolioConstructor.__init__(self, initial_capital, ['BTC', 'ETH'], 
                                      alpha_models, risk_models)
    def generate_taget_portfolio:
        pass

#TEST SUITE:
if __name__ == '__main__':
    mac_2_10 = am.MovingAverageCrossover('MAC 2/10', 2, 10)
    limit = rm.Limiter(3)

    btc_portfolio_constructor = PortfolioConstructor(100, ['BTC', 'ETH'],
                                                     [mac_2_10], [limit])

    print(btc_portfolio_constructor.current_portfolio)


    btc_eth_mac_portfolio = BTC_ETH_MovingAverageCrossover(1000)
    
    #fetch test market data from poloniex
    DATE_FMT = '%Y-%m-%d %H:%M:%S'
    start = dt.datetime.strptime('2018-05-01 00:00:00', DATE_FMT)
    end = dt.datetime.strptime('2018-05-30 00:00:00', DATE_FMT)
    api = poloniex.Poloniex('key', 'secret')
    market_data = api.chart_data('BTC_ETH', start.timestamp(), end.timestamp(), 300)

    for i in range(len(market_data)):
        btc_eth_mac_portfolio.update(market_data.iloc[i], 'weightedAverage')
        print(btc_eth_mac_portfolio.signals)
