import os

from celery.decorators import task
from slack_sdk import WebClient

from algo_bot import utils
from algo_bot.db.models import User

CLIENT = WebClient(token=os.environ.get("SLACKBOT_API_TOKEN"))


@task()
def respond_file_link(user_id, text, title, filename):
    user = User.find(user_id)
    if not user:
        raise RuntimeError(f"Unknown user id {user_id}.")

    url = utils.html_url(filename)
    attachments = [
        {
            "author_name": f"{user.first_name} {user.last_name}",
            "title_link": url,
            "title": title,
            "text": text,
            "footer": "Stocking Bot 0.1b",
            "fields": [],
        }
    ]
    CLIENT.chat_postMessage(
        channel="#general",
        text=f"<@{user.slack}>",
        username="stockbot",
        icon_emoji=":robot_face:",
        attachments=attachments,
    )
