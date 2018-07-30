import datetime 
import pandas 
import requests 
import hmac 
import hashlib 
import base64 
import urllib
import logging

import market_model

DATE_FMT = '%Y-%m-%d %H:%M:%S'

class API():
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.public_url = 'https://api.kraken.com/0/public/'
        self.private_url = 'https://api.kraken.com/0/private/'
        self.session = requests.Session()

    @classmethod
    def from_key_file(cls, filename):
        with open(filename) as keys:
            key = keys.readline().strip()
            secret = keys.readline().strip()
            return cls(key, secret)

    def _sign(self, data, url):
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = url.encode() + hashlib.sha256(encoded).digest()
        signature = hmac.new(base64.b64decode(self.secret),
                message, hashlib.sha512)
        sigdigest = base64.b64encode(signature.digest())
        return sigdigest.decode()
    
    def _nonce(self):
        return int(datetime.datetime.now().timestamp() * 1000)

    def ticker(self, pair):
        logging.info('Requesting Kraken Ticker for ' + pair)
        result = requests.get(self.public_url + 'Ticker', {'pair': pair})
        #construct a pandas dataframe from the ticker data:
        result = dict(result.json())
        logging.debug('Ticker received: ' + str(result))
        result = result['result']
        result = pandas.DataFrame(result).T
        result[['ask', 'bid', 'last', 'volume', 'vol weighted avg price', 
            '# trades', 'low', 'high', 'open']] = result[:]
        result = result.drop(columns = ['a','b','c','v','p','t','l','h','o'])
        
        #index the currency information with timestamp:
        now = datetime.datetime.now()
        date_index = []
        for i in range(len(result.index)):
            date_index.append(now)
        levels = [result.index, date_index]
        index = pandas.MultiIndex.from_arrays(levels)
        return result.set_index(index, drop = True)

    def balance(self):
        data = {'nonce': self._nonce()}
        urlpath = '/0/private/Balance'
        headers = {
                'API-Key': self.key,
                'API-Sign': self._sign(data, urlpath)
                }
        result = self.session.post('https://api.kraken.com/0/private/Balance', data = data, headers = headers)
        result = dict(result.json())
        result = result['result']
        result = pandas.Series(result)
        return result
    
    def positions(self):
        data = {'nonce': self._nonce()}
        urlpath = '/0/private/OpenPositions'
        headers = {
                'API-Key': self.key,
                'API-Sign': self._sign(data, urlpath)
                }
        result = self.session.post('https://api.kraken.com/0/private/OpenPositions', data = data, headers = headers)
        
        result = dict(result.json())
        result = result['result']
        result = pandas.DataFrame(result).T
        return result

    def trades(self, pair, since):
        data = {'pair': pair, 'since': since.timestamp()}
        result = requests.get(self.public_url + 'Trades', data)

        while result.status_code != 200:
            result = requests.get(self.public_url + 'Trades', data)

        result = result.json()
        result = result['result']
        last = result['last']
        result_frame = pandas.DataFrame()
        for i in range(len(result[pair])):
            row = pandas.Series(result[pair][i],
                    index = ['price', 'volume', 'time', 'buy/sell', 'market/limit', 'misc'])
            row.name = datetime.datetime.fromtimestamp(row['time'])
            row = row.drop('time')
            result_frame = result_frame.append(row)
        return result_frame

class LiveMarket(market_model.LiveMarketModel):
    def __init__(self):
        api = API.from_key_file('keys')
        market_model.LiveMarketModel.__init__(self, api)

    def ticker(self, pairs):
        new_ticker = self._api.ticker(pairs)
        new_ticker['ask'] = new_ticker['ask'][0][0]
        new_ticker['bid'] = new_ticker['bid'][0][0]
        self._ticker = self._ticker.append(new_ticker)
        return new_ticker
    
    def fetch_ohlc(self, pairs, start, end, period = 300):
        trades = self._api.trades(pairs, start)
        return trades
