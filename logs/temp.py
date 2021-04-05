import quantstats as qs
import numpy as np
import matplotlib.pyplot as plt
from finviz.screener import Screener
#
# filters = ['exch_nasd', 'exch_nyse', 'cap_microover', 'ta_sma50_pca']
# stock_list = Screener(filters=filters, table='Overview', order='-marketcap')  # Get the performance table and sort it by price ascending
#
# stock_list.to_csv("/home/gene/projects/upsilon_one/logs/stock.csv")


# def ema(data, window):
#     alpha = 2 / (window + 1.0)
#     alpha_rev = 1-alpha
#     n = data.shape[0]
#     pows = alpha_rev**(np.arange(n+1))
#     scale_arr = 1/pows[:-1]
#     offset = data[0]*pows[1:]
#     pw0 = alpha*alpha_rev**(n-1)
#     mult = data*pw0*scale_arr
#     cumsums = mult.cumsum()
#     out = offset + cumsums*scale_arr[::-1]
#     return out

def sma(data, window):
    weights = np.repeat(1.0, window) / window
    sma = np.convolve(data, weights, 'valid')
    return sma

data = qs.utils.download_weekly('AAPL')
data_sma = sma(data, 8)
print(data)
print(data_sma)
# data_sma.to_csv('/home/gene/projects/upsilon_one/logs/aapl.csv')
