import pandas as pd
import datetime
from TechnicalIndicators.TechincalIndicators import historical_vol
import numpy as np
import math


def calculate_factors(dates, prices):
    # this function takes the dataframe of earnings dates and the df of prices
    # adds the movement at each earnings, median 180hv and 60hv, and year range indicator
    # returns the final df

    results = []
    tot = 0
    beat = 0
    for index, row in dates.iterrows():
        ticker = row['Ticker']
        date = row['Dates']

        date_test = datetime.datetime.strptime(date, "%Y-%m-%d")

        if date_test.weekday() == 0:
            day_before = date_test - datetime.timedelta(days=3)
        else:
            day_before = date_test - datetime.timedelta(days=1)

        year_before = date_test - datetime.timedelta(days=365)

        year_before = year_before.strftime("%Y-%m-%d")

        day_before = day_before.strftime("%Y-%m-%d")

        try:
            # get prices for the current ticker
            px = prices.loc[ticker,]
            day_of = px.loc[date]
            before = px.loc[day_before]

            # calculate move on earnings
            move = abs(day_of['close'] - before['close'])

            px_move = (move / before['close']) * 100.0

            year_data = px[year_before:date]

            cur_rng = range_indicator(year_data['close'], day_of['close'])

            # get median 60 and 180 hv
            hv180 = np.nanmedian(historical_vol(year_data['close'], 180)) * 100
            hv60 = np.nanmedian(historical_vol(year_data['close'], 60)) * 100
            beat = beat_vol(px_move, hv60)

            res = (ticker, date, move, px_move, cur_rng, hv60, hv180, beat)

            results.append(res)

        except:
            continue

    res_data_frame = pd.DataFrame(results, columns=['ticker', 'date', 'dollar_move', 'px_move',
                                                    'rng_indicator', 'hv60', 'hv180', 'beat'])

    return res_data_frame


def beat_vol(move, hv60):
    # return 1 if the move was greater than 1.25 historical vol move fro one day
    day_hv = hv60 * 1 / math.sqrt(255)
    day_hv *= 1.25
    print("day_hv", day_hv, "Move", move)
    if move > day_hv:
        return 1
    return 0


def range_indicator(pxs, cur):
    max_price = max(pxs)
    min_price = min(pxs)

    cur_rng = abs(cur - min_price) / max_price
    return cur_rng


def prep_data():
    earnings_dates = pd.read_csv('./Data/EarningsDatesClean.csv')

    prices = pd.read_csv("./Data/EarningsPrices.csv")

    prices['date'] = pd.to_datetime(prices['date'])

    earnings_dates.index = pd.to_datetime(earnings_dates['Dates'])

    prices.set_index(['ticker', 'date'], inplace=True, drop=True)

    return earnings_dates, prices


def get_factors(earnings_dates, prices):
    res_df = calculate_factors(earnings_dates, prices)

    res_df.to_csv("earnings_movements.csv")


if __name__ == '__main__':
    dates, pxs = prep_data()
    get_factors(dates, pxs)
