import strategy
import market
import pandas
pandas.set_option('display.width', None)

def main():
    test_market = market.TestMarket()
    test_strategy = strategy.Strategy(test_market)

    test_strategy.simulate(2, 10, True)
    test_strategy.simulate(2, 5, True)
    test_strategy.simulate(2, 10, True)
    
if __name__ == '__main__':
    main()
