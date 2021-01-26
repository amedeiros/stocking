import re
import shlex
import argparse
from slackbot.bot import respond_to

from algo_bot.db.models import Screener, User
from sqlalchemy.exc import IntegrityError

SCREENER_PARSER = argparse.ArgumentParser()
SCREENER_PARSER.add_argument("--name", type=str, required=True)
SCREENER_PARSER.add_argument("--filters", type=str, required=True)
SCREENER_PARSER.add_argument("--cron", type=str)


@respond_to("^screener-new (.*)")
def new_screener(message, params):
    user = User.where(slack=message.user["id"]).first()

    if user:
        try:
            params = shlex.split(params)
            args = SCREENER_PARSER.parse_args(params)
            Screener.create(name=args.name, user=user, filters=args.filters, cron=args.cron)
            message.reply(f"Succesfully created screener {args.name}.")
        except IntegrityError as exc:
            message.reply(f"Error: Screener already exists!")
    else:
        message.reply("Error: Must have a user account!")
