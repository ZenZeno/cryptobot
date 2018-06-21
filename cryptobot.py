import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import market

test_market = market.Market()

app = dash.Dash()

app.layout = html.Div(
        html.Div([
            html.H4('Poloniex Market'),
            dcc.Graph(id='live-ticker-feed'),
            dcc.Interval(
                id = 'interval',
                interval = 1000,
                n_intervals =0
                ),
            html.Div(id='table-container')
            ])
        )
        
@app.callback(Output('live-ticker-feed', 'figure'),
        [Input('interval', 'n_intervals')])
def update_ticker(n):
    test_market.update()
    figure = test_market.plot()

    return figure


@app.callback(Output('table-container', 'children'),
        [Input('interval', 'n_intervals')])
def update_table(n):
    return test_market.generate_table(10)

if __name__ == '__main__':
    app.run_server()
