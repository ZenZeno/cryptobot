import strategy
import market
import pandas
pandas.set_option('display.width', None)

def main():
    test_market = market.TestMarket()
    test_strategy = strategy.Strategy(test_market)

    test_strategy.simulate(2, 10)
    test_strategy.simulate(2, 5)
    test_strategy.simulate(2, 10)
    
if __name__ == '__main__':
    main()
