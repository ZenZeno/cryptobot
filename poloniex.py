import requests
import datetime 
import pandas
import hmac
import hashlib

class Poloniex:
    def __init__(self, key, secret):
        self.key = bytes(key, 'utf8')
        self.secret = bytes(secret, 'utf8')
    
    def ticker(self, pair):
        result = requests.get('http://poloniex.com/public', {'command': 'returnTicker'})
        
        #Try again until data is recieved:
        while result.status_code != 200:
            print('Poloniex ticker timed out. Retrying...')
            
            result = requests.get('http://poloniex.com/public', {'command': 'returnTicker'})

        #we want to return only the ticker data for the specified currency
        data = pandas.DataFrame(result.json())
        data = data.loc[:, pair].T

        #add a timestamp and convert data to the proper shape:
        date = pandas.Series({'date': datetime.datetime.now()})
        data = data.append(date)
        data = data.to_frame().T
        data = data.set_index('date')
        
        return data 

    def chart_data(self, pair, start, end, period):
        print('Fetching poloniex chart data...')

        result = requests.get('http://poloniex.com/public', 
                {'command': 'returnChartData', 
                 'currencyPair':pair, 
                 'start': start, 
                 'end': end, 
                 'period':period})
        
        #Try again until data is recieved:
        while result.status_code != 200:
            print('Poloniex chart data timed out. Retrying...')

            result = requests.get('http://poloniex.com/public', 
                    {'command': 'returnChartData', 
                     'currencyPair':pair, 
                     'start': start, 
                     'end': end, 
                     'period':period})

        #parse json into dataframe, then set the date string as index:
        result = pandas.DataFrame(result.json())
        result.index = result['date'].apply(self.createTimeString)
        result = result.drop('date', axis = 1)

        return result
    
    def balances(self):
        nonce = int(datetime.datetime.now().timestamp() * 1000)
        payload = {'command': 'returnBalances',
                   'nonce': nonce}
        
        request = requests.Request('POST', 'https://poloniex.com/tradingApi',
                data = payload)

        #Sign the request with SHA512 hash and send the appropriate headers:
        request = request.prepare()
        signature =  hmac.new(self.secret, request.body, 
                digestmod = hashlib.sha512)
        request.headers['Sign'] = signature.hexdigest()
        request.headers['Key'] = self.key

        #Open a session and send the request:
        with requests.Session() as session:
            result = session.send(request)
           
            #Try again until response is recieved:
            while result.status_code != 200:
                print('Poloniex balances timed out, retrying...')
                result = session.send(request)
        
        #Return a pandas series of the data:
        result = pandas.Series(result.json())
        return result

    def buy(self, currency_pair, rate, amount):
        nonce = int(datetime.datetime.now().timestamp() * 1000)
        payload = {'command': 'buy',
                   'currencyPair': currency_pair,
                   'rate': rate,
                   'amount': amount,
                   'nonce': nonce}
        
        request = requests.Request('POST', 'https://poloniex.com/tradingApi',
                data = payload)

        #Sign the request with SHA512 hash and send the appropriate headers:
        request = request.prepare()
        signature =  hmac.new(self.secret, request.body, 
                digestmod = hashlib.sha512)
        request.headers['Sign'] = signature.hexdigest()
        request.headers['Key'] = self.key

        #Open a session and send the request:
        with requests.Session() as session:
            print('Placing buy order')
            result = session.send(request)
           
            #Try again until response is recieved:
            while result.status_code != 200:
                print('Poloniex balances timed out, retrying...')
                result = session.send(request)
        
        #Return a pandas series of the data:
        result = pandas.Series(result.json())
        return result

    def sell(self, currency_pair, rate, amount):
        nonce = int(datetime.datetime.now().timestamp() * 1000)
        payload = {'command': 'buy',
                   'currencyPair': currency_pair,
                   'rate': rate,
                   'amount': amount,
                   'nonce': nonce}
        
        request = requests.Request('POST', 'https://poloniex.com/tradingApi',
                data = payload)

        #Sign the request with SHA512 hash and send the appropriate headers:
        request = request.prepare()
        signature =  hmac.new(self.secret, request.body, 
                digestmod = hashlib.sha512)
        request.headers['Sign'] = signature.hexdigest()
        request.headers['Key'] = self.key

        #Open a session and send the request:
        with requests.Session() as session:
            print('Placing buy order')
            result = session.send(request)
           
            #Try again until response is recieved:
            while result.status_code != 200:
                print('Poloniex balances timed out, retrying...')
                result = session.send(request)
        
        #Return a pandas series of the data:
        result = pandas.Series(result.json())
        return result

if __name__ == '__main__':
    with open('keys') as file:
        api_keys = file.read().strip().split(',')

    api = Poloniex(api_keys[0], api_keys[1])
    print(api.balances())
