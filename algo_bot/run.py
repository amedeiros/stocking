import atexit

from slackbot.bot import Bot

bot = Bot()
# NO CLUE WHY THIS IS NOT WORKING FROM SETTINGS
bot._client.icon_emoji = ":robot_face:"


def goodbye():
    bot._client.send_message("#general", "Shutting down...", as_user=False)


def main():
    print("Starting!")
    atexit.register(goodbye)
    bot._client.send_message("#general", "Starting...", as_user=False)
    bot.run()


if __name__ == "__main__":
    main()
