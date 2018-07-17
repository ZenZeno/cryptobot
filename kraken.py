import datetime as dt
import pandas as pd
import requests as rq

class Kraken():
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.public_url = 'https://api.kraken.com/0/public/'

    @classmethod
    def from_key_file(cls, filename):
        with open(filename) as keys:
            keys = keys.read().strip().split(',')
            return cls(keys[0], keys[1])

    def ticker(self, pair):
        result = rq.get(self.public_url + 'Ticker', {'pair': pair})

        result = dict(result.json())
        result = result['result']
        result = pd.DataFrame(result)
        result['ask', 'bid'] = result['a', 'b']
        return result

if __name__ == '__main__':
    api = Kraken('','')
    ticker = api.ticker('ETHXBT')
    print(ticker)

