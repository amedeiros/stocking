from alpha_vantage_client import AlphaVantageClient
from charting import *
from finviz_client import *
from predicting import prophet
from fbprophet.plot import plot_plotly  # This returns a plotly Figure
import plotly.offline as py
from trends import *
py.init_notebook_mode()
