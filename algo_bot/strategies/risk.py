import numpy as np
import pandas as pd

from algo_bot import charting, utils
from algo_bot.clients import alpha_vantage_client as avc
from algo_bot.db.models import Screener

# Scatter plot of expected return of the stocks vs. their standard deviations of daily retunrs
AREA = np.pi * 20


def risk_expected_return_std_deviation(screener: Screener, limit=5):
    results = screener.run().head(limit)
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
    return utils.image_url(filename)
