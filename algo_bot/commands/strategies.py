import argparse
import re
import time
from datetime import datetime

import numpy as np
import pandas as pd
from slackbot.bot import respond_to

from algo_bot import cache, charting, utils
from algo_bot.clients import alpha_vantage_client as avc
from algo_bot.db.models import Screener

RUN_STRATEGY_PARSER = argparse.ArgumentParser()
RUN_STRATEGY_PARSER.add_argument("--screener-id", type=int, required=True)

# Scatter plot of expected return of the stocks vs. their standard deviations of daily retunrs
AREA = np.pi * 20

MAX_RECORDS = 10


@respond_to("^strategy-risk-vs-reward (.*)", re.IGNORECASE)
@utils.auth
@utils.parse_params(parser=RUN_STRATEGY_PARSER)
def run_strategy_risk_vs_reward(message, params):
    user = message.user["db_user"]
    screener = Screener.find(params.screener_id)

    if screener and screener.user == user:
        results = screener.run().head(MAX_RECORDS)
        tickers = list(results["Ticker"])
        data = {}
        for ticker in tickers:
            # Grab the close
            data[ticker] = avc.time_series_daily(ticker)["4. close"]

        # Create the DataFrame sorting by date and droping rows with None values.
        df = pd.DataFrame(data=data).sort_values(by="date", ascending=False).dropna()
        fig = charting.risk_vs_return(df, AREA)
        filename = f"{screener.name.replace(' ', '_')}_risk_vs_return.png"
        utils.store_pyplat_graph(fig, filename)
        utils.send_webapi(
            message,
            "",
            title=f"Results for risk vs reward using screener: {screener.name}",
            title_link=utils.image_url(filename),
        )
    else:
        utils.reply_webapi(
            message, "Error: Screener not found or does not belong to you!"
        )


@respond_to("^strategy-turtle (.*)")
@utils.auth
@utils.parse_params(parser=RUN_STRATEGY_PARSER)
def run_strategy_turtle(message, params):
    user = message.user["db_user"]
    screener = Screener.find(params.screener_id)

    if screener and screener.user == user:
        key = f"turtle:{user.id}:{screener.id}:{utils.today()}"
        df = cache.read(key)

        if df is None:
            df = _turtle(screener)
            cache.write(key, df, 60 * 60)

        filename = f"{screener.id}_turtle.html"
        utils.store_html(df.to_html(classes="table table-striped"), filename)
        utils.send_webapi(
            message,
            text="",
            title=f"Turtle Results",
            title_link=utils.html_url(filename),
        )
    else:
        utils.reply_webapi(
            message, "Error: Screener not found or does not belong to you!"
        )


def _turtle(screener):
    results = screener.run().head(MAX_RECORDS)
    tickers = list(results["Ticker"])
    records = []

    for ticker in tickers:
        current_price = None
        current_volume = None
        row = results[results["Ticker"] == ticker]
        try:
            current_price = float(row["Price"].max())
            current_volume = row["Volume"].max()
        except KeyError as exc:
            breakpoint()

        daily = None
        sma_50 = None
        sma_200 = None
        # Last 55 days
        daily = avc.time_series_daily(ticker).head(55)

        # SMA-50 and SMA-200
        sma_50 = avc.sma(ticker).sort_values(by="date", ascending=False).head(55)
        sma_200 = (
            avc.sma(ticker, time_period="200")
            .sort_values(by="date", ascending=False)
            .head(55)
        )

        # Calculate when the golden cross happened.
        # Calcuate are we above the golden cross still.
        golden_cross_days = sma_50[sma_50["SMA"] > sma_200["SMA"]]
        # above_cross = golden_cross_days.loc[golden_cross_days.idxmax()]
        first_cross = golden_cross_days.loc[golden_cross_days.idxmin()]
        first_cross_date = first_cross.idxmax()[0]
        # most_recent_above_date = above_cross.idxmax()[0]
        first_cross_close = daily.loc[first_cross_date]["4. close"]

        # Find the highest close price in the last 55 days
        date = daily["4. close"].idxmax()
        max_row = daily.loc[daily["4. close"].idxmax()]

        # Buy if the cross has happend before today and the sma 50 is still above sma 200
        # buy = (
        #     first_cross_date <= datetime.utcnow()
        #     and datetime.utcnow() >= most_recent_above_date
        # )
        buy = current_price >= first_cross_close
        records.append(
            {
                "ticker": ticker,
                "55 day max date": date,
                "55 day max close": max_row["4. close"],
                "cross date": first_cross_date,
                "cross close value": first_cross_close,
                "current price": current_price,
                "current volume": current_volume,
                "buy?": buy,
            }
        )

    df = pd.DataFrame(records)

    return df


def _retry(callable):
    while True:
        try:
            callable()
        except ValueError as exc:
            print(exc)
            time.sleep(60)
        else:
            break
