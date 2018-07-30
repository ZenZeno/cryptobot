import unittest
import pandas
import datetime
import logging

import market_model
import kraken
import poloniex
import portfolio

DATE_FMT = '%Y-%m-%d %H:%M:%S'

class KrakenLiveMarket(unittest.TestCase):
    def setUp(self):
        self.market = kraken.LiveMarket()
        pandas.set_option('display.width', None)

    def test_ticker(self):
        self.assertIsInstance(self.market.ticker('ETHXBT'), pandas.DataFrame)

if __name__ == '__main__':
    logging.basicConfig(filename='test.log', level=logging.DEBUG, filemode='w')
    unittest.main()
