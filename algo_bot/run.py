import asyncio
import json
import re

from slackbot.bot import Bot
# from slackbot_settings import *


def main():
    print("Starting!")
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
