import plotly.graph_objects as go
import plotly.express as px


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
