import time
import pandas

import market
import strategy

pandas.set_option('display.width', None)
test_market = market.LiveMarket()
test_strategy = strategy.Strategy(test_market)

while True:
    test_strategy.trade()
    test_strategy.display()
    time.sleep(1)


