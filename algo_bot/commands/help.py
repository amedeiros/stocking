import re

from slackbot.bot import respond_to

from algo_bot.commands import utils
from algo_bot.slackbot_settings import BOT_ENV


@respond_to("^help", re.IGNORECASE)
def help(message):
    response = (
        """
Stocking bot help sub-commands (%s)

    @stockbot manual help (Display manual analysis commands)
    @stockbot user help (Display user commands)
"""
        % BOT_ENV
    )
    message.reply(utils.wrap_ticks(response))


@respond_to("user help", re.IGNORECASE)
def user_help(message):
    response = (
        """
Stocking bot help user commands (%s)

    @stockbot user register EMAIL FIRST_NAME LAST_NAME
    """
        % BOT_ENV
    )
    message.reply(utils.wrap_ticks(response))


@respond_to("manual help", re.IGNORECASE)
def manual(message):
    response = (
        """
Stocking bot help manual analysis (%s)

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
    message.reply(utils.wrap_ticks(response))