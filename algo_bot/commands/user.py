import json
import re

from slackbot.bot import respond_to

from algo_bot.commands import utils
from algo_bot.db.models import User


@respond_to("user register (.*) (.*) (.*)", re.IGNORECASE)
def register(message, email=None, first_name=None, last_name=None):
    user = User.where(slack=message.user["id"]).first()

    if user:
        message.reply("You already have an account!")
    else:
        try:
            user = User.create(
                slack=message.user["id"],
                timezone=message.user["tz"],
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            message.reply("Success!")
        except:
            message.reply("Failed!")
            breakpoint()
