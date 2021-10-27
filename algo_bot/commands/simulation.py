import argparse
import re
import numpy as np
import pandas as pd
from slackbot.bot import respond_to
from algo_bot import utils
from algo_bot.clients import alpha_vantage_client as avc
import matplotlib.pyplot as plt

RUN_SIMULATION_PARSER = argparse.ArgumentParser()
RUN_SIMULATION_PARSER.add_argument("--ticker", type=str, required=True)
RUN_SIMULATION_PARSER.add_argument("--balance", type=float, required=True)
RUN_SIMULATION_PARSER.add_argument("--limit", type=float, required=True)
COLUMN_RENAME = {"date": "Date", "1. open": "Open", "2. high": "High", "3. low": "Low", "4. close": "Close", "5. adjusted close": "Adj Close", "6. volume": "Volume"}


@respond_to("^simulate-turtle (.*)", re.IGNORECASE)
@utils.parse_params(parser=RUN_SIMULATION_PARSER)
def run_turtle_simulation(message, params):
    dailyAdjustedRaw = avc.adjusted(params.ticker)
    df = dailyAdjustedRaw.sort_values(by="date", ascending=False).reset_index().rename(columns=COLUMN_RENAME).drop(["7. dividend amount", "8. split coefficient"], axis=1, inplace=False)
    df = df.head(90).sort_values(by="Date", ascending=True).reset_index().drop(["index"], axis=1, inplace=False)
    signals = turtleSignals(df)
    messages, states_buy, states_sell, total_gains, invest = turtle_buy_stock(df.Close, signals['signal'], df, initial_money=params.balance, max_buy=params.limit, max_sell=params.limit)
    # Reply the simulation
    utils.reply_webapi(message, utils.wrap_ticks("\n".join(messages)))
    # Send the chart
    close = df['Close']
    fig = plt.figure(figsize=(15, 5))
    plt.plot(close, color='r', lw=2.)
    plt.plot(close, '^', markersize=10, color='m', label='buying signal', markevery=states_buy)
    plt.plot(close, 'v', markersize=10, color='k', label='selling signal', markevery=states_sell)
    plt.title('total gains %f, total investment %f%%' % (total_gains, invest))
    plt.legend()
    filename = f"{params.ticker}_turtle_sim.png"
    utils.store_pyplat_graph(fig, filename)
    utils.send_webapi(
        message,
        "",
        title=f"Chart results for turtle simulation {params.ticker}",
        title_link=utils.image_url(filename),
    )


@respond_to("^simulate-moving-average (.*)", re.IGNORECASE)
@utils.parse_params(parser=RUN_SIMULATION_PARSER)
def run_moving_average_simulation(message, params):
    dailyAdjustedRaw = avc.adjusted(params.ticker)
    df = dailyAdjustedRaw.sort_values(by="date", ascending=False).reset_index().rename(columns=COLUMN_RENAME).drop(["7. dividend amount", "8. split coefficient"], axis=1, inplace=False)
    df = df.head(90).sort_values(by="Date", ascending=True).reset_index().drop(["index"], axis=1, inplace=False)
    signals = movingAverageSignals(df)
    messages, states_buy, states_sell, total_gains, invest = moving_average_buy_stock(df.Close, signals['positions'], df, initial_money=params.balance, max_buy=params.limit, max_sell=params.limit)
    # Reply the simulation
    utils.reply_webapi(message, utils.wrap_ticks("\n".join(messages)))
    # Send the chart
    close = df['Close']
    fig = plt.figure(figsize = (15,5))
    plt.plot(close, color='r', lw=2.)
    plt.plot(close, '^', markersize=10, color='m', label = 'buying signal', markevery = states_buy)
    plt.plot(close, 'v', markersize=10, color='k', label = 'selling signal', markevery = states_sell)
    plt.title('total gains %f, total investment %f%%'%(total_gains, invest))
    plt.legend()
    filename = f"{params.ticker}_moving_average_sim.png"
    utils.store_pyplat_graph(fig, filename)
    utils.send_webapi(
        message,
        "",
        title=f"Chart results for moving average simulation {params.ticker}",
        title_link=utils.image_url(filename),
    )


def movingAverageSignals(df):
    short_window = int(0.025 * len(df))
    long_window = int(0.05 * len(df))
    signals = pd.DataFrame(index=df.index)
    signals['signal'] = 0.0

    signals['short_ma'] = df['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_ma'] = df['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

    signals['signal'][short_window:] = np.where(signals['short_ma'][short_window:]
                                                > signals['long_ma'][short_window:], 1.0, 0.0)
    signals['positions'] = signals['signal'].diff()

    return signals


def moving_average_buy_stock(
    real_movement,
    signal,
    df,
    initial_money=10000,
    max_buy=1,
    max_sell=1,
):
    """
    real_movement = actual movement in the real world
    delay = how much interval you want to delay to change our decision from buy to sell, vice versa
    initial_state = 1 is buy, 0 is sell
    initial_money = 1000, ignore what kind of currency
    max_buy = max quantity for share to buy
    max_sell = max quantity for share to sell
    """
    starting_money = initial_money
    states_sell = []
    states_buy = []
    current_inventory = 0
    messages = []

    def buy(i, initial_money, current_inventory):
        shares = initial_money // real_movement[i]
        if shares < 1:
            messages.append(
                'Date: %s day %d: total balances %f, not enough money to buy a unit price %f'
                % (df.Date[i], i, initial_money, real_movement[i])
            )
        else:
            if shares > max_buy:
                buy_units = max_buy
            else:
                buy_units = shares
            initial_money -= buy_units * real_movement[i]
            current_inventory += buy_units
            messages.append(
                'Date: %s day %d: buy %d units at price %f, total balance %f'
                % (df.Date[i], i, buy_units, buy_units * real_movement[i], initial_money)
            )
            states_buy.append(0)
        return initial_money, current_inventory

    for i in range(real_movement.shape[0] - int(0.025 * len(df))):
        state = signal[i]
        if state == 1:
            initial_money, current_inventory = buy(
                i, initial_money, current_inventory
            )
            states_buy.append(i)
        elif state == -1:
            if current_inventory == 0:
                messages.append('Date: %s day %d: cannot sell anything, inventory 0' % (df.Date[i], i))
            else:
                if current_inventory > max_sell:
                    sell_units = max_sell
                else:
                    sell_units = current_inventory
                current_inventory -= sell_units
                total_sell = sell_units * real_movement[i]
                initial_money += total_sell
                try:
                    invest = (
                        (real_movement[i] - real_movement[states_buy[-1]])
                        / real_movement[states_buy[-1]]
                    ) * 100
                except:
                    invest = 0
                messages.append(
                    'Date: %s day %d, sell %d units at price %f, investment %f %%, total balance %f,'
                    % (df.Date[i], i, sell_units, total_sell, invest, initial_money)
                )
            states_sell.append(i)
    invest = ((initial_money - starting_money) / starting_money) * 100
    total_gains = initial_money - starting_money
    return messages, states_buy, states_sell, total_gains, invest


def turtleSignals(df):
    count = int(np.ceil(len(df) * 0.1))
    signals = pd.DataFrame(index=df.index)
    signals['signal'] = 0.0
    signals['trend'] = df['Close']
    signals['RollingMax'] = (signals.trend.shift(1).rolling(count).max())
    signals['RollingMin'] = (signals.trend.shift(1).rolling(count).min())
    signals.loc[signals['RollingMax'] < signals.trend, 'signal'] = -1
    signals.loc[signals['RollingMin'] > signals.trend, 'signal'] = 1
    return signals


def turtle_buy_stock(
    real_movement,
    signal,
    df,
    initial_money=10000,
    max_buy=1,
    max_sell=1,
):
    """
    real_movement = actual movement in the real world
    delay = how much interval you want to delay to change our decision from buy to sell, vice versa
    initial_state = 1 is buy, 0 is sell
    initial_money = 1000, ignore what kind of currency
    max_buy = max quantity for share to buy
    max_sell = max quantity for share to sell
    """
    starting_money = initial_money
    states_sell = []
    states_buy = []
    current_inventory = 0
    messages = []

    def buy(i, initial_money, current_inventory):
        shares = initial_money // real_movement[i]
        if shares < 1:
            messages.append(
                'DATE: %s day %d: total balances %f, not enough money to buy a unit price %f'
                % (df.Date[i], i, initial_money, real_movement[i])
            )
        else:
            if shares > max_buy:
                buy_units = max_buy
            else:
                buy_units = shares
            initial_money -= buy_units * real_movement[i]
            current_inventory += buy_units
            messages.append(
                'DATE: %s day %d: buy %d units at price %f, total balance %f'
                % (df.Date[i], i, buy_units, buy_units * real_movement[i], initial_money)
            )
            states_buy.append(0)
        return initial_money, current_inventory

    for i in range(real_movement.shape[0] - int(0.025 * len(df))):
        state = signal[i]
        if state == 1:
            initial_money, current_inventory = buy(
                i, initial_money, current_inventory
            )
            states_buy.append(i)
        elif state == -1:
            if current_inventory == 0:
                messages.append('DATE: %s day %d: cannot sell anything, inventory 0' % (df.Date[i], i))
            else:
                if current_inventory > max_sell:
                    sell_units = max_sell
                else:
                    sell_units = current_inventory
                current_inventory -= sell_units
                total_sell = sell_units * real_movement[i]
                initial_money += total_sell
                try:
                    invest = (
                        (real_movement[i] - real_movement[states_buy[-1]])
                        / real_movement[states_buy[-1]]
                    ) * 100
                except:
                    invest = 0
                messages.append(
                    'DATE: %s day %d, sell %d units at price %f, investment %f %%, total balance %f,'
                    % (df.Date[i], i, sell_units, total_sell, invest, initial_money)
                )
            states_sell.append(i)

    invest = ((initial_money - starting_money) / starting_money) * 100
    total_gains = initial_money - starting_money
    return messages, states_buy, states_sell, total_gains, invest
