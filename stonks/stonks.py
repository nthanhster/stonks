'''Activision Blizzard, ATVI, 28/9/2018, 83.19 USD'''

import yfinance as yf
import pandas as pd
import numpy as np
# ticker_format = yf.Ticker("ATVI")
pattern_date_time = "([0-9]{4}-[0-9]{2}-[0-9]{2})"


def average(data):
    sum = 0
    for i in data:
        sum += i
    return sum/len(data)


def ma(data, moving_window):
    ma = []
    for i in range(len(data) - moving_window + 1):
        calc = []
        for j in range(i, moving_window + i):
            calc.append(data[j])
        ma.append(average(calc))
    return ma


class Stonk:
    def __init__(self, ticker='ATVI', from_date="2016-01-01", to_date='2019-01-01', mov_window='30'):
        self.ticker = str(ticker)
        self.from_date = str(from_date)
        self.to_date = str(to_date)
        self.date_series = None
        self.close_series = None
        self.mov_window = int(mov_window)
        #self.mavg_time_series = np.array(ma(self.close, self.mov_window))
        self.get_market_data()

    def __str__(self):
        return self.ticker

    def __repr__(self):
        return self.ticker

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):

        return self.ticker < other.ticker

    def get_market_data(self):
        df = yf.download(self.ticker, start=self.from_date, end=self.to_date, prepost=True)
        self.date_series = np.column_stack(df.index.values)
        self.close_series = np.column_stack(df['Close'].values)

if __name__ == '__main__':
    #testing
    a = yf.Ticker("AAPL")
    print(a)



