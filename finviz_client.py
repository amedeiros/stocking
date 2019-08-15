from finviz.screener import Screener
import finviz
import pandas as pd
import nest_asyncio
nest_asyncio.apply()


def screener(filters=['exch_nasd', 'sh_avgvol_o200', 'sh_price_u5', 'ta_change_u10', 'geo_usa'], order='-volume'):
    stock_list = Screener(filters=filters, order=order)
    df = pd.DataFrame(stock_list.data)
    df.set_index("Ticker", drop=False)
    return df


def finviz_get_insider(stock):
    return finviz.get_insider(stock)


def finviz_get_news(stock):
    news = finviz.get_news(stock)
    table = pd.DataFrame(news)
    table.columns = ['Title', 'Link']
    return table
