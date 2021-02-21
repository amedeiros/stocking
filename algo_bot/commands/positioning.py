import argparse
import re

from slackbot.bot import respond_to

from algo_bot import utils

POSITION_PARSER = argparse.ArgumentParser()
POSITION_PARSER.add_argument("--risk", type=float, required=True)
POSITION_PARSER.add_argument("--price", type=float, required=True)
POSITION_PARSER.add_argument("--exit", type=float, required=True)
POSITION_PARSER.add_argument("--stop", type=float, required=True)


@respond_to("positioning-long (.*)", re.IGNORECASE)
@utils.parse_params(parser=POSITION_PARSER)
def position_long(message, params):
    r = utils.position_sizing_long(params.risk, params.price, params.stop, params.exit)
    utils.reply_webapi(message, utils.wrap_ticks_tabulate(r.to_df()))
