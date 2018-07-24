import datetime as dt
import pandas as pd
import requests as rq
import hmac as hm
import hashlib as hl
import base64 as b64
import urllib

import market_model

class API():
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.public_url = 'https://api.kraken.com/0/public/'
        self.private_url = 'https://api.kraken.com/0/private/'
        self.session = rq.Session()

    @classmethod
    def from_key_file(cls, filename):
        with open(filename) as keys:
            key = keys.readline().strip()
            secret = keys.readline().strip()
            return cls(key, secret)

    def sign(self, data, url):
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = url.encode() + hl.sha256(encoded).digest()
        signature = hm.new(b64.b64decode(self.secret),
                message, hl.sha512)
        sigdigest = b64.b64encode(signature.digest())
        return sigdigest.decode()
    
    def nonce(self):
        return int(dt.datetime.now().timestamp() * 1000)

    def ticker(self, pair):
        result = rq.get(self.public_url + 'Ticker', {'pair': pair})
        print(result.json())
        #construct a pandas dataframe from the ticker data:
        result = dict(result.json())
        result = result['result']
        result = pd.DataFrame(result).T
        result[['ask', 'bid', 'last', 'volume', 'vol weighted avg price', 
            '# trades', 'low', 'high', 'open']] = result[:]
        result = result.drop(columns = ['a','b','c','v','p','t','l','h','o'])
        
        #index the currency information with timestamp:
        now = dt.datetime.now()
        date_index = []
        for i in range(len(result.index)):
            date_index.append(now)
        levels = [result.index, date_index]
        index = pd.MultiIndex.from_arrays(levels)
        return result.set_index(index, drop = True)

    def balance(self):
        data = {'nonce': self.nonce()}
        urlpath = '/0/private/Balance'
        headers = {
                'API-Key': self.key,
                'API-Sign': self.sign(data, urlpath)
                }
        result = self.session.post('https://api.kraken.com/0/private/Balance', data = data, headers = headers)
        result = dict(result.json())
        result = result['result']
        result = pd.Series(result)
        return result
    
    def positions(self):
        data = {'nonce': self.nonce()}
        urlpath = '/0/private/OpenPositions'
        headers = {
                'API-Key': self.key,
                'API-Sign': self.sign(data, urlpath)
                }
        result = self.session.post('https://api.kraken.com/0/private/OpenPositions', data = data, headers = headers)
        
        result = dict(result.json())
        result = result['result']
        result = pd.DataFrame(result).T
        return result

class Market(market_model.MarketModel):
    def __init__(self):
        api = API.from_key_file('keys')
        market_model.MarketModel.__init__(self, api)

    def ticker(self, pairs):
        new_ticker = self._api.ticker(pairs)
        self._ticker = self._ticker.append(new_ticker)
        return new_ticker

