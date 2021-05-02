import datetime as dt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde, norm
import matplotlib.mlab as mlab
from pandas_datareader import data as pdr


# Create our portfolio of equities
tickers = ['TSLA']

# Set the investment weights (I arbitrarily picked for example)
weights = np.array([1])

# Set an initial investment level
initial_investment = 10000

# Download closing prices
data = pdr.get_data_yahoo(tickers, start="2020-04-29", end=dt.date.today())['Close']

# From the closing prices, calculate periodic returns
returns = data.pct_change()


# Generate Var-Cov matrix
cov_matrix = returns.cov()
avg_rets = returns.mean()
# Calc mean returns for portfolio overall, using dot product to normalize individual means against investment weights
port_mean = avg_rets.dot(weights)
# Calculate portfolio standard deviation
port_stdev = np.sqrt(weights.T.dot(cov_matrix).dot(weights))
# Calculate mean of investment
mean_investment = (1 + port_mean) * initial_investment

# Calculate standard deviation of investmnet
stdev_investment = initial_investment * port_stdev

# Select our confidence interval (I'll choose 95% here)
conf_level1 = 0.01

# Using SciPy ppf method to generate values for the
# inverse cumulative distribution function to a normal distribution
# Plugging in the mean, standard deviation of our portfolio
# as calculated above
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html

cutoff1 = norm.ppf(conf_level1, mean_investment, stdev_investment)

#Finally, we can calculate the VaR at our confidence interval
var_1d1 = initial_investment - cutoff1
print(var_1d1)


# Calculate n Day VaR
# var_array = []
# var_array_278 = []
# num_days = int(21)
# for x in range(1, num_days+1):
#     var_array.append(np.round(var_1d1 * np.sqrt(x), 2))
#     var_array_278.append(np.round(var_1d1 * 2.71 * np.sqrt(x), 2))
#     print(str(x) + " day VaR @ 99% confidence: " + str(np.round(var_1d1 * np.sqrt(x), 2)))
#     print(str(x) + " day VaR278 @ 99% confidence: " + str(np.round(var_1d1 * 2.71 * np.sqrt(x), 2)))
# # Build plot
# plt.xlabel("Day #")
# plt.ylabel("Max portfolio loss (USD)")
# plt.title("Max portfolio loss (VaR) over 15-day period")
# plt.plot(var_array, "r")
# plt.plot(var_array_278, "r")
# plt.show()
returns = returns * 100

min_returns = abs(returns.rolling(21).min())
new_VAR = min_returns.iloc[-63:].mean() + min_returns.iloc[-63:].std()
new_VARe = min_returns.iloc[-63:].mean() + 2.71 * min_returns.iloc[-63:].std()


new_var_array = []
new_var_array_e = []
num_days = int(10)
for x in range(1, num_days+1):
    new_var_array.append(np.round(new_VAR * np.sqrt(x), 2))
    new_var_array_e.append(np.round(new_VARe * np.sqrt(x), 2))
    print(str(x) + " day Max Normal: " + str(np.round(new_VAR * np.sqrt(x), 2)))
    print(str(x) + " day Tail Loss: " + str(np.round(new_VARe * np.sqrt(x), 2)))
plt.xlabel("Day #")
plt.ylabel("Max portfolio loss (USD)")
plt.title("Max portfolio loss (VaR) over 10-day period")
plt.plot(new_var_array, "r")
plt.plot(new_var_array_e, "r")
plt.show()


# length = input(21
# pct2 =(src - src[1]) / src[1] * 100
# min_return = abs(lowest(pct2,length))
# s = sma(min_return, 63) + stdev(min_return, 63)
# s3 = sma(min_return, 63) + 3*stdev(min_return, 63)