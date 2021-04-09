import quantstats as qs
import numpy as np
import matplotlib.pyplot as plt
from finviz.screener import Screener
#
# filters = ['exch_nasd', 'exch_nyse', 'cap_microover', 'ta_sma50_pca']
tickers = ['SPY', 'QQQ', 'ARKW', 'ACWI', 'TLT',  'AAPL', 'TSM', 'WORK', 'TEAM', 'SQ', 'PEP', 'ZM', 'TSLA', 'PLTR', 'AYX']
custom = ['1', '2', '3', '4', '43', '44', '49', '51', '53', '65']
stock_list = Screener(tickers=tickers, rows=50, order='ticker', table='Overview', custom=custom)
stock_list.to_csv("/home/gene/projects/upsilon_one/logs/stock.csv")



