import argparse
import re
import shlex

from slackbot.bot import respond_to
from sqlalchemy.exc import IntegrityError

from algo_bot import cache, utils
from algo_bot.db.models import User

USER_PARSER = argparse.ArgumentParser()
USER_PARSER.add_argument("--email", type=str)
USER_PARSER.add_argument("--first_name", type=str)
USER_PARSER.add_argument("--last_name", type=str)


@respond_to("^delete-cache", re.IGNORECASE)
@utils.auth
def delete_cache(message):
    utils.reply_webapi(message, f"Cache Delete?: {cache.REDIS_CLIENT.flushdb()}")


@respond_to("user-new (.*)", re.IGNORECASE)
def register(message, params):
    try:
        params = shlex.split(params)
        args = USER_PARSER.parse_args(params)

        if "<mailto:" in args.email:
            email = args.email.replace("<mailto:", "").replace(">", "").split("|")[0]
        else:
            email = args.email

        User.create(
            slack=message.user["id"],
            timezone=message.user["tz"],
            email=email,
            first_name=args.first_name,
            last_name=args.last_name,
        )
        utils.reply_webapi(message, "Success!")
    except IntegrityError:
        utils.reply_webapi(message, "You already have an account!")
