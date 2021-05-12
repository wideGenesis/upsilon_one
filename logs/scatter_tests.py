import datetime as dt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde, norm
from pandas_datareader import data as pdr
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf, plot_predict

# Create our portfolio of equities
tickers = ['SPY']

# Download closing prices
n = 10
i = 'd'
data = pdr.get_data_yahoo(tickers, start="2008-08-08", end=dt.date.today(), interval=i)['Close']
# data = pdr.get_data_yahoo(tickers, start="2020-01-29", end=dt.date.today())['Close']

# From the closing prices, calculate periodic returns
# pct = data.pct_change()
# pct = pct[1:]
# mean = pct.mean()
# std = pct.std()
# skew = pct.describe()
pct = (data - data.rolling(n).mean()) / data.rolling(n).mean()
pct = pct[n:]



# Repeat for each equity in portfolio
# pct.hist(bins=40, histtype="stepfilled", alpha=0.5)
# x = np.linspace(mean - 3*std, mean + 3*std, 100)
# plt.plot(x, norm.pdf(x, mean, std), "r")
# plt.title(f"{tickers} weekly returns (binned) vs. normal distribution")
# plt.text(x=0, y=5, s=f'{tickers} {skew}')
plot_predict(pct, lags=63)
plt.title(f"{tickers} ACF {n} {i}")
plt.show()
