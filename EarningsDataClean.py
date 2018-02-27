import pandas as pd


def reformat_dates(data):
    new_dates = []
    for row in data['Dates']:
        new_dates.append(slash_to_iso(row))
    data['Dates'] = new_dates
    return data


def slash_to_iso(date):
    date = date.split("/")
    date = '-'.join((date[2], date[0], date[1]))
    return date


if __name__ == '__main__':
    data = pd.read_csv('./EarningsDates.csv')
    data = reformat_dates(data)
    data.to_csv("./EarningsDatesClean.csv")

