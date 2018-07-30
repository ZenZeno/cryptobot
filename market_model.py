import pandas

class LiveMarketModel():
    def __init__(self, api):
        self._api = api
        self._ticker = pandas.DataFrame()

    def ticker(self, pairs):
        raise NotImplementedError

class TestMarketModel():
    def __init__(self, api):
        self._api = api
        self._chart = pandas.DataFrame()
        self.tick = -1 #-1 so that the first time next() is called, tick = 0

    def next(self):
        self.tick += 1
        return self._chart.iloc[self.tick]

    def chart(self, pairs):
        return(self._chart)
        
