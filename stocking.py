from alpha_vantage_client import AlphaVantageClient
from charting import *
from finviz_client import *
from predicting import prophet
from fbprophet.plot import plot_plotly  # This returns a plotly Figure
import plotly.offline as py
from trends import *
from datetime import datetime, timedelta
from IPython.core.display import display, HTML

py.init_notebook_mode()


def years_ago(years=1):
    ago = datetime.now() - timedelta(days=years*365)
    return ago.strftime("%Y-%m-%d")


def today():
    return datetime.now().strftime("%Y-%m-%d")


def calc_sma(df, window, min_periods=1):
    return df.rolling(window=window, min_periods=min_periods).mean()
