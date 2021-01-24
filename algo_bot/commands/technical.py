import json
import re

from slackbot.bot import respond_to

from algo_bot import charting
from algo_bot.clients import alpha_vantage_client
from algo_bot.commands import utils


@respond_to("sector-performance", re.IGNORECASE)
def sector_performance(message):
    utils.processing(message)
    df = alpha_vantage_client.sector_performance()
    fig = charting.sector_performance_chart(df)
    utils.store_graph(fig, "sector_performance.html")
    message.send_webapi(
        "",
        json.dumps(
            utils.attachments(
                message,
                title="Sector Performance",
                title_link=utils.html_url("sector_performance.html"),
            )
        ),
    )


@respond_to("golden-cross (.*)", re.IGNORECASE)
def golden_cross(message, ticker):
    utils.processing(message)
    time_series = alpha_vantage_client.time_series_daily(ticker)
    sma_50 = alpha_vantage_client.sma(ticker)
    sma_200 = alpha_vantage_client.sma(ticker, time_period="200")
    fig = charting.golden_cross(
        start=utils.today(),
        stop=utils.years_ago(),
        df=time_series,
        sma_50=sma_50,
        sma_200=sma_200,
        ticker=ticker,
    )
    utils.store_graph(fig, f"{ticker}_golden_cross.html")
    message.send_webapi(
        "",
        json.dumps(
            utils.attachments(
                message,
                title=f"Golden Cross Chart For {ticker}",
                title_link=utils.html_url(f"{ticker}_golden_cross.html"),
            )
        ),
    )


@respond_to("sma (.*)", re.IGNORECASE)
def sma(message, ticker):
    utils.processing(message)
    sma = alpha_vantage_client.sma(ticker)
    fig = charting.plot_sma(sma)
    filename = f"{ticker}_sma.html"
    utils.store_graph(fig, filename)
    message.send_webapi(
        "",
        json.dumps(
            utils.attachments(
                message,
                title=f"SMA Chart For {ticker}",
                title_link=utils.html_url(filename),
            )
        ),
    )
