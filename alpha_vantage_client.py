import requests
import os
import pandas as pd


class AlphaVantageClient:
    BASE_URL = 'https://www.alphavantage.co'
    KEY = os.environ['ALPHA_VANTAGE_KEY']

    def __init__(self, ticker):
        self.ticker = ticker

    def time_series_daily(self, outputsize='full'):
        response = requests.get(
            self._url(function='TIME_SERIES_DAILY', outputsize=outputsize))

        return self._frame_response(response, 'Time Series (Daily)')

    def time_series_intraday(self, interval='60min', outputsize='full'):
        url = self._url(function='TIME_SERIES_INTRADAY',
                        outputsize=outputsize) + '&interval=' + interval
        response = requests.get(url)

        return self._frame_response(response, 'Time Series (%s)' % (interval))

    def _url(self, function, outputsize):
        return '%s/query?function=%s&symbol=%s&outputsize=%s&apikey=%s' % (
            AlphaVantageClient.BASE_URL, function, self.ticker, outputsize, AlphaVantageClient.KEY)

    def _frame_response(self, response, primary_key):
        data = {'dates': [], 'open': [], 'close': [],
                'high': [], 'low': [], 'volume': []}

        for k, v in response.json()[primary_key].items():
            data['dates'].append(k)
            data['close'].append(float(v['4. close']))
            data['open'].append(float(v['1. open']))
            data['high'].append(float(v['2. high']))
            data['low'].append(float(v['3. low']))
            data['volume'].append(float(v['5. volume']))

        return pd.DataFrame(data=data)
