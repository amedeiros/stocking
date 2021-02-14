import argparse

import pandas as pd
from slackbot.bot import respond_to
from sqlalchemy.exc import IntegrityError

from algo_bot import utils
from algo_bot.db.models import Screener

SCREENER_PARSER = argparse.ArgumentParser()
SCREENER_PARSER.add_argument("--name", type=str, required=True)
SCREENER_PARSER.add_argument("--filters", type=str, required=True)
SCREENER_PARSER.add_argument("--cron", type=str)


@respond_to("^screener-new (.*)")
@utils.auth
@utils.parse_params(parser=SCREENER_PARSER)
def new_screener(message, params):
    user = message.user["db_user"]

    try:
        Screener.create(
            name=params.name, user=user, filters=params.filters, cron=params.cron
        )
        utils.reply_webapi(message, f"Succesfully created screener {params.name}.")
    except IntegrityError:
        utils.reply_webapi(message, "Error: Screener already exists!")


@respond_to("^screener-list")
@utils.auth
def screener_list(message):
    user = message.user["db_user"]
    screeners = user.screeners
    df = pd.DataFrame(data=list(map(lambda x: x.to_dict(), screeners))).set_index("id")
    utils.reply_webapi(message, utils.wrap_ticks_tabulate(df))


@respond_to("^screener-run --id (.*)")
@utils.auth
def screener_run(message, id):
    user = message.user["db_user"]
    screener = Screener.find(id)

    if not screener or screener.user != user:
        utils.reply_webapi(message, f"Error: No Screener with ID {id}")
    else:
        df = screener.run()
        filename = f"{screener.name.replace(' ', '_')}_screener.html"
        utils.store_html(df.to_html(classes="table table-striped"), filename)
        utils.send_webapi(
            message,
            "",
            title=f"Screener Results: {screener.name}",
            title_link=utils.html_url(filename),
        )
