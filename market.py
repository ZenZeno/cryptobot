import poloniex
import pandas
import plotly
import plotly.graph_objs as go
import dash_html_components as html


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

    def generate_table(self, max_rows = 10):
        #Convert the tail of self.ticker into an html table:
        tail = self.ticker.tail(max_rows)
        table = html.Table(
                #Header
                [html.Tr([html.Th(col) for col in tail.columns])] + 
                #Body
                [html.Tr(
                    [html.Td(tail.iloc[i][col]) for col in tail.columns
                    ]) for i in range(min(len(tail), max_rows))]
                )
        
        return table
