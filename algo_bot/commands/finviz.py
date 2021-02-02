import re

import pandas as pd
from slackbot.bot import respond_to

from algo_bot import utils
from algo_bot.clients import finviz_client


@respond_to("^screener (.*)", re.IGNORECASE)
def screener(message, filters):
    df = finviz_client.screener(filters=filters.split(","))
    filename = f"{filters.replace(',', '_')}screener.html"
    utils.store_html(df.to_html(classes="table table-striped"), filename)
    utils.send_webapi(
        message,
        "",
        title="FinViz Screener Results",
        title_link=utils.html_url(filename),
    )


@respond_to("ticker-performance (.*)", re.IGNORECASE)
def ticker_performance(message, ticker):
    df = finviz_client.finviz_performance(ticker=ticker)
    filename = f"{ticker}_performance.html"
    utils.store_html(df.to_html(classes="table table-striped"), filename)
    utils.send_webapi(
        message,
        "",
        title=f"Performance for {ticker}",
        title_link=utils.html_url(filename),
    )


@respond_to("ticker-overview (.*)", re.IGNORECASE)
def ticker_overview(message, ticker):
    df = finviz_client.finviz_overview(ticker=ticker)
    filename = f"{ticker}_overview.html"
    utils.store_html(df.to_html(classes="table table-striped"), filename)
    utils.send_webapi(
        message, "", title=f"Overview for {ticker}", title_link=utils.html_url(filename)
    )


@respond_to("ticker-technical (.*)", re.IGNORECASE)
def ticker_technical(message, ticker):
    df = finviz_client.finviz_technical(ticker=ticker)
    filename = f"{ticker}_technical.html"
    utils.store_html(df.to_html(classes="table table-striped"), filename)
    utils.send_webapi(
        message,
        "",
        title=f"Technical for {ticker}",
        title_link=utils.html_url(filename),
    )


@respond_to("ticker-ownership (.*)", re.IGNORECASE)
def ticker_ownership(message, ticker):
    df = finviz_client.finviz_ownership(ticker=ticker)
    filename = f"{ticker}_ownership.html"
    utils.store_html(df.to_html(classes="table table-striped"), filename)
    utils.send_webapi(
        message,
        "",
        title=f"Ownership for {ticker}",
        title_link=utils.html_url(filename),
    )


@respond_to("ticker-financial (.*)", re.IGNORECASE)
def ticker_financial(message, ticker):
    df = finviz_client.finviz_financial(ticker=ticker)
    utils.store_html(
        df.to_html(classes="table table-striped"), f"{ticker}_financial.html"
    )
    utils.send_webapi(
        message,
        "",
        title=f"Financials for {ticker}",
        title_link=utils.html_url(f"{ticker}_financial.html"),
    )


@respond_to("insider (.*)", re.IGNORECASE)
def insider(message, ticker):
    insider = finviz_client.finviz_get_insider(ticker)
    df = pd.DataFrame(insider)
    filename = f"{ticker}_insider.html"
    utils.store_html(df.to_html(classes="table table-striped"), filename)
    utils.send_webapi(
        message, "", title=f"Insider for {ticker}", title_link=utils.html_url(filename)
    )
