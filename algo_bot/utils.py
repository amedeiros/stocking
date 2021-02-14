import json
import os
import shlex
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import wraps

import boto3
import pandas as pd
import plotly
from tabulate import tabulate

from algo_bot.db.models import User
from algo_bot.slackbot_settings import BOT_ENV


@dataclass
class Positioning:
    position_size: int
    max_loss_per_share: float
    total_risk: float
    total_gain: float
    profit: float
    purchase_cost: float
    risk_reward_ratio: float

    def to_df(self):
        return pd.DataFrame(data=[self.to_dict()])

    def to_dict(self):
        return {
            "position_size": self.position_size,
            "max_loss_per_share": self.max_loss_per_share,
            "total_risk": self.total_risk,
            "total_gain": self.total_gain,
            "profit": self.profit,
            "purchase_cost": self.purchase_cost,
            "risk_reward_ratio": self.risk_reward_ratio,
        }


def attachments(
    message, title, title_link, footer="Stocking Bot 0.1b", text=None, fields=[]
):
    return [
        {
            "author_name": message.user["profile"]["real_name"],
            "title_link": title_link,
            "title": title,
            "color": f"#{message.user['color']}",
            "text": text,
            "footer": footer,
            "fields": fields,
        }
    ]


def wrap_ticks(message):
    return """\n```\n%s\n```""" % (message)


def wrap_ticks_tabulate(df, headers="keys", tablefmt="pipe"):
    return wrap_ticks(tabulate(df, headers=headers, tablefmt=tablefmt))


def processing(message):
    message.reply("Processing...")


def html_url(name, bucket="stocks-am"):
    return boto3.client("s3").generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": bucket,
            "Key": name,
            "ResponseContentType": "text/html",
        },
    )


def image_url(name, bucket="stocks-am"):
    return boto3.client("s3").generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": bucket,
            "Key": name,
            "ResponseContentType": "image/png",
        },
    )


def store_html(html, name, bucket="stocks-am"):
    f = open("templates/%s" % name, "w")
    f.write(
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">\n'
    )
    f.write(
        '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>\n'
    )
    f.write(
        '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>\n'
    )
    f.write(html)
    f.close()
    s3 = boto3.resource("s3")
    s3.Object(bucket, name).put(Body=open("templates/%s" % name, "rb"))


def store_pyplat_graph(fig, name, bucket="stocks-am"):
    if BOT_ENV == "development":
        filename = f"./templates/{name}"
        fig.savefig(filename)
        s3 = boto3.resource("s3")
        s3.Object(bucket, name).put(Body=open(filename, "rb"))
        os.remove(filename)
    else:
        raise RuntimeError("Unknown environment %s" % BOT_ENV)


def store_graph(fig, name, bucket="stocks-am"):
    if BOT_ENV == "development":
        filename = f"./templates/{name}"
        plotly.offline.plot(fig, filename=filename)
        s3 = boto3.resource("s3")
        s3.Object(bucket, name).put(Body=open(filename, "rb"))
        os.remove(filename)
    else:
        raise RuntimeError("Unknown environment %s" % BOT_ENV)


def years_ago(years=1):
    ago = datetime.now() - timedelta(days=years * 365)
    return ago.strftime("%Y-%m-%d")


def today():
    return datetime.now().strftime("%Y-%m-%d")


def years_from_now(years=1):
    future = datetime.now() + timedelta(days=years * 365)
    return future.strftime("%Y-%m-%d")


def postion_sizing_long(risk, price, stop, exit) -> Positioning:
    max_loss_per_share = price - stop
    position_size = _round_down(risk / max_loss_per_share)
    max_gain = position_size * exit
    total_risk = position_size * max_loss_per_share
    cost = position_size * price
    profit = max_gain - cost
    risk_reward_ratio = ((profit / total_risk) * 100) / 100
    return Positioning(
        position_size=position_size,
        max_loss_per_share=max_loss_per_share,
        total_risk=total_risk,
        total_gain=max_gain,
        profit=profit,
        purchase_cost=cost,
        risk_reward_ratio=risk_reward_ratio,
    )


def position_sizing_short(risk, price, stop, exit):
    max_loss_per_share = stop - price
    position_size = _round_down(risk / max_loss_per_share)
    max_gain = position_size * exit
    total_risk = position_size * max_loss_per_share
    cost = position_size * price
    profit = cost - max_gain
    risk_reward_ratio = ((profit / total_risk) * 100) / 100
    return Positioning(
        position_size=position_size,
        max_loss_per_share=max_loss_per_share,
        total_risk=total_risk,
        total_gain=max_gain,
        profit=profit,
        purchase_cost=cost,
        risk_reward_ratio=risk_reward_ratio,
    )


def reply_webapi(message, text):
    message.reply_webapi(text, as_user=False)


def send_webapi(message, text, title, title_link=""):
    message.send_webapi(
        "",
        json.dumps(
            attachments(
                message,
                text=text,
                title=title,
                title_link=title_link,
            )
        ),
        as_user=False,
    )


def _round_down(num, divisor=10):
    return num - (num % divisor)


# Annotations
def auth(func):
    def inner(*args, **kwargs):
        message = args[0]
        processing(message)
        user = User.where(slack=message.user["id"]).first()

        if not user:
            reply_webapi(message, "Error: must create an account!")
        else:
            # After Auth assign the db user object to the message
            # then rewrite the args
            message.user["db_user"] = user
            args = tuple([message]) + args[1:]
            func(*args, **kwargs)

    return inner


def parse_params(parser, *args):
    def inner_function(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # If a parser was supplied parse the params and reasign
            params = args[1]
            params = shlex.split(params)
            params = parser.parse_args(params)
            args = (args[0], params) + args[2:]
            func(*args, **kwargs)

        return wrapper

    return inner_function
