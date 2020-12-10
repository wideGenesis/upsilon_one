import finviz
import os
import quantstats as qs

stock = 'QQQ'

price = finviz.get_stock(stock)
news = finviz.get_news(stock)

print(price)
print(news)

# extend pandas functionality with metrics, etc.
qs.extend_pandas()

# fetch the daily returns for a stock
returns = qs.utils.download_returns(stock)

# show sharpe ratio
img = os.path.join('results', 'ticker_stat', f'{stock}.png')
print(qs.stats.sharpe(returns))
qs.plots.snapshot_v2(returns, title=f'{stock}', savefig=img, show=False, ticker=stock)
print(qs.reports.metrics(returns, mode='full'))

