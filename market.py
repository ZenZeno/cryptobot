import poloniex
import pandas
import plotly
import plotly.graph_objs as go

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
        data = go.Data([
            go.Scatter(
                x = last.index,
                y = last
            )])
        layout = go.Layout(title = 'First Plot')
        figure = go.Figure(data = data, layout = layout)
        return figure
