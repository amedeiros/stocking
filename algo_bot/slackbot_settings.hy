(import [algo_bot.settings [AlgoBotSettings get_settings]])

(setv ^AlgoBotSettings settings (get_settings))

(setv DEFAULT_REPLY "Sorry but I didn't understand you")
(setv BOT_EMOJI ":robot_face:")
(setv PLUGINS [
    "slackbot.plugins"
    "algo_bot.commands.finviz"
    "algo_bot.commands.help"
    "algo_bot.commands.news"
    "algo_bot.commands.technical"
    "algo_bot.commands.ticker"
    "algo_bot.commands.user"
    "algo_bot.commands.screener"
    "algo_bot.commands.strategies"
    "algo_bot.commands.positioning"])
(setv BOT_ENV settings.bot_env)
(setv ERRORS_TO "errors")
