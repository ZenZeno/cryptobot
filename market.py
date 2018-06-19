import poloniex
import pandas
import plotly


class Market():
    def __init__(self, mode = 'ticker', pair = 'BTC_ETH', start = False, end = False, period = 300):
        self.api = poloniex.Poloniex('key', 'secret')
        self.period = period
        self.pair = pair
        
        if mode == 'history' and start and end:
            self.chart = self.api.returnChartData(self.pair, start, end, period)
            print(self.chart)

        if mode == 'ticker':
            self.ticker = self.api.returnTicker(self.pair)     
            print(self.ticker)

    def update(self):
        self.ticker = pandas.concat([self.ticker, self.api.returnTicker(self.pair)])
        
        print(self.ticker)

    def plot(self):
        last = self.ticker['last']

        plotly.offline.plot({
                             'data': [last.index, last.data],
                             'layout': go.Layout(title='hello world')
                            })

