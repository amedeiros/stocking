(import [algo_bot.settings [AlgoBotSettings get_settings]])

(setv ^AlgoBotSettings settings (get_settings))

(setv DEFAULT_REPLY "Sorry but I didn't understand you")
(setv BOT_EMOJI ":robot_face:")
(setv PLUGINS ["slackbot.plugins" "algo_bot.commands.all"])
(setv BOT_ENV settings.bot_env)
(setv ERRORS_TO "errors")
