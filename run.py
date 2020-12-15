import asyncio
import json
import re

import boto3
import pandas
import plotly
from slackbot.bot import Bot, respond_to
from tabulate import tabulate

import stocking
from charting import candlestick_plot
from finviz_client import finviz_get_news
from slackbot_settings import *


def main():
    print("Starting!")
    bot = Bot()
    bot.run()

@respond_to("ticker (.*)", re.IGNORECASE)
def ticker(message, ticker):
    msg = stocking.overview(ticker)
    message.reply(_wrap_ticks(msg))

@respond_to("ticker-top5 (.*)", re.IGNORECASE)
def ticker_top(message, ticker):
    df = stocking.time_series_daily(ticker).head()
    message.reply(_wrap_ticks_tabluate(df))


@respond_to("screener (.*)", re.IGNORECASE)
def screener(message, filters):
    filters = filters.split(",")
    df = stocking.screener(filters=filters)
    message.reply(_wrap_ticks_tabluate(df))


@respond_to("ticker-performance (.*)", re.IGNORECASE)
def ticker_performance(message, ticker):
    df = stocking.finviz_performance(ticker=ticker)
    message.reply(_wrap_ticks_tabluate(df))


@respond_to("ticker-overview (.*)", re.IGNORECASE)
def ticker_overview(message, ticker):
    df = stocking.finviz_overview(ticker=ticker)
    message.reply(_wrap_ticks_tabluate(df))


@respond_to("ticker-technical (.*)", re.IGNORECASE)
def ticker_technical(message, ticker):
    df = stocking.finviz_technical(ticker=ticker)
    message.reply(_wrap_ticks_tabluate(df))


@respond_to("ticker-ownership (.*)", re.IGNORECASE)
def ticker_ownership(message, ticker):
    df = stocking.finviz_ownership(ticker=ticker)
    message.reply(_wrap_ticks_tabluate(df))


@respond_to("ticker-financial (.*)", re.IGNORECASE)
def ticker_financial(message, ticker):
    df = stocking.finviz_financial(ticker=ticker)
    message.reply(_wrap_ticks_tabluate(df))


@respond_to("insider (.*)", re.IGNORECASE)
def insider(message, ticker):
    insider = stocking.finviz_get_insider(ticker)
    df = pandas.DataFrame(insider).head(10)
    ticks = _wrap_ticks_tabluate(df)
    message.reply(ticks)


@respond_to("candlestick (.*)", re.IGNORECASE)
def candlestick(message, ticker):
    _processing(message)
    time_series = stocking.time_series_daily(ticker)
    fig = candlestick_plot(time_series)
    _store_graph(fig, "%s_candlestick.html" % ticker)
    message.reply(_graph_url("%s_candlestick.html" % ticker))


@respond_to("news (.*)", re.IGNORECASE)
def news(message, ticker):
    for url in _get_news_urls(ticker):
        message.reply(url)


@respond_to("news-compact (.*)", re.IGNORECASE)
def compact_news(message, ticker):
    response = "\n".join(_get_news_urls(ticker))
    message.reply(response)


@respond_to("interest-over-time (.*)", re.IGNORECASE)
def interest_over_time(message, ticker):
    interest = stocking.interest_over_time(ticker)
    df = pandas.DataFrame(interest).head(10)
    message.reply(_wrap_ticks_tabluate(df))


@respond_to("sector-performance", re.IGNORECASE)
def sector_performance(message):
    df = stocking.sector_performance().head(10)
    message.reply(_wrap_ticks_tabluate(df))


@respond_to("prophet (.*)", re.IGNORECASE)
def prophet(message, ticker):
    _processing(message)
    time_series = stocking.time_series_daily(ticker)
    prophet = stocking.prophet(time_series, "open")
    future = prophet.make_future_dataframe(periods=365)
    forecast = prophet.predict(future)
    date = stocking.today()
    forecast.to_csv("./forecasts/" + ticker + "-" + date + "-forecast.csv")
    fig = stocking.plot_plotly(prophet, forecast)
    _store_graph(fig, "%s_prophet.html" % ticker)
    message.reply(_graph_url("%s_prophet.html" % ticker))


@respond_to("golden-cross (.*)", re.IGNORECASE)
def golden_cross(message, ticker):
    _processing(message)
    time_series = stocking.time_series_daily(ticker)
    df = time_series.set_index("dates")
    sma_50 = stocking.sma(ticker).set_index("dates")
    sma_200 = stocking.sma(ticker, time_period="200").set_index("dates")
    fig = stocking.golden_cross(
        start=stocking.today(),
        stop=stocking.years_ago(),
        df=df,
        sma_50=sma_50,
        sma_200=sma_200,
        ticker=ticker,
    )
    _store_graph(fig, "%s_golden_cross.html" % ticker)
    message.reply(_graph_url("%s_golden_cross.html" % ticker))


@respond_to("help", re.IGNORECASE)
def help(message):
    response = (
        """
Stocking bot help (%s)

    @stockbot ticker TICKER (AlphaVantage Overview)
    @stockbot news TICKER (Returns news from FinViz as individual messages of URL's to unfurl)
    @stockbot news-compact TICKER (Returns news from FinViz as one message results in no unfurling)
    @stockbot ticker-top5 TICKER (Returns last five days of open, close, high, low and volume)
    @stockbot candlestick TICKER (Link to a candlestick chart for the supplied ticker)
    @stockbot screener FILTERS (Finviz screener comma seperated filters EX: @stockbot screener exch_nasd,geo_usa,sh_price_u5,ta_sma50_cross200a)
    @stockbot ticker-performance TICKER (Finviz performance table)
    @stockbot ticker-overview TICKER (Finviz overview table)
    @stockbot ticker-technical TICKER (Finviz technical table)
    @stockbot ticker-ownership TICKER (Finviz ownership table)
    @stockbot ticker-financial TICKER (Finviz financial table)
    @stockbot insider TICKER (List last 10 insider trades)
    @stockbot sector-performance (Get back sector performance)
    @stockbot golden-cross TICKER (50SMA cross over the 200SMA)
    @stockbot prophet TICKER (facebooks prophet forecasting algorithm)
    """
        % BOT_ENV
    )
    message.reply(_wrap_ticks(response))


def _wrap_ticks(message):
    return """\n```\n%s\n```""" % (message)


def _wrap_ticks_tabluate(df, headers="keys", tablefmt="pipe"):
    return _wrap_ticks(tabulate(df, headers=headers, tablefmt=tablefmt))


def _get_news_urls(ticker):
    urls = []
    table = finviz_get_news(ticker)
    for _, url in table.head().iterrows():
        urls.append(url["Link"])
    return urls


def _processing(message):
    message.reply("Processing...")


def _graph_url(name, bucket="stocks-am"):
    return boto3.client("s3").generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": bucket,
            "Key": name,
            "ResponseContentType": "text/html",
        },
    )


def _store_graph(fig, name, bucket="stocks-am"):
    if BOT_ENV == "development":
        plotly.offline.plot(fig, filename="./templates/%s" % name)
        s3 = boto3.resource("s3")
        s3.Object(bucket, name).put(Body=open("./templates/%s" % name, "rb"))
        os.remove("./templates/%s" % name)
    else:
        raise RuntimeError("Unknown environment %s" % BOT_ENV)


if __name__ == "__main__":
    main()
