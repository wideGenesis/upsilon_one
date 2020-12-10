import finviz
from finviz.screener import Screener
import os
import quantstats as qs

stock = 'QQQ'
# stock_list = ['QQQ']
#
# stock_ = Screener(tickers=stock_list, table='Performance', order='price')
#
# price = finviz.get_stock(stock)
# news = finviz.get_news(stock)
#
# print(price)
# print(news)
#
#
# chart = stock_.get_charts(period='d', chart_type='c', size='m', ta='0')
# print(chart)

# period='d' > daily
# period='w' > weekly
# period='m' > monthly

# chart_type='c' > candle
# chart_type='l' > lines

# size='m' > small
# size='l' > large

# ta='1' > display technical analysis
# ta='0' > ignore technical analysis


# extend pandas functionality with metrics, etc.
qs.extend_pandas()

# fetch the daily returns for a stock
returns = qs.utils.download_returns(stock)

# show sharpe ratio
img = os.path.join('results', 'ticker_stat', f'{stock}.png')
print(qs.stats.sharpe(returns))
qs.plots.snapshot_v2(returns, title=f'{stock}', savefig=img, show=False, ticker=stock)
print(qs.reports.metrics(returns, mode='full'))

