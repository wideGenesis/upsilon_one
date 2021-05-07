import datetime as dt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from pandas_datareader import data as pdr


# Create our portfolio of equities
tickers = ['AYX']

# Download closing prices
data = pdr.get_data_yahoo(tickers, start="2020-01-29", end=dt.date.today())['Close']

# From the closing prices, calculate periodic returns
# pct = data.pct_change()


# def momentum_rank(prices=None, ticker=None):
#     prices = prices
#     prices = prices[ticker]
#     m20 = ((prices - prices.rolling(20).mean()) / prices.rolling(20).mean()) * 100
#     m50 = ((prices - prices.rolling(50).mean()) / prices.rolling(50).mean()) * 100
#     m200 = ((prices - prices.rolling(200).mean()) / prices.rolling(200).mean()) * 100
#
#     delta = prices.diff()
#     delta = delta[1:]
#     up, down = delta.copy(), delta.copy()
#     up[up < 0] = 0
#     down[down > 0] = 0
#     roll_up1 = up.ewm(span=10).mean()
#     roll_down1 = down.abs().ewm(span=10).mean()
#     rs = roll_up1 / roll_down1
#     rsi = 100.0 - (100.0 / (1.0 + rs))
#
#     rank = (0.25 * m20 + 0.35 * m50 + 0.4 * m200) / rsi
#     print(rank.tail(50))
#     # print(m20, m50, m200)
#     # print(rsi)
#
# momentum_rank(data, 'AYX')

