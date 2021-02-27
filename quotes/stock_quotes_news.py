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
        except Exception as e10:
            msg1 = 'Описание для ETF недоступно'
            return msg1
        msg1 = price['Company'] + '\n' + \
            'Sector: ' + price['Sector'] + '\n' + \
            'Industry: ' + price['Industry'] + '\n' + \
            'Country: ' + price['Country'] + '\n' + \
            'MarketCap: ' + price['Market Cap'] + '\n' + \
            'Price: ' + price['Price'] + '\n' + \
            'SMA50: ' + price['SMA50'] + '\n' + \
            'AvgVolume: ' + price['Avg Volume'] + '\n'
        return msg1

    def company_rank(self):
        try:
            rank = get_company_rank(self.stock)
            price = finviz.get_stock(self.stock)
            sma50 = price['SMA50'].split('%')
            sma50 = float(sma50[0])
            print(rank[0], rank[1], rank[2])
            print(sma50)

        except Exception as e11:
            msg1 = 'Ранг для данного тикера недоступен'
            return msg1

        if rank[0] is True and rank[1] is True and rank[2] is True and sma50 > 0:
            msg1 = 'Развивающаяся, прибыльная компания с перспективами роста и моментумом. ' + \
                   '\U0001F44D'*5 + ' - Сильный кандидат для покупки'
            return msg1
        elif rank[0] is True and rank[1] is True and rank[2] is True and sma50 < 0:
            msg1 = 'Развивающаяся, прибыльная компания с перспективами роста. ' + \
                   '\U0001F44D'*4 + ' - Хороший кандидат для покупки'
            return msg1
        elif rank[0] is True and rank[1] is True and rank[2] is False and sma50 > 0:
            msg1 = 'Стабильная, прибыльная компания с перспективами роста или компания ' \
                   'оптимизирующая рентабельность бизнеса без расширения рынков сбыта. ' + \
                   '\U0001F44D'*4 + ' - Хороший кандидат для покупки'
            return msg1
        elif rank[0] is True and rank[1] is True and rank[2] is False and sma50 < 0:
            msg1 = 'Стабильная, прибыльная компания с перспективами роста или компания ' \
                   'оптимизирующая рентабельность бизнеса без расширения рынков сбыта. ' + \
                   '\U0001F44D'*3 + ' - Средний кандидат для покупки'
            return msg1

        elif rank[0] is True and rank[1] is False and rank[2] is True and sma50 > 0:
            msg1 = 'Развивающаяся компания с краткосрочным падением прибыли и рентабельности. ' + \
                   '\U0001F44D'*4 + ' - Средний кандидат для покупки. У компании ожидаются прибыли в будущем, ' \
                                    'и эти ожидания мотивируют инвесторов к покупке акций'
            return msg1
        elif rank[0] is True and rank[1] is False and rank[2] is True and sma50 < 0:
            msg1 = 'Развивающаяся компания с краткосрочным падением прибыли и рентабельности. ' + \
                   '\U0001F44D'*3 + ' - Средний кандидат для покупки. У компании ожидаются прибыли в будущем, ' \
                                    'но на данный момент эти ожидания не мотивируют инвесторов к покупке акций.'
            return msg1

        elif rank[0] is False and rank[1] is True and rank[2] is True and sma50 > 0:
            msg1 = 'Стабильная компания, без перспектив к росту и развитию в краткосрочной перспективе. ' + \
                   '\U0001F44D'*4 + ' - Средний кандидат для покупки.'
            return msg1
        elif rank[0] is False and rank[1] is True and rank[2] is True and sma50 < 0:
            msg1 = 'Стабильная компания, без перспектив к росту и развитию в краткосрочной перспективе. ' + \
                   '\U0001F44D'*3 + ' - Слабый кандидат для покупки.'
            return msg1

        elif rank[0] is False and rank[1] is False and rank[2] is True and sma50 > 0:
            msg1 = 'Развивающаяся, но убыточная компания. Возможно компания только захватывает рынки сбыта. ' + \
                   '\U0001F44D'*2 + ' - Слабый кандидат для покупки. Компания "на любителя"'
            return msg1
        elif rank[0] is False and rank[1] is False and rank[2] is True and sma50 < 0:
            msg1 = 'Развивающаяся, но убыточная компания. Возможно компания только захватывает рынки сбыта. ' + \
                   '\U0001F44D'*1 + ' - Очень слабый кандидат для покупки. Компания "на любителя"'
            return msg1

        elif rank[0] is False and rank[1] is False and rank[2] is False and sma50 > 0:
            msg1 = 'Убыточная компания, без перспектив и развития. ' + \
                   '\U0001F44E' + ' - Не является кандидатом для покупки, может быть кандидатом для спекуляций'
            return msg1
        elif rank[0] is False and rank[1] is False and rank[2] is False and sma50 < 0:
            msg1 = 'Убыточная компания, без перспектив и развития. ' + \
                   '\U0001F44E' + ' - Не является кандидатом для покупки и спекуляций'
            return msg1

        elif rank[0] is False and rank[1] is True and rank[2] is False and sma50 > 0:
            msg1 = 'Компания без перспектив и развития. ' + \
                   '\U0001F44D'*2 + ' - Очень слабый кандидат для покупки. Кандидат для спекуляций'
            return msg1
        elif rank[0] is False and rank[1] is True and rank[2] is False and sma50 < 0:
            msg1 = 'Компания без перспектив и развития. ' + \
                   '\U0001F44D' + ' - Кандидат для спекуляций исключительно '
            return msg1

        elif rank[0] is True and rank[1] is False and rank[2] is False and sma50 > 0:
            msg1 = 'Убыточная компания,но с перспективой развития. ' + \
                   '\U0001F44D'*2 + ' - Очень слабый кандидат для покупки. Кандидат для спекуляций'
            return msg1
        elif rank[0] is True and rank[1] is False and rank[2] is False and sma50 < 0:
            msg1 = 'Убыточная компания,но с перспективой развития. ' + \
                   '\U0001F44D'*1 + ' - Кандидат для спекуляций'
            return msg1

        elif rank[0] is None and rank[1] is None and rank[2] is None:
            msg1 = 'Недостаточно данных для скоринга'
            return msg1
# 'U+1F44D'
#     {'rank': 2, 'revenue_estimate': -1, 'revenue_estimate_next_year': -1, 'curr_avg_estimate': 2,
#      'next_qtr_avg_estimate': 2, 'total_revenue': -1, 'diluted_normalized_eps': 1,
#      'net_profit_margin_percent_annual': -2, 'divident_per_share_annual': 2, 'mkt_cap': -1, 'beta': -1,
#      'current_ratio_quarterly': 2, 'long_term_debt_equity_quarterly_r': -2}

    def company_rank_v2(self):
        msg1 = ''
        msg2 = ''
        try:
            rank = get_ranking_data(self.stock)
            price = finviz.get_stock(self.stock)
            sma50 = price['SMA50'].split('%')
            sma50 = float(sma50[0])
            print(rank)
            print(sma50)

        except Exception as e11:
            msg1.replace('', 'Ранг для данного тикера недоступен')
            return msg1

        final = {}
        for k, k2 in zip(rank, ins.ranking):
            if k == k2:
                final[dic2[k]] = dic1[k]

        # if rank['revenue_estimate'] == 2:
        #     msg1.replace(msg1, ins.ranking['revenue_estimate'][2])
        # elif rank['revenue_estimate'] == 1:
        #     msg1.replace(msg1, ins.ranking['revenue_estimate'][1])
        # elif rank['revenue_estimate'] == -1:
        #     msg1.replace(msg1, ins.ranking['revenue_estimate'][3])
        #
        # if rank['revenue_estimate_next_year'] == 1:
        #     msg2.replace(msg2, ins.ranking['revenue_estimate_next_year'][1])
        # elif rank['revenue_estimate_next_year'] == -1:
        #     msg2.replace(msg2, ins.ranking['revenue_estimate_next_year'][2])
        # print(msg1 + '\n' + msg2)
        # return msg1 + '\n' + msg2


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

