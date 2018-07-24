import unittest
import market_model
import kraken

class MarketModelTests(object):
    pass

class KrakenModelTests(MarketModelTests, unittest.TestCase):
    def setUp(self):
        self.market = kraken.Market()

    def test_ticker(self):
        print(self.market.ticker('ETHXBT'))

    def test_ohlc(self):
        print(self.market.ohlc('ETHXBT'))

if __name__ == '__main__':
    unittest.main()
