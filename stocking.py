from dataclasses import dataclass
from datetime import datetime, timedelta

import pandas as pd
import plotly.offline as py
from fbprophet.plot import plot_plotly  # This returns a plotly Figure
from IPython.core.display import HTML, display

from alpha_vantage_client import *
from charting import *
from finviz_client import *
from predicting import prophet
from trends import *

py.init_notebook_mode()


@dataclass
class Positioning:
    position_size: int
    max_loss_per_share: float
    total_risk: float
    total_gain: float
    profit: float
    purchase_cost: float
    risk_reward_ratio: float


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


def _round_down(num, divisor=10):
    return num - (num % divisor)
