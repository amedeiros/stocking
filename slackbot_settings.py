import os

DEFAULT_REPLY = "Sorry but I didn't understand you"

PLUGINS = [
    "slackbot.plugins",
    # 'mybot.plugins',
]


BOT_ENV = os.environ.get("BOT_EMV") or "development"
