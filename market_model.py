import datetime as dt
import pandas as pd
import kraken as kr

class MarketModel():
    def __init__(self, api):
        self.api = api
        self.history = pd.DataFrame() 

    def next(self):
        pass

class KrakenMarketModel(MarketModel):
    def __init__(self):
        api = kr.Kraken.from_key_file('keys')
        MarketModel.__init__(self, api)

    def update(self, pairs):
        #Add new market data to historical record before returning it:
        ticker = self.api.ticker(pairs)
        self.history = self.history.append(ticker)
    
    def ask(self, pair):
        return float(self.history.loc[pair].iloc[-1].loc['ask'][0])
    
    def bid(self, pair):
        return float(self.history.loc[pair].iloc[-1].loc['bid'][0])

    def last(self, pair):
        return float(self.history.loc[pair].iloc[-1].loc['last'][0])
    
if __name__ == '__main__':
    test_market = KrakenMarketModel()

    for i in range(10):
        print(test_market.update('XETHXXBT'))
        print(test_market.history)
        print(test_market.ask('XETHXXBT'))
