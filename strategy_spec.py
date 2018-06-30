import strategy
import market

def main():
    test_market = market.TestMarket()
    test_strategy = strategy.Strategy(test_market)

    test_strategy.generate_signals()

    print(test_strategy.market.ticker)

    test_strategy.trade()

if __name__ == '__main__':
    main()
