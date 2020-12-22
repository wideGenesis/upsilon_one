from dataclasses import dataclass
import pandas as pd
import json
import finviz
from finvizfinance.news import News
import quantstats as qs


@dataclass
class StockStat:
    __slots__ = [
        'stock',
        'returns',
        'limit_',
        'title',
        'ticker',
        'benchmark',
        'mode',
        'ticker_',
        'display',
    ]

    def __init__(self,
                 stock: str = None,
                 returns: pd = None,
                 limit_: int = None,
                 title: str = None,
                 benchmark: str = 'QQQ',
                 mode: str = 'full',
                 ticker_: str = None,
                 display: bool = False,
                 ):
        self.stock = stock
        self.returns = returns
        self.limit_ = limit_
        self.title = title
        self.benchmark = benchmark
        self.mode = mode
        self.ticker_ = ticker_
        self.display = display

    def stock_download(self):
        try:
            returns = qs.utils.download_returns(self.stock)
        except ValueError as e11:
            return e11
        self.returns = returns

    def stock_snapshot(self):
        img = f'results/ticker_stat/{self.stock}.png'
        qs.plots.snapshot_v2(self.returns,
                             title=f'{self.stock}',
                             savefig=img)
    def stock_stat(self):
        stats = qs.reports.metrics_v2(self.returns,
                                      benchmark=self.benchmark,
                                      mode=self.mode,
                                      ticker_=self.stock,
                                      display=self.display)
        parse = json.loads(stats)
        msg = '```Ключевые Характеристики:``` ' + '\n' + '\n' + 'Start Period ' + parse[self.stock]['Start Period'] + '\n' + \
              'End Period ' + parse[self.stock]['End Period'] + '\n' + '\n' + \
              "```Total Return % ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['Total Return '])\
              + f'| {self.benchmark} ' + str(parse['Benchmark']['Total Return ']) + '\n' + '\n' + \
              "```CAGR% ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['CAGR%'])\
              + f'| {self.benchmark} ' + str(parse['Benchmark']['CAGR%']) + '\n' + '\n' + \
              "```Sharpe ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['Sharpe']) \
              + f'| {self.benchmark} ' + str(parse['Benchmark']['Sharpe']) + '\n' + '\n' + \
              "```Volatility (ann.) % ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['Volatility (ann.) ']) \
              + f'| {self.benchmark} ' + str(parse['Benchmark']['Volatility (ann.) ']) + '\n' + '\n' + \
              "```Expected Monthly % ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['Expected Monthly %']) \
              + f'| {self.benchmark} ' + str(parse['Benchmark']['Expected Monthly %']) + '\n' + '\n' + \
              "```Expected Yearly % ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['Expected Yearly %']) \
              + f'| {self.benchmark} ' + str(parse['Benchmark']['Expected Yearly %']) + '\n' + '\n' + \
              "```Kelly Criterion % ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['Kelly Criterion ']) \
              + f'| {self.benchmark} ' + str(parse['Benchmark']['Kelly Criterion ']) + '\n' + '\n' + \
              "```Daily Value-at-Risk ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['Daily Value-at-Risk ']) \
              + f'| {self.benchmark} ' + str(parse['Benchmark']['Daily Value-at-Risk ']) + '\n' + '\n' + \
              "```Best Year ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['Best Year ']) \
              + f'| {self.benchmark} ' + str(parse['Benchmark']['Best Year ']) + '\n' + '\n' + \
              "```Worst Year ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['Worst Year ']) \
              + f'| {self.benchmark} ' + str(parse['Benchmark']['Worst Year ']) + '\n' + '\n' + \
              "```Alpha ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['Alpha']) \
              + f'| {self.benchmark} ' + str(parse['Benchmark']['Alpha']) + '\n' + '\n' + \
              "```Beta ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['Beta']) \
              + f'| {self.benchmark} ' + str(parse['Benchmark']['Beta'])

        return msg

    def stock_description(self):
        try:
            price = finviz.get_stock(self.stock)
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

    def stock_news(self):
        try:
            news = finviz.get_news(self.stock)
        except ValueError as e10:
            return 'Ticker not found'
        msg = ''
        for n in news[0:15]:
            msg += ' '.join(n) + '\n' + '\n'
        return msg


def fin_news():
    fnews = News()
    all_news = fnews.getNews()
    news = all_news['news'][0:5]
    news = news[(news.Source == "www.reuters.com") | (news.Source == "www.marketwatch.com") | (
                news.Source == "www.bloomberg.com")]
    news_list = []
    for d1 in news['Date']:
        for t1 in news['Title']:
            for l1 in news['Link']:
                row = (d1 + ' ' + t1 + ' ' + l1)
                news_list.append(row)

    print(news_list)


    #
    # return msg

    # msg = ''
    # for n in news['Link'][0:10]:
    #     for s in news['Source'][0:10]:
    #         if s == 'www.reuters.com':
    #             msg += n + '\n' + '\n'
    # print(msg)
    # return msg
    #
    # z = all_news['blogs']['Source'].head(50)
    #
    # print(z)
    # print(type(z))
    # print(type(all_news))
    # """
    #  www.reuters.com
    #  www.bloomberg.com
    #  www.marketwatch.com
    #
    #   zerohedge
    #   vantagepointtrading.com
    #
    #
    # """
fin_news()