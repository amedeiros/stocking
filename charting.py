import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def candlestick_plot(df):
    fig = go.Figure(data=[go.Candlestick(x=df['dates'],
                                         open=df['open'],
                                         high=df['high'],
                                         low=df['low'],
                                         close=df['close'])])
    return fig


def line_chart_trends(df):
    fig = go.Figure()

    for column in df.columns:
        if column != 'isPartial':
            fig.add_trace(go.Scatter(
                x=df.index, y=df[column], mode="lines+markers", name=column))

    return fig


def golden_cross(start, stop, df, sma_50, sma_200, ticker):
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.plot(df.loc[start:stop, :].index,
            df.loc[start:stop, 'open'], label='price')
    ax.plot(sma_200.loc[start:stop, :].index,
            sma_200.loc[start:stop, 'sma'], label='200-days SMA')
    ax.plot(sma_50.loc[start:stop, :].index,
            sma_50.loc[start:stop, 'sma'], label='50-days SMA')
    ax.set_ylabel(ticker + ' Price in $')
    ax.legend(loc='best')
    return fig
