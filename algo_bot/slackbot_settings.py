from algo_bot.settings import AlgoBotSettings, get_settings

settings: AlgoBotSettings = get_settings()

DEFAULT_REPLY = "Sorry but I didn't understand you"
BOT_EMOJI = ":robot_face:"
PLUGINS = [
    "slackbot.plugins",
    "algo_bot.commands.finviz",
    "algo_bot.commands.help",
    "algo_bot.commands.news",
    "algo_bot.commands.technical",
    "algo_bot.commands.ticker",
    "algo_bot.commands.user",
    "algo_bot.commands.screener",
    "algo_bot.commands.strategies",
]


BOT_ENV = settings.bot_env
ERRORS_TO = "errors"
