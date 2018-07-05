#Python libraries:
import datetime
import numpy as np
import pandas as pd

#Cryptobot classes:
import strategy
import market
import poloniex

pd.set_option('display.width', None)

def run_simulation(start, end):
    test_market = market.TestMarket(start = start.strftime('%Y-%m-%d %H:%M:%S'), 
                                    end = end.strftime('%Y-%m-%d %H:%M:%S')) 
    test_strategy = strategy.Strategy(test_market)

    test_strategy.simulate()
    print(test_strategy.get_stats())

def rand_period():
    min_date = datetime.datetime.strptime('2014-01-01 00:00:00', '%Y-%m-%d %H:%M:%S').timestamp() 
    max_date = datetime.datetime.now().timestamp()
    
    #pick two dates within the parameters, start must be before end:
    start = np.random.randint(min_date, max_date)
    end = np.random.randint(start, max_date)

    start_date = datetime.datetime.fromtimestamp(start)
    end_date = datetime.datetime.fromtimestamp(end)
    
    return start_date, end_date

def main():

    start_date, end_date = rand_period()
    run_simulation(start_date, end_date)

if __name__ == '__main__':
    main()
