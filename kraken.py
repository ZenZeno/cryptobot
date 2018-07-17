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

if __name__ == '__main__':
    api = Kraken('','')
    ticker = api.ticker('ETHXBT')
    print(ticker)

