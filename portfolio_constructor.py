import pandas as pd
import datetime as dt

import risk_model as rm
import alpha_model as am
import market_model as mm
import cost_model as cm
import poloniex

class PortfolioConstructor():
    def __init__(self, initial_capital, coins, alpha_models, risk_models):
        self.initial_capital = initial_capital
        self.alpha_models = alpha_models
        self.risk_models = risk_models
        
        #Estimate according to max poloniex fee:
        self.cost_model = cm.CostModel(0.20)

        #initialize database with bitcoin starting capital 
        self.current_portfolio = pd.DataFrame(columns = ['Amount',
                                                         'XBT Value'], 
                                              index = coins)

        self.current_portfolio.loc['XBT', 'Amount'] = initial_capital
        self.current_portfolio.fillna(0, inplace = True)
        self.target_portfolio = self.current_portfolio

    def update(self, price):
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
    def __init__(self, initial_capital, short_window, long_window, risk_percentage):
        alpha_models = [am.MovingAverageCrossover('MAC', short_window, long_window)]
        risk_models = [rm.Limiter(risk_percentage)]
        self.short_window = short_window
        self.long_window = long_window

        PortfolioConstructor.__init__(self, initial_capital, ['XBT', 'ETH'], 
                                      alpha_models, risk_models)

    def generate_target_portfolio(self, market_price):
        if self.signals['MAC'] == 1.0:
            #Sell as many BTC as the risk model will allow:
            current_btc = self.current_portfolio.loc['XBT', 'Amount']
            risk_capital = self.risk_models[0].limit * current_btc
            eth_volume = risk_capital / market_price
            self.target_portfolio.loc['ETH', 'Amount'] = self.current_portfolio.loc['ETH', 'Amount'] + eth_volume
            self.target_portfolio.loc['XBT', 'Amount'] = self.current_portfolio.loc['XBT', 'Amount'] - risk_capital
        elif self.signals['MAC'] == -1.0:
            #Sell all ETH for BTC:
            current_eth = self.current_portfolio.loc['ETH', 'Amount']
            btc_volume = current_eth * market_price
            self.target_portfolio.loc['XBT', 'Amount'] += btc_volume
            self.target_portfolio.loc['ETH', 'Amount'] = 0

        self.target_portfolio.loc['XBT', 'XBT Value'] = self.target_portfolio.loc['XBT', 'Amount']
        self.target_portfolio.loc['ETH', 'XBT Value'] = market_price * self.target_portfolio.loc['ETH', 'Amount']

    def __str__(self):
        output = 'MAC Crossover ' + str(self.short_window) + '/' + str(self.long_window) + '\n'
        output += 'Current Portfolio:\n' + str(self.current_portfolio)

        return output

#TEST SUITE:
if __name__ == '__main__':
    mac_portfolio = BTC_ETH_MovingAverageCrossover(1000, 2, 10, 30)
    market = mm.KrakenMarketModel()
    while True:
        market.update('XETHXXBT')
        mac_portfolio.update(market.last('XETHXXBT'))
        print(mac_portfolio.alpha_models)
        print(mac_portfolio)
