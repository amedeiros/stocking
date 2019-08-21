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


def golden_cross(start, stop, df, sma_50, sma_200, ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.loc[start:stop, :].index, y=df.loc[start:stop, 'open'], name='price'))

    fig.add_trace(go.Scatter(
        x=sma_200.loc[start:stop, :].index, y=sma_200.loc[start:stop, 'sma'], name='SMA-200'))
    fig.add_trace(go.Scatter(
        x=sma_50.loc[start:stop, :].index, y=sma_50.loc[start:stop, 'sma'], name='SMA-50'))

    fig.update_layout(title_text=ticker, xaxis_rangeslider_visible=True)

    return fig


def predicted_golden_cross(start, stop, price, predicted_price, sma_50, predicted_50, sma_200, predicted_200, ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=price.loc[start:stop, :].index, y=price.loc[start:stop, 'open'], name="price"))
    fig.add_trace(go.Scatter(x=predicted_price.loc[start:stop, :].index,
                             y=predicted_price.loc[start:stop, 'yhat'], name="predicted price"))

    fig.add_trace(go.Scatter(x=predicted_50.loc[start:stop, :].index,
                             y=predicted_50.loc[start:stop, 'yhat'], name='Predicted SMA-50'))
    fig.add_trace(go.Scatter(x=predicted_200.loc[start:stop, :].index,
                             y=predicted_200.loc[start:stop, 'yhat'], name='Predicted SMA-200'))

    fig.add_trace(go.Scatter(
        x=sma_50.loc[start:stop, :].index, y=sma_50.loc[start:stop, 'sma'], name='SMA-50'))
    fig.add_trace(go.Scatter(
        x=sma_200.loc[start:stop, :].index, y=sma_200.loc[start:stop, 'sma'], name='SMA-200'))

    fig.update_layout(title_text=ticker, xaxis_rangeslider_visible=True)

    return fig
