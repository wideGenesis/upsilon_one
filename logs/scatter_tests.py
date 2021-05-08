import datetime as dt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde, norm
from pandas_datareader import data as pdr


# Create our portfolio of equities
tickers = ['amzn']

# Download closing prices
data = pdr.get_data_yahoo(tickers, start="2020-01-29", end=dt.date.today(), interval="w")['Close']
# data = pdr.get_data_yahoo(tickers, start="2020-01-29", end=dt.date.today())['Close']


# From the closing prices, calculate periodic returns
pct = data.pct_change()
mean = pct.mean()
std = pct.std()
skew = pct.describe()


# Repeat for each equity in portfolio
pct.hist(bins=40, histtype="stepfilled", alpha=0.5)
x = np.linspace(mean - 3*std, mean + 3*std, 100)
plt.plot(x, norm.pdf(x, mean, std), "r")
plt.title(f"{tickers} weekly returns (binned) vs. normal distribution")
plt.text(x=0, y=5, s=f'{tickers} {skew}')
plt.show()
