import market
import time

def main():
    live_market = market.LiveMarket()
    live_market.update()

    test_market = market.TestMarket()

if __name__ == '__main__':
    main()
