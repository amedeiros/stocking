import asyncio

import finviz
import nest_asyncio
import pandas as pd
from finviz.screener import Screener

nest_asyncio.apply()


def screener(
    filters=["exch_nasd", "sh_avgvol_o200", "sh_price_u5", "ta_change_u10", "geo_usa"],
    order="-volume",
):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    stock_list = Screener(filters=filters, order=order)
    df = pd.DataFrame(stock_list.data)
    df.set_index("Ticker", drop=False)
    loop.close()
    return df


def finviz_performance(ticker):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    s = Screener(table="Performance", tickers=[ticker])
    df = pd.DataFrame(s.data)
    loop.close()
    return df


def finviz_overview(ticker):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    s = Screener(table="Overview", tickers=[ticker])
    df = pd.DataFrame(s.data)
    loop.close()
    return df


def finviz_technical(ticker):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    s = Screener(table="Technical", tickers=[ticker])
    df = pd.DataFrame(s.data)
    loop.close()
    return df


def finviz_ownership(ticker):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    s = Screener(table="Ownership", tickers=[ticker])
    df = pd.DataFrame(s.data)
    loop.close()
    return df


def finviz_financial(ticker):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    s = Screener(table="Financial", tickers=[ticker])
    df = pd.DataFrame(s.data)
    loop.close()
    return df


def finviz_get_insider(stock):
    return finviz.get_insider(stock)


def finviz_get_news(stock):
    news = finviz.get_news(stock)
    table = pd.DataFrame(news)
    table.columns = ["Title", "Link"]
    return table
