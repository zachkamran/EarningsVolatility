import pandas as pd
import datetime


def get_move(dates, prices):
    # this function takes the dataframe of earnings dates and the df of prices and adds the movement to the dates df
    results = []
    e = 0
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
            px = prices.loc[ticker,]
            day_of = px.loc[date]
            before = px.loc[day_before]

            move = abs(day_of['close'] - before['close'])

            px_move = (move / before['close']) * 100.0

            year_data = px[year_before:date]

            max_price = max(year_data['close'])
            min_price = min(year_data['close'])

            cur_rng = abs(day_of['close'] - min_price) / max_price
            print(cur_rng)
            res = (ticker, date, move, px_move, cur_rng)

            results.append(res)
        except:
            e += 1
            print("except num", e)
            continue

    res_data_frame = pd.DataFrame(results, columns=['ticker', 'date', 'dollar_move', 'px_move', 'rng_indicator'])
    return res_data_frame


if __name__ == '__main__':
    earnings_dates = pd.read_csv('./EarningsDatesClean.csv')

    prices = pd.read_csv("./EarningsPrices.csv")

    prices['date'] = pd.to_datetime(prices['date'])

    earnings_dates.index = pd.to_datetime(earnings_dates['Dates'])

    prices.set_index(['ticker', 'date'], inplace=True, drop=True)

    res_df = get_move(earnings_dates, prices)

    res_df.to_csv("earnings_movements.csv")
