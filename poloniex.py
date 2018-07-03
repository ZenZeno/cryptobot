import requests
import hmac
import hashlib
import datetime 
import pandas

class Poloniex:
    def __init__(self, key, secret):
        self.key = key
        self.secret = bytes(secret, 'utf8')
    
    def createTimeStamp(self, datestr, format="%Y-%m-%d %H:%M:%S"):
        timeStamp = datetime.datetime.strptime(datestr, format)
        return timeStamp.timestamp()

    def createTimeString(self, time_stamp, format="%Y-%m-%d %H:%M:%S"):
        time_string = datetime.datetime.fromtimestamp(time_stamp)
        return time_string.strftime(format)

    def api_query(self, command, args={}):
        if command == 'returnTicker' or command == 'return24hVolume' or command == 'returnCurrencies':
            result = requests.get('http://poloniex.com/public', {'command':command})
            return result
        elif command == 'returnChartData':
            args['command'] = command
            result = requests.get('http://poloniex.com/public', args)
            return result
        else:
            raise ValueError(command + ' is not a valid command')
        
    def returnTicker(self, pair):
        result = self.api_query('returnTicker')
        
        #Try again until data is recieved:
        while result.status_code != 200:
            print('Poloniex ticker timed out. Retrying...')
            result = self.api_query('returnTicker')

        #we want to return only the ticker data for the specified currency
        data = pandas.DataFrame(result.json())
        print(result)

        data = data.loc[:, pair].T

        #add a timestamp and convert data to the proper shape:
        date = pandas.Series({'date': datetime.datetime.now()})
        data = data.append(date)
        data = data.to_frame().T
        data = data.set_index('date')
        
        return data 

    def return24Volume(self):
        result = self.api_query('return24hVolume')
        if result:
            data = pandas.DataFrame(result.json()) 
            return data
        else:
            print('No data retrieved')

    def returnCurrencies(self):
        result = self.api_query('returnCurrencies')
        if result:
            data = pandas.DataFrame(result.json())
            return data
        else:
            print('No data retrieved')

    def returnChartData(self, pair, start, end, period):
        result = self.api_query('returnChartData', 
                                {'currencyPair':pair, 'start': start, 'end': end, 'period':period})
        while isinstance(result, (str, type(None))):
            result = self.api_query('returnChartData', 
                                    {'currencyPair':pair, 'start': start, 'end': end, 'period':period})

        result = pandas.DataFrame(result.json())
        result.index = result['date'].apply(self.createTimeString)
        result = result.drop('date', axis = 1)
        print(result)

        return result


if __name__ == '__main__':
    api = Poloniex('key', 'secret')

    tickerTest = api.returnTicker()
    print(tickerTest)

    volumeTest = api.return24Volume()
    print(volumeTest)

    currencyTest = api.returnCurrencies()
    print(currencyTest)

    chartTest = api.returnChartData('BTC_USD', api.createTimeStamp('2018-05-31 13:00:00'), 
                                    api.createTimeStamp('2018-05-31 14:00:00'), 900)

