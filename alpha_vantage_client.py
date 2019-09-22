import requests
import os
import pandas as pd
from datetime import datetime


class AlphaVantageClient:
    BASE_URL = 'https://www.alphavantage.co/query?'
    KEY = os.environ['ALPHA_VANTAGE_KEY']

    def __init__(self, ticker):
        self.ticker = ticker

    def time_series_daily(self, outputsize='full'):
        response = requests.get(
            self._url(function='TIME_SERIES_DAILY', outputsize=outputsize, symbol=self.ticker))

        return self._frame_response(response, 'Time Series (Daily)')

    def time_series_intraday(self, interval='60min', outputsize='full'):
        url = self._url(function='TIME_SERIES_INTRADAY',
                        outputsize=outputsize, interval=interval, symbol=self.ticker)

        response = requests.get(url)

        return self._frame_response(response, 'Time Series (%s)' % (interval))

    def sma(self, interval='daily', series_type='open', time_period='50'):
        url = self._url(function='SMA', symbol=self.ticker,
                        series_type=series_type, time_period=time_period, interval=interval)

        response = requests.get(url)

        data = {'dates': [], 'sma': []}

        for k, v in response.json()['Technical Analysis: SMA'].items():
            try:
                data['dates'].append(datetime.strptime(k, "%Y-%m-%d"))
                data['sma'].append(float(v['SMA']))
            except:
                pass

        return pd.DataFrame(data=data)

    def sector_performance(self):
        url = self._url(function="SECTOR")

        response = requests.get(url)

        data = {'type': [], 'energy': [], 'consumer discretionary': [],
                'industrials': [], 'consumer staples': [], 'financials': [],
                'materials': [], 'health care': [], 'communication': [],
                'real estate': [], 'IT': [], 'utilities': []}

        for k, v in response.json().items():
            if k != 'Meta Data':
                data['type'].append(k)
                data['energy'].append(float(v['Energy'][:-1]))
                data['consumer discretionary'].append(
                    float(v['Consumer Discretionary'][:-1]))
                data['industrials'].append(float(v['Industrials'][:-1]))
                data['consumer staples'].append(
                    float(v['Consumer Staples'][:-1]))
                data['financials'].append(float(v['Financials'][:-1]))
                data['materials'].append(float(v['Materials'][:-1]))
                data['health care'].append(float(v['Health Care'][:-1]))
                data['communication'].append(
                    float(v['Communication Services'][:-1]))
                data['IT'].append(float(v['Information Technology'][:-1]))
                data['utilities'].append(float(v['Utilities'][:-1]))

                if 'Real Estate' in v.keys():
                    data['real estate'].append(float(v['Real Estate'][:-1]))
                else:
                    # real estate not always present
                    data['real estate'].append(0.0)

        return pd.DataFrame(data=data)

    def _url(self, **vargs):
        url = AlphaVantageClient.BASE_URL

        for k, v in vargs.items():
            url += "%s=%s&" % (k, v)

        url += 'apikey=' + AlphaVantageClient.KEY

        return url

    def _frame_response(self, response, primary_key):
        data = {'dates': [], 'open': [], 'close': [],
                'high': [], 'low': [], 'volume': []}

        for k, v in response.json()[primary_key].items():
            try:
                data['dates'].append(datetime.strptime(k, "%Y-%m-%d"))
            except:
                data['dates'].append(datetime.strptime(k, "%Y-%m-%d %H:%M:%S"))

            data['close'].append(float(v['4. close']))
            data['open'].append(float(v['1. open']))
            data['high'].append(float(v['2. high']))
            data['low'].append(float(v['3. low']))
            data['volume'].append(float(v['5. volume']))

        return pd.DataFrame(data=data)
