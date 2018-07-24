import pandas

class MarketModel():
    def __init__(self, api):
        self._api = api
        self._ohlc = pandas.DataFrame() 
        self._ticker = pandas.DataFrame()

    def ticker(self, pairs):
        raise NotImplementedError

    def ohlc(self, pairs):
        raise NotImplementedError

    def calc_ohlc(self):
        raise NotImplementedError

    def get_ohlc(selfi, pairs):
        raise NotImplementedError

class PoloniexTestMarket(MarketModel):
    def __init__(self, pair, start, end, delta = 300):
        api = px.Poloniex('','')
        MarketModel.__init__(self, api)

        self.tick = 0
        self.history = self.api.chart_data(pair, start.timestamp(), end.timestamp(), delta)

    def update(self):
        self.tick += 1
        self.ticker = self.history.head(self.tick)

    def price(self):
        return self.ticker.iloc[-1]['weightedAverage']

