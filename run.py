import asyncio
import json
import re

import boto3
import pandas
import plotly
from slackbot.bot import Bot, respond_to
from tabulate import tabulate

from slackbot_settings import *
from algo_bot.clients import finviz_client, alpha_vantage_client, trends
import charting
import stocking


def main():
    print("Starting!")
    bot = Bot()
    bot.run()


@respond_to("ticker (.*)", re.IGNORECASE)
def ticker(message, ticker):
    df = alpha_vantage_client.company_overview(ticker)
    _store_html(df.to_html(classes='table table-striped'),
                f"{ticker}_overview.html")
    message.send_webapi('', json.dumps(
        _attachments(message, text=df["Description"][0], title=f"Overview for {ticker}", title_link=_html_url(f"{ticker}_overview.html"))))


@respond_to("ticker-top5 (.*)", re.IGNORECASE)
def ticker_top(message, ticker):
    df = alpha_vantage_client.time_series_daily(ticker).head()
    message.reply(_wrap_ticks_tabluate(df))


@respond_to("screener (.*)", re.IGNORECASE)
def screener(message, filters):
    df = finviz_client.screener(filters=filters.split(","))
    filename = f"{filters.replace(',', '_')}screener.html"
    _store_html(df.to_html(classes='table table-striped'), filename)
    message.send_webapi('', json.dumps(
        _attachments(message, title=f"FinViz Screener Results", title_link=_html_url(filename))))


@respond_to("ticker-performance (.*)", re.IGNORECASE)
def ticker_performance(message, ticker):
    df = finviz_client.finviz_performance(ticker=ticker)
    filename = f"{ticker}_performance.html"
    _store_html(df.to_html(classes="table table-striped"), filename)
    message.send_webapi('', json.dumps(_attachments(
        message, title=f"Performance for {ticker}", title_link=_html_url(filename))))


@respond_to("ticker-overview (.*)", re.IGNORECASE)
def ticker_overview(message, ticker):
    df = finviz_client.finviz_overview(ticker=ticker)
    filename = f"{ticker}_overview.html"
    _store_html(df.to_html(classes="table table-striped"), filename)
    message.send_webapi('', json.dumps(_attachments(
        message, title=f"Overview for {ticker}", title_link=_html_url(filename))))


@respond_to("ticker-technical (.*)", re.IGNORECASE)
def ticker_technical(message, ticker):
    df = finviz_client.finviz_technical(ticker=ticker)
    filename = f"{ticker}_technical.html"
    _store_html(df.to_html(classes="table table-striped"), filename)
    message.send_webapi('', json.dumps(_attachments(
        message, title=f"Technical for {ticker}", title_link=_html_url(filename))))


@respond_to("ticker-ownership (.*)", re.IGNORECASE)
def ticker_ownership(message, ticker):
    df = finviz_client.finviz_ownership(ticker=ticker)
    filename = f"{ticker}_ownership.html"
    _store_html(df.to_html(classes="table table-striped"), filename)
    message.send_webapi('', json.dumps(_attachments(
        message, title=f"Ownership for {ticker}", title_link=_html_url(filename))))


@respond_to("ticker-financial (.*)", re.IGNORECASE)
def ticker_financial(message, ticker):
    df = finviz_client.finviz_financial(ticker=ticker)
    _store_html(df.to_html(classes='table table-striped'),
                f"{ticker}_financial.html")

    message.send_webapi('', json.dumps(_attachments(
        message, title=f"Financials for {ticker}", title_link=_html_url(f"{ticker}_financial.html"))))


@respond_to("insider (.*)", re.IGNORECASE)
def insider(message, ticker):
    insider = finviz_client.finviz_get_insider(ticker)
    df = pandas.DataFrame(insider)
    filename = f"{ticker}_insider.html"
    _store_html(df.to_html(classes="table table-striped"), filename)
    message.send_webapi('', json.dumps(_attachments(
        message, title=f"Insider for {ticker}", title_link=_html_url(filename))))


@respond_to("candlestick (.*)", re.IGNORECASE)
def candlestick(message, ticker, interval="60min"):
    _processing(message)
    time_series = alpha_vantage_client.time_series_intraday(
        ticker, interval=interval)
    fig = charting.candlestick_plot(time_series)
    _store_graph(fig, "%s_candlestick.html" % ticker)
    message.send_webapi('', json.dumps(_attachments(
        message, title=f"Candlestick Chart For {ticker}", title_link=_html_url("%s_candlestick.html" % ticker))))


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
    _processing(message)
    interest = trends.interest_over_time(ticker)
    df = pandas.DataFrame(interest)
    fig = charting.line_chart_trends(df)
    filename = f"{ticker}_interest_over_time.html"
    _store_graph(fig, filename)
    message.send_webapi('', json.dumps(_attachments(
        message, title=f"Interest Over Time: {ticker}", title_link=_html_url(filename))))


@respond_to("sector-performance", re.IGNORECASE)
def sector_performance(message):
    _processing(message)
    df = alpha_vantage_client.sector_performance()
    fig = charting.sector_performance_chart(df)
    _store_graph(fig, "sector_performance.html")
    message.send_webapi('', json.dumps(_attachments(
        message, title=f"Sector Performance", title_link=_html_url("sector_performance.html"))))


@respond_to("golden-cross (.*)", re.IGNORECASE)
def golden_cross(message, ticker):
    _processing(message)
    time_series = alpha_vantage_client.time_series_daily(ticker)
    sma_50 = alpha_vantage_client.sma(ticker)
    sma_200 = alpha_vantage_client.sma(ticker, time_period="200")
    fig = charting.golden_cross(
        start=stocking.today(),
        stop=stocking.years_ago(),
        df=time_series,
        sma_50=sma_50,
        sma_200=sma_200,
        ticker=ticker,
    )
    _store_graph(fig, f"{ticker}_golden_cross.html")
    message.send_webapi('', json.dumps(_attachments(
        message, title=f"Golden Cross Chart For {ticker}", title_link=_html_url(f"{ticker}_golden_cross.html"))))


@respond_to("sma (.*)", re.IGNORECASE)
def sma(message, ticker):
    _processing(message)
    sma = alpha_vantage_client.sma(ticker)
    fig = charting.plot_sma(sma)
    filename = f"{ticker}_sma.html"
    _store_graph(fig, filename)
    message.send_webapi('', json.dumps(_attachments(
        message, title=f"SMA Chart For {ticker}", title_link=_html_url(filename))))


@respond_to("help", re.IGNORECASE)
def help(message):
    response = (
        """
Stocking bot help (%s)

    @stockbot ticker TICKER (AlphaVantage Overview)
    @stockbot news TICKER (Returns news from FinViz as individual messages of URL's to unfurl)
    @stockbot news-compact TICKER (Returns news from FinViz as one message results in no unfurling)
    @stockbot interest-over-time TICKER (Chart news interest over time)
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
    @stockbot sma TICKER (Chart of the simple moving average)
    @stockbot golden-cross TICKER (50SMA cross over the 200SMA)
    """
        % BOT_ENV
    )
    message.reply(_wrap_ticks(response))


def _attachments(message, title, title_link, footer="Stocking Bot 0.1b", text=None, fields=[]):
    return [
        {
            'author_name': message.user["profile"]["real_name"],
            'title_link': title_link,
            'title': title,
            'color': f"#{message.user['color']}",
            'text': text,
            'footer': footer,
            "fields":fields,
        }]


def _wrap_ticks(message):
    return """\n```\n%s\n```""" % (message)


def _wrap_ticks_tabluate(df, headers="keys", tablefmt="pipe"):
    return _wrap_ticks(tabulate(df, headers=headers, tablefmt=tablefmt))


def _get_news_urls(ticker):
    urls = []
    table = finviz_client.finviz_get_news(ticker)
    for _, url in table.head().iterrows():
        urls.append(url["Link"])
    return urls


def _processing(message):
    message.reply("Processing...")


def _html_url(name, bucket="stocks-am"):
    return boto3.client("s3").generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": bucket,
            "Key": name,
            "ResponseContentType": "text/html",
        },
    )


def _store_html(html, name, bucket="stocks-am"):
    f = open("templates/%s" % name, "w")
    f.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">\n')
    f.write('<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>\n')
    f.write('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>\n')
    f.write(html)
    f.close()
    s3 = boto3.resource("s3")
    s3.Object(bucket, name).put(Body=open("templates/%s" % name, "rb"))


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
