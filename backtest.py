import pandas as pd
import numpy as np
import datetime as dt
import sys

import poloniex
import execution_model as em
import market_model as mm
import portfolio_constructor as pc

def pick_random_time_period():
    DATE_FMT = '%Y-%m-%d %H:%M:%S'  
    min_date = dt.datetime.strptime('2014-01-01 00:00:00', DATE_FMT).timestamp()
    max_date = dt.datetime.now().timestamp()

    start = np.random.randint(min_date, max_date)
    end = np.random.randint(start, max_date)

    start = dt.datetime.fromtimestamp(start)
    end = dt.datetime.fromtimestamp(end)

    return start, end

def construct_random_model(time_period):
    api = poloniex.Poloniex('', '')
    test_market = mm.TestMarket(api, 'BTC_ETH', time_period[0].timestamp(), time_period[1].timestamp(), 300)
    
    short_window = np.random.randint(1, 20)
    long_window = np.random.randint(short_window + 1, 100)

    portfolio = pc.BTC_ETH_MovingAverageCrossover(1000, short_window, long_window, 10, 'weightedAverage')
    
    model = em.ExecutionModel(False, test_market, portfolio)

    return model

def main():
    num_simulations = sys.argv[1]

    for i in range(int(num_simulations)):
        time_period = pick_random_time_period()
        model = construct_random_model(time_period)
        model.execute()

if __name__ == '__main__':
    main()

