import market
import time

def main():
    test_market = market.Market()
    test_market.update()

    while True:
        time.sleep(10)    
        test_market.update()

if __name__ == '__main__':
    main()
