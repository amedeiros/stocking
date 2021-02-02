import argparse
import re

from slackbot.bot import respond_to

from algo_bot import utils
from algo_bot.db.models import Screener
from algo_bot.strategies import risk

RUN_STRATEGY_PARSER = argparse.ArgumentParser()
RUN_STRATEGY_PARSER.add_argument("--screener-id", type=int, required=True)


@respond_to("^strategy-risk-vs-reward (.*)", re.IGNORECASE)
@utils.auth
@utils.parse_params(parser=RUN_STRATEGY_PARSER)
def run_strategy_risk_vs_reward(message, params):
    user = message.user["db_user"]
    screener = Screener.find(params.screener_id)

    if screener and screener.user == user:
        url = risk.risk_expected_return_std_deviation(screener)
        utils.send_webapi(
            message,
            "",
            title=f"Results for risk vs reward using screener: {screener.name}",
            title_link=url,
        )
    else:
        utils.reply_webapi(
            message, "Error: Screener not found or does not belong to you!"
        )


@respond_to("^strategy-turtle (.*)")
@utils.auth
def run_strategy_turtle(message, params):
    pass
    # user = message.user["db_user"]
