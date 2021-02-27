from dataclasses import dataclass
import pandas as pd
import json
import finviz
from finvizfinance.news import News
import quantstats as qs
from quotes.historical_universe import *
from quotes.parsers import *
from telegram import instructions as ins


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
            sma50 = price['SMA50'].split('%')
            sma50 = float(sma50[0])
        except Exception as e10:
            msg1 = 'Описание для ETF недоступно'
            return msg1
        if sma50 > 0:
            mom = 'у акций компании наблюдается моментум'
        elif sma50 <= 0:
            mom = 'отсутствует'
        msg1 = price['Company'] + '\n' + \
            'Sector: ' + price['Sector'] + '\n' + \
            'Industry: ' + price['Industry'] + '\n' + \
            'Country: ' + price['Country'] + '\n' + \
            'MarketCap: ' + price['Market Cap'] + '\n' + \
            'Price: ' + price['Price'] + '\n' + \
            'SMA50: ' + price['SMA50'] + '\n' + \
            'Моментум: ' + mom + '\n' + \
            'AvgVolume: ' + price['Avg Volume'] + '\n'
        return msg1

    def company_rank_v2(self):
        msg1 = ''
        try:
            rank = get_ranking_data(self.stock)
        except Exception as e11:
            msg1 = 'Аналитика для данного тикера недоступна. '
            return msg1

        next_earning_date = None
        for k, v in rank.items():
            if k == "next_earning_date":
                next_earning_date = v
            elif k == 'data':
                msg1 = 'Данные временно недоступны, попробуйте выполнить запрос через минуту. '
            else:
                msg1 += '\n' + ins.ranking[k][v]
        return msg1

    def stock_news(self):
        try:
            news = finviz.get_news(self.stock)
        except Exception as e10:
            msg = 'Описание для ETF недоступно'
            return msg
        msg = ''
        for n in news[0:15]:
            msg += ' '.join(n) + '\n' + '\n'
        return msg


def fin_news(blogs=False, rows=20):
    fnews = News()
    all_news = fnews.getNews()
    if blogs:
        news = all_news['blogs'][0:rows]
        news = news[(news.Source == "zerohedge") | (news.Source == "vantagepointtrading.com") | (
                news.Source == "seekingalpha.com")]
    else:
        news = all_news['news'][0:rows]
        news = news[(news.Source == "www.reuters.com") | (news.Source == "www.marketwatch.com") | (
                news.Source == "www.bloomberg.com")]
    news_list = []
    for index, row in news.iterrows():
        row = (row['Date'], row['Title'], row['Link'])
        news_list.append(row)
    msg = ''
    for n in news_list[0:rows]:
        msg += ' '.join(n) + '\n' + '\n'
    return msg

