import os
import finviz
import quantstats as qs


def stock_description(stock=None, limit_=None):
    try:
        price = finviz.get_stock(stock)
    except ValueError as e10:
        return 'Ticker not found'
    msg1 = price['Company'] + '\n' + \
        'Sector: ' + price['Sector'] + '\n' + \
        'Industry: ' + price['Industry'] + '\n' + \
        'Country: ' + price['Country'] + '\n' + \
        'MarketCap: ' + price['Market Cap'] + '\n' + \
        'Price: ' + price['Price'] + '\n' + \
        'SMA50: ' + price['SMA50'] + '\n' + \
        'AvgVolume: ' + price['Avg Volume'] + '\n'
    return msg1


def stock_quotes(stock=None, limit_=None):
    img = f'results/ticker_stat/{stock}.png'
    try:
        returns = qs.utils.download_returns(stock)
    except ValueError as e11:
        return 'Ticker not found'
    qs.plots.snapshot_v2(returns, title=f'{stock}', savefig=img, show=False, ticker=stock)
    msg2 = qs.reports.metrics_v2(returns, benchmark='QQQ', mode='full', ticker_=stock,  display=False)


def stock_news(stock=None, limit_=None):
    try:
        news = finviz.get_news(stock)
    except ValueError as e10:
        return 'Ticker not found'
    msg = ''
    for n in news[0:15]:
        msg += ' '.join(n) + '\n' + '\n'
    return msg
