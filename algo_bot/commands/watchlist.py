import argparse
import re

import pandas as pd
from slackbot.bot import respond_to
from sqlalchemy.exc import IntegrityError

from algo_bot import utils
from algo_bot.db.models import Watchlist

WATCHLIST_NEW_PARSER = argparse.ArgumentParser()
WATCHLIST_NEW_PARSER.add_argument("--name", type=str, required=True)
WATCHLIST_NEW_PARSER.add_argument("--ticker", type=str, required=True)

WATCHLIST_UPDATE = argparse.ArgumentParser()
WATCHLIST_UPDATE.add_argument("--id", type=int, required=True)
WATCHLIST_UPDATE.add_argument("--ticker", type=str, required=True)


@respond_to("^watchlist-new (.*)", re.IGNORECASE)
@utils.auth
@utils.parse_params(parser=WATCHLIST_NEW_PARSER)
def new_watchlist(message, params):
    user = message.user["db_user"]
    try:
        Watchlist.create(name=params.name, tickers=params.ticker, user=user)
        utils.reply_webapi(message, f"Succesfully created watchlist {params.name}.")
    except IntegrityError:
        utils.reply_webapi(message, "Error: Watchlist already exists!")


@respond_to("^watchlist-list")
@utils.auth
def list_watchlists(message):
    user = message.user["db_user"]
    watchlists = user.watchlists
    if len(watchlists) == 0:
        utils.reply_webapi(message, "You have no watchlists.")
        return
    df = pd.DataFrame(data=list(map(lambda x: x.to_dict(), watchlists))).set_index("id")
    utils.reply_webapi(message, utils.wrap_ticks_tabulate(df))


@respond_to("^watchlist-add-ticker (.*)", re.IGNORECASE)
@utils.auth
@utils.parse_params(parser=WATCHLIST_UPDATE)
def watchlist_add_ticker(message, params):
    user = message.user["db_user"]
    watchlist = Watchlist.where(id=params.id, user_id=user.id).first()

    if watchlist:
        watchlist.add_ticker(params.ticker)
        utils.reply_webapi(message, f"Updated watchlist {watchlist.name}.")
    else:
        utils.reply_webapi(message, "You do not own a watchlist with that id!")


@respond_to("^watchlist-del-ticker (.*)", re.IGNORECASE)
@utils.auth
@utils.parse_params(parser=WATCHLIST_UPDATE)
def watchlist_del_ticker(message, params):
    user = message.user["db_user"]
    watchlist = Watchlist.where(id=params.id, user_id=user.id).first()

    if watchlist:
        watchlist.del_ticker(params.ticker)
        utils.reply_webapi(message, f"Updated watchlist {watchlist.name}.")
    else:
        utils.reply_webapi(message, "You do not own a watchlist with that id!")


@respond_to("^watchlist-view --id (.*)", re.IGNORECASE)
@utils.auth
def watchlist_view(message, watchlist_id):
    user = message.user["db_user"]
    watchlist = Watchlist.where(id=watchlist_id, user_id=user.id).first()

    if watchlist:
        latest = watchlist.latest()
        utils.reply_webapi(message, utils.wrap_ticks_tabulate(latest))
    else:
        utils.reply_webapi(message, "You do not own a watchlist with that id!")
