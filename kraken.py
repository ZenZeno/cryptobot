import datetime as dt
import pandas as pd
import requests as rq
import hmac as hm
import hashlib as hl
import base64 as b64
import urllib

class Kraken():
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

    def ticker(self, pair):
        result = rq.get(self.public_url + 'Ticker', {'pair': pair})

        #construct a pandas dataframe from the ticker data:
        result = dict(result.json())
        result = result['result']
        result = pd.DataFrame(result).T
        result[['ask', 'bid', 'last', 'volume', 'vol weighted avg price', 
            '# trades', 'low', 'high', 'open']] = result[:]
        result = result.drop(columns = ['a','b','c','v','p','t','l','h','o'])
        
        #index the currency information with timestamp:
        levels = [result.index, [dt.datetime.now()]]
        index = pd.MultiIndex.from_arrays(levels)
        return result.set_index(index, drop = True)

    def balance(self, coins):
        data = {'nonce': int(dt.datetime.now().timestamp() * 1000)}
        urlpath = '/0/private/Balance'
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hl.sha256(encoded).digest()
        print(message)
        signature = hm.new(b64.b64decode(self.secret),
                message, hl.sha512)
        sigdigest = b64.b64encode(signature.digest())
        headers = {
                'API-Key': self.key,
                'API-Sign': sigdigest.decode()
                }
        result = self.session.post('https://api.kraken.com/0/private/Balance', data = data, headers = headers)
        return result.json()

if __name__ == '__main__':
    api = Kraken.from_key_file('keys')
    print(api.key, api.secret)
    ticker = api.ticker('ETHXBT')
    print(ticker)
    print(api.balance(['XBT','ETH']))
