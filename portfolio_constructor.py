import pandas as pd
import datetime as dt

import risk_model as rm
import alpha_model as am

class PortfolioConstructor():
    def __init__(self, initial_capital, coins, alpha_models, risk_models):
        self.alpha_models = alpha_models
        self.risk_models = risk_models
        
        #initialize database with bitcoin starting capital 
        self.current_portfolio = pd.DataFrame(columns = ['Type', 'Amount','BTC Value'], index = coins)
        self.current_portfolio.loc['BTC', 'Amount'] = initial_capital
        self.current_portfolio.loc['BTC', 'Type'] = 'Long'
        self.target_portfolio = self.current_portfolio

    def generate_target_portfolio():
        pass

class BTC_ETH_MovingAverageCrossover(PortfolioConstructor):
    def __init__(self, initial_capital):
        alpha_models = [am.MovingAverageCrossover(2, 10)]
        risk_models = [rm.Limiter(3)]

        PortfolioConstructor.__init__(self, initial_capital, ['BTC', 'ETH'], alpha_models, risk_models)

    def generate_target_portfolio(self):
        pass

if __name__ == '__main__':
    mac_2_10 = am.MovingAverageCrossover(2, 10)
    limit = rm.Limiter(3)

    btc_portfolio_constructor = PortfolioConstructor(100, ['BTC', 'ETH'], [mac_2_10], [limit])

    print(btc_portfolio_constructor.current_portfolio)

