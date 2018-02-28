import pandas
import numpy as np


def rsi(prices, window=14):
    # calculate the difference in price from previous close
    delta = prices.diff()
    delta = delta[1:]  # get rid of first as it has no difference

    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    # can be changed to simple moving average with pandas.rolling_mean()
    roll_up1 = pandas.ewma(up, window)
    roll_down1 = pandas.ewma(down.abs(), window)

    rs1 = roll_up1 / roll_down1

    rsi_ewma = 100.0 - (100.0 / (1.0 + rs1))

    return rsi_ewma


def on_balance_volume(close, volume):
    obv = np.zeros(len(close))
    for i in range(1, len(close)):
        if close.loc[i] > close.loc[i - 1]:
            obv[i] = obv[i - 1] + volume.loc[i]
        elif close.loc[i] < close.loc[i - 1]:
            obv[i] = obv[i - 1] - volume.loc[i]
        else:
            obv[i] = obv[i - 1]

    return obv


def historical_vol(prices, window_size):
    return prices.pct_change().rolling(window_size).std() * (252 ** 0.5)
