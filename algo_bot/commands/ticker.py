import json
import re

from slackbot.bot import respond_to

from algo_bot import charting
from algo_bot.clients import alpha_vantage_client
from algo_bot.commands import utils


@respond_to("candlestick (.*)", re.IGNORECASE)
def candlestick(message, ticker, interval="60min"):
    utils.processing(message)
    time_series = alpha_vantage_client.time_series_intraday(ticker, interval=interval)
    fig = charting.candlestick_plot(time_series)
    filename = f"{ticker}_candlestick.html"
    utils.store_graph(fig, filename)
    message.send_webapi(
        "",
        json.dumps(
            utils.attachments(
                message,
                title=f"Candlestick Chart For {ticker}",
                title_link=utils.html_url(filename),
            )
        ),
    )


@respond_to("ticker (.*)", re.IGNORECASE)
def ticker(message, ticker):
    df = alpha_vantage_client.company_overview(ticker)
    filename = f"{ticker}_overview.html"
    utils.store_html(df.to_html(classes="table table-striped"), filename)
    message.send_webapi(
        "",
        json.dumps(
            utils.attachments(
                message,
                text=df["Description"][0],
                title=f"Overview for {ticker}",
                title_link=utils.html_url(filename),
            )
        ),
    )


@respond_to("ticker-top5 (.*)", re.IGNORECASE)
def ticker_top(message, ticker):
    df = alpha_vantage_client.time_series_daily(ticker).head()
    message.reply(utils.wrap_ticks_tabluate(df))