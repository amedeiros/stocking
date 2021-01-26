import re
import shlex
import argparse
from slackbot.bot import respond_to

from algo_bot.db.models import User
from sqlalchemy.exc import IntegrityError

USER_PARSER = argparse.ArgumentParser()
USER_PARSER.add_argument("--email", type=str)
USER_PARSER.add_argument("--first_name", type=str)
USER_PARSER.add_argument("--last_name", type=str)

@respond_to("user-new (.*)", re.IGNORECASE)
def register(message, params):
    try:
        params = shlex.split(params)
        args = USER_PARSER.parse_args(params)

        if "<mailto:" in args.email:
            email = args.email.replace("<mailto:", "").replace(">", "").split("|")[0]
        else:
            email = args.email

        user = User.create(
            slack=message.user["id"],
            timezone=message.user["tz"],
            email=email,
            first_name=args.first_name,
            last_name=args.last_name,
        )
        message.reply("Success!")
    except IntegrityError:
        message.reply("You already have an account!")
