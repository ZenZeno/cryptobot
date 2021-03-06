import pandas as pd
import datetime as dt

import risk_model as rm
import alpha_model as am
import market_model as mm
import cost_model as cm
import poloniex

class PortfolioConstructor():
    def __init__(self, initial_capital, coins, alpha_models, risk_models, label):
        self.initial_capital = initial_capital
        self.alpha_models = alpha_models
        self.risk_models = risk_models
        self.label = label
        
        #Estimate according to max poloniex fee:
        self.cost_model = cm.CostModel(0.20)

        #initialize database with bitcoin starting capital 
        self.current_portfolio = pd.DataFrame(columns = ['Amount',
                                                         'BTC Value'], 
                                              index = coins)

        self.current_portfolio.loc['BTC', 'Amount'] = initial_capital
        self.current_portfolio.fillna(0, inplace = True)
        self.target_portfolio = self.current_portfolio

    def update(self, market_data):
        price = market_data[self.label]
        [alpha_model.generate_signals(price) 
                for alpha_model in self.alpha_models]
        self.update_signals()
        self.generate_target_portfolio(price)

    def update_signals(self):
        self.signals = [(alpha_model.name, alpha_model.signal) 
                for alpha_model in self.alpha_models]

        self.signals = dict(self.signals)

    def generate_target_portfolio(self):
        pass

class BTC_ETH_MovingAverageCrossover(PortfolioConstructor):
    def __init__(self, initial_capital, short_window, long_window, risk_percentage, label):
        alpha_models = [am.MovingAverageCrossover('MAC 2/10', short_window, long_window)]
        risk_models = [rm.Limiter(risk_percentage)]
        self.short_window = short_window
        self.long_window = long_window

        PortfolioConstructor.__init__(self, initial_capital, ['BTC', 'ETH'], 
                                      alpha_models, risk_models, label)

    def generate_target_portfolio(self, market_price):
        if self.signals['MAC 2/10'] == 1.0:
            #Sell as many BTC as the risk model will allow:
            current_btc = self.current_portfolio.loc['BTC', 'Amount']
            risk_capital = self.risk_models[0].limit * current_btc
            eth_volume = risk_capital / market_price
            self.target_portfolio.loc['ETH', 'Amount'] = self.current_portfolio.loc['ETH', 'Amount'] + eth_volume
            self.target_portfolio.loc['BTC', 'Amount'] = self.current_portfolio.loc['BTC', 'Amount'] - risk_capital
        elif self.signals['MAC 2/10'] == -1.0:
            #Sell all ETH for BTC:
            current_eth = self.current_portfolio.loc['ETH', 'Amount']
            btc_volume = current_eth * market_price
            self.target_portfolio.loc['BTC', 'Amount'] += btc_volume
            self.target_portfolio.loc['ETH', 'Amount'] = 0

        self.target_portfolio.loc['BTC', 'BTC Value'] = self.target_portfolio.loc['BTC', 'Amount']
        self.target_portfolio.loc['ETH', 'BTC Value'] = market_price * self.target_portfolio.loc['ETH', 'Amount']

    def __str__(self):
        output = 'MAC Crossover ' + str(self.short_window) + '/' + str(self.long_window) + '\n'
        output += 'Current Portfolio:\n' + str(self.current_portfolio)

        return output

#TEST SUITE:
if __name__ == '__main__':
    btc_eth_mac_portfolio = BTC_ETH_MovingAverageCrossover(1000, 2, 10, 30, 'weightedAverage')
    
    #fetch test market data from poloniex
    DATE_FMT = '%Y-%m-%d %H:%M:%S'
    start = dt.datetime.strptime('2018-05-01 00:00:00', DATE_FMT)
    end = dt.datetime.strptime('2018-05-30 00:00:00', DATE_FMT)
    api = poloniex.Poloniex('key', 'secret')
    market_data = api.chart_data('BTC_ETH', start.timestamp(), end.timestamp(), 300)

    for i in range(len(market_data)):
        btc_eth_mac_portfolio.update(market_data.iloc[i])
        btc_eth_mac_portfolio.current_portfolio = btc_eth_mac_portfolio.target_portfolio
        print(btc_eth_mac_portfolio)

