import json
import re

import pandas as pd
from slackbot.bot import respond_to

from algo_bot import charting
from algo_bot.clients import finviz_client, trends
from algo_bot.commands import utils


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
    utils.processing(message)
    interest = trends.interest_over_time(ticker)
    df = pd.DataFrame(interest)
    fig = charting.line_chart_trends(df)
    filename = f"{ticker}_interest_over_time.html"
    utils.store_graph(fig, filename)
    message.send_webapi(
        "",
        json.dumps(
            utils.attachments(
                message,
                title=f"Interest Over Time: {ticker}",
                title_link=utils.html_url(filename),
            )
        ),
    )


def _get_news_urls(ticker):
    urls = []
    table = finviz_client.finviz_get_news(ticker)
    for _, url in table.head().iterrows():
        urls.append(url["Link"])
    return urls
