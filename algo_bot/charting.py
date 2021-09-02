import matplotlib.pyplot as plt
import plotly.graph_objects as go
from algo_bot import utils


def candlestick_plot(df):
    return go.Figure(
        data=[
            go.Candlestick(
                x=list(df.index),
                open=df["1. open"],
                high=df["2. high"],
                low=df["3. low"],
                close=df["4. close"],
                name="Candlestick",
            ),
            go.Scatter(
                x=list(df.index), y=df["5. volume"], name="Volume", mode="lines",
            ),
        ]
    )


def line_chart_trends(df):
    fig = go.Figure()

    for column in df.columns:
        if column != "isPartial":
            fig.add_trace(
                go.Scatter(x=df.index, y=df[column], mode="lines+markers", name=column)
            )

    return fig


def plot_sma(df):
    return go.Figure(
        data=[go.Scatter(x=list(df.index), y=df["SMA"], name="SMA", mode="lines",)]
    )

def sector_performance_chart(df):
    fig = go.Figure(
        data=[go.Bar(x=list(df.index), y=df["Rank A: Real-Time Performance"])]
    )

    fig.update_layout(legend_title_text="Sector")
    fig.update_xaxes(title_text="Sectors")
    fig.update_yaxes(title_text="Rank A: Real-Time Performance")

    return fig


def golden_cross(start, stop, df, sma_50, sma_200, ticker):
    sma_200 = sma_200.sort_values(by="date", ascending=False)
    sma_50 = sma_50.sort_values(by="date", ascending=False)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df.loc[start:stop, :].index, y=df.loc[start:stop, "1. open"], name="price"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=sma_200.loc[start:stop, :].index,
            y=sma_200.loc[start:stop, "SMA"],
            name="SMA-200",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=sma_50.loc[start:stop, :].index,
            y=sma_50.loc[start:stop, "SMA"],
            name="SMA-50",
        )
    )

    fig.update_layout(title_text=ticker, xaxis_rangeslider_visible=True)

    return fig


def predicted_price(start, stop, price, predicted_price, ticker):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=price.loc[start:stop, :].index,
            y=price.loc[start:stop, "close"],
            name="price",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=predicted_price.loc[utils.years_from_now():start, :].index,
            y=predicted_price.loc[utils.years_from_now():start, "yhat"],
            name="predicted price",
        )
    )

    fig.update_layout(title_text=ticker, xaxis_rangeslider_visible=True)
    return fig


def predicted_golden_cross(
    start,
    stop,
    price,
    predicted_price,
    sma_50,
    predicted_50,
    sma_200,
    predicted_200,
    ticker,
):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=price.loc[start:stop, :].index,
            y=price.loc[start:stop, "close"],
            name="price",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=predicted_price.loc[start:stop, :].index,
            y=predicted_price.loc[start:stop, "yhat"],
            name="predicted price",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=predicted_50.loc[start:stop, :].index,
            y=predicted_50.loc[start:stop, "yhat"],
            name="Predicted SMA-50",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=predicted_200.loc[start:stop, :].index,
            y=predicted_200.loc[start:stop, "yhat"],
            name="Predicted SMA-200",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=sma_50.loc[start:stop, :].index,
            y=sma_50.loc[start:stop, "sma"],
            name="SMA-50",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=sma_200.loc[start:stop, :].index,
            y=sma_200.loc[start:stop, "sma"],
            name="SMA-200",
        )
    )

    fig.update_layout(title_text=ticker, xaxis_rangeslider_visible=True)

    return fig


def risk_vs_return(df, s):
    fig = plt.figure()
    plt.scatter(df.mean(), df.std(), alpha=0.5, s=s)

    plt.xlabel("Expected returns")
    plt.ylabel("Risk")

    for label, x, y in zip(df.columns, df.mean(), df.std()):
        plt.annotate(
            label,
            xy=(x, y),
            xytext=(50, 30),
            textcoords="offset points",
            ha="right",
            va="bottom",
            arrowprops=dict(arrowstyle="-", connectionstyle="arc3,rad=0.5"),
        )

    return fig
