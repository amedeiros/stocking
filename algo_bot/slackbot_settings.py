import os

DEFAULT_REPLY = "Sorry but I didn't understand you"

PLUGINS = [
    "slackbot.plugins",
    "algo_bot.commands.finviz",
    "algo_bot.commands.help",
    "algo_bot.commands.news",
    "algo_bot.commands.technical",
    "algo_bot.commands.ticker",
    "algo_bot.commands.user",
]


BOT_ENV = os.environ.get("BOT_EMV") or "development"
ERRORS_TO = "errors"
