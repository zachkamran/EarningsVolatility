import pandas as pd
import requests
from bs4 import BeautifulSoup
import quandl
import sys


def quandl_data(api_key, tickers, start_date=None, end_date=None):
    start_date = "2014-10-00"
    end_date = "2018-01-17"
    quandl.ApiConfig.api_key = api_key  # put your API key here
    table = quandl.get_table('WIKI/PRICES',
                             qopts={'columns': ['date', 'ticker', 'open', 'high', 'low', 'close', 'volume']},
                             date={'gte': start_date, 'lte': end_date}, ticker=tickers, paginate=True)

    table.to_csv("./EarningsPrices.csv")
    return table


def getEarningsDates(tickers):
    url = 'http://www.nasdaq.com/earnings/report/'
    stocks = []
    dates = []
    eps = []
    epsForcasted = []
    # print(tickers)

    for stock in tickers:
        cur_url = url + stock.lower()
        try:
            req = requests.get(cur_url)

            soup = BeautifulSoup(req.text, 'html.parser')
            earningsTable = soup.find("div", {"id": "showdata-div"}).find("table")
            rows = earningsTable.findAll('tr')

        except:
            continue

        for tr in rows[1:]:
            cols = tr.findAll('td')
            stocks.append(stock)
            dates.append(cols[1].string)
            eps.append(cols[2].string)
            epsForcasted.append(cols[3].string)

    df = pd.DataFrame.from_items([('Ticker', stocks),
                                  ('Dates', dates),
                                  ("EPS", eps),
                                  ("EpsForcasted", epsForcasted)])

    return df


def read_tickers(fname):
    colnames = ['ticker', 'none']
    data = pd.read_csv(fname, names=colnames)
    return data.ticker.tolist()


if __name__ == '__main__':
    symbols = read_tickers('./earnings_tickers.csv')
    if len(sys.argv) > 0:
        key = sys.argv[1]
        data = quandl_data(symbols)

    dates = getEarningsDates(symbols)  # example stock

    dates.to_csv("new_earnings_dates.csv")
