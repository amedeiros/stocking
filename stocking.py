from alpha_vantage_client import AlphaVantageClient
from charting import *
from finviz_client import *
from predicting import prophet
from fbprophet.plot import plot_plotly  # This returns a plotly Figure
import plotly.offline as py
from trends import *
from datetime import datetime, timedelta
from IPython.core.display import display, HTML
import pandas as pd

py.init_notebook_mode()


def years_ago(years=1):
    ago = datetime.now() - timedelta(days=years*365)
    return ago.strftime("%Y-%m-%d")


def today():
    return datetime.now().strftime("%Y-%m-%d")


def postion_sizing(risk, price, stop, exit=1):
    max_loss_per_share = price - stop
    position_size = _round_down(risk / max_loss_per_share)
    max_gain = position_size * exit
    total_risk = position_size * max_loss_per_share
    cost = position_size * price
    df = pd.DataFrame({
        'position_size': [position_size],
        'max_loss_per_share': [max_loss_per_share],
        'total_risk': [total_risk],
        'total_gain': [max_gain],
        'profit': [max_gain - cost],
        'purchase_cost': [cost],
        'risk_reward_ratio': [((max_gain / total_risk) * 100) / 100]})

    return df


def _round_down(num, divisor=10):
    return num - (num % divisor)
