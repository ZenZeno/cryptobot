import market
import time

def main():
    live_market = market.LiveMarket()
    live_market.update()

    test_market = market.TestMarket()
    test_market.calculate_moving_avg(10, 20)

if __name__ == '__main__':
    main()
