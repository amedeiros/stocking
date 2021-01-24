import re

from slackbot.bot import respond_to

from algo_bot.db.models import User
from sqlalchemy.exc import IntegrityError


@respond_to("user register (.*) (.*) (.*)", re.IGNORECASE)
def register(message, email=None, first_name=None, last_name=None):
    try:
        user = User.create(
            slack=message.user["id"],
            timezone=message.user["tz"],
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        message.reply("Success!")
    except IntegrityError:
        message.reply("You already have an account!")
