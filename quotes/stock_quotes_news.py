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
        if returns.empty:
            self.returns = None
        else:
            self.returns = returns

    def stock_snapshot(self):
        if self.returns is not None:
            img = f'results/ticker_stat/{self.stock}.png'
            qs.plots.snapshot_v2(self.returns,
                                 title=f'{self.stock}',
                                 savefig=img)

    # def stock_stat(self):
    #     if self.returns is not None:
    #         stats = qs.reports.metrics_v2(self.returns,
    #                                       benchmark=self.benchmark,
    #                                       mode=self.mode,
    #                                       ticker_=self.stock,
    #                                       display=self.display)
    #         parse = json.loads(stats)
    #         msg = '__Ключевые Характеристики:__ ' + '\n' + '\n' + 'Start Period ' + parse[self.stock]['Start Period'] + '\n' + \
    #               'End Period ' + parse[self.stock]['End Period'] + '\n' + '\n' + \
    #               "```Total Return % ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['Total Return '])\
    #               + f'| {self.benchmark} ' + str(parse['Benchmark']['Total Return ']) + '\n' + '\n' + \
    #               "```CAGR% ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['CAGR%'])\
    #               + f'| {self.benchmark} ' + str(parse['Benchmark']['CAGR%']) + '\n' + '\n' + \
    #               "```Sharpe ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['Sharpe']) \
    #               + f'| {self.benchmark} ' + str(parse['Benchmark']['Sharpe']) + '\n' + '\n' + \
    #               "```Volatility (ann.) % ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['Volatility (ann.) ']) \
    #               + f'| {self.benchmark} ' + str(parse['Benchmark']['Volatility (ann.) ']) + '\n' + '\n' + \
    #               "```Kelly Criterion % ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['Kelly Criterion ']) \
    #               + f'| {self.benchmark} ' + str(parse['Benchmark']['Kelly Criterion ']) + '\n' + '\n' + \
    #               "```Daily Value-at-Risk ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['Daily Value-at-Risk ']) \
    #               + f'| {self.benchmark} ' + str(parse['Benchmark']['Daily Value-at-Risk ']) + '\n' + '\n' + \
    #               "```Best Year ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['Best Year ']) \
    #               + f'| {self.benchmark} ' + str(parse['Benchmark']['Best Year ']) + '\n' + '\n' + \
    #               "```Worst Year ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['Worst Year ']) \
    #               + f'| {self.benchmark} ' + str(parse['Benchmark']['Worst Year ']) + '\n' + '\n' + \
    #               "```Alpha ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['Alpha']) \
    #               + f'| {self.benchmark} ' + str(parse['Benchmark']['Alpha']) + '\n' + '\n' + \
    #               "```Beta ```" + '\n' + f'{self.stock} ' + str(parse[self.stock]['Beta']) \
    #               + f'| {self.benchmark} ' + str(parse['Benchmark']['Beta'])
    #
    #         return msg
    def stock_stat_v3(self, rank_type=None, rank=None):
        if self.returns is not None:
            stats = qs.reports.metrics_v2(self.returns,
                                          benchmark=self.benchmark,
                                          mode=self.mode,
                                          ticker_=self.stock,
                                          display=self.display)
            parse = json.loads(stats)
            if float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
                    and rank >= 11:
                sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
                         f'Upsilon-score максимален для компании этого типа. ' \
                         f'\n\n{self.stock} - ⭐️⭐️⭐️⭐️⭐️'
            elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
                    and rank >= 8:
                sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
                         f'Upsilon-score достаточно высок для компании этого типа. ' \
                         f'\n\n{self.stock} - ⭐️⭐️⭐️⭐️'
            elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
                    and rank >= 6:
                sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
                         f'Upsilon-score умеренно высок для компании этого типа. ' \
                         f'\n\n{self.stock} - ⭐️⭐️⭐️'
            elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
                    and rank <= 5:
                sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
                         f'Но Upsilon-score низок для компании этого типа. ' \
                         f'\n\n{self.stock} - ⭐️⭐️'
            elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
                    and rank >= 13:
                sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
                         f'Но Upsilon-score максимален для компании этого типа. ' \
                         f'\n\n{self.stock} - ⭐️⭐️⭐️⭐️⭐'
            elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
                    and rank >= 10:
                sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
                         f'Но Upsilon-score достаточно высок для компании этого типа. ' \
                         f'\n\n{self.stock} - ⭐️⭐️⭐️⭐️'
            elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
                    and rank >= 7:
                sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
                         f'Upsilon-score умеренно высок для компании этого типа. ' \
                         f'\n\n{self.stock} - ⭐️⭐️⭐️'
            elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
                    and rank >= 5:
                sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
                         f'Upsilon-score низок для компании этого типа. ' \
                         f'\n\n{self.stock} - ⭐️⭐️️'
            elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 0 \
                    and rank <= 4:
                sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
                         f'И Upsilon-score слишком низок для компании этого типа. Потенциальный риск не оправдан. ' \
                         f'\n\n{self.stock} - ⭐️'

            elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
                    and rank >= 8:
                sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
                         f'Upsilon-score максимален для компании этого типа. ' \
                         f'\n\n{self.stock} - ⭐️⭐️⭐️⭐️⭐️'
            elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
                    and rank >= 6:
                sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
                         f'Upsilon-score достаточно высок для компании этого типа. ' \
                         f'\n\n{self.stock} - ⭐️⭐️⭐️⭐️'
            elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
                    and rank >= 4:
                sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
                         f'Upsilon-score умеренно высок для компании этого типа. ' \
                         f'\n\n{self.stock} - ⭐️⭐️⭐️'
            elif float(parse[self.stock]['Sharpe']) > float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
                    and rank <= 3:
                sharpe = f'Соотношение доходности и риска у {self.stock} больше чем у индекса. ' \
                         f'Но Upsilon-score низок для компании этого типа. ' \
                         f'\n\n{self.stock} - ⭐️⭐️'
            elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
                    and rank >= 10:
                sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
                         f'Но Upsilon-score максимален для компании этого типа. ' \
                         f'\n\n{self.stock} - ⭐️⭐️⭐️⭐️⭐️'
            elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
                    and rank >= 8:
                sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
                         f'Но Upsilon-score достаточно высок для компании этого типа. ' \
                         f'\n\n{self.stock} - ⭐️⭐️⭐️⭐️'
            elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
                    and rank >= 6:
                sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
                         f'Но Upsilon-score умеренно высок для компании этого типа. ' \
                         f'\n\n{self.stock} - ⭐️⭐️⭐'
            elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
                    and rank >= 4:
                sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
                         f'Upsilon-score низок для компании этого типа. ' \
                         f'\n\n{self.stock} - ⭐️⭐️'
            elif float(parse[self.stock]['Sharpe']) <= float(parse['Benchmark']['Sharpe']) and rank_type == 1 \
                    and rank <= 3:
                sharpe = f'Соотношение доходности и риска у {self.stock} меньше чем у индекса. ' \
                         f'И Upsilon-score слишком низок для компании этого типа. Потенциальный риск не оправдан. ' \
                         f'\n\n{self.stock} - ⭐'
            elif rank == 0:
                sharpe = f'\U000026D4 отсутствуют данные для оценки {self.stock} или крайне плохое ведение бизнеса'
            else:
                sharpe = f'\U000026A0 противоречивые результаты анализа. Финансовая оценка не соответсвует ' \
                         f'ценовой динамике акций {self.stock}'

            msg = f'{self.stock} __проанализирована __\nс ' + parse[self.stock]['Start Period'] + ' по ' + \
                  parse[self.stock]['End Period'] + '\n' + '\n' + '```Вывод: ```' + '\n' + sharpe + '\n' + '\n'
            print(rank, rank_type)
            return msg

    def stock_description_v3(self):
        try:
            description, rank = get_ranking_data3(self.stock)
        except Exception as e10:
            msg1 = 'Ошибка, попробуйте позже...'
            return msg1
        if len(description) == 0 and rank['rank'] is None and rank['data'] is None:
            msg1 = None
            msg2 = None
            msg3 = None
            return msg1, msg2, msg3
        if description['marketCap'] is not None:
            mc = round(float(description['marketCap'] / 1000000000), 2)
        else:
            mc = 'нет данных'
        if description['beta'] is not None:
            beta = round(float(description['beta']), 2)
        else:
            beta = 'нет данных'
        if description['volume'] is not None:
            vol = round(float(description['volume'] / 1000000), 4)
        else:
            vol = 0
        if description['averageVolume'] is not None:
            avol = round(float(description['averageVolume'] / 1000000), 4)
        else:
            avol = 0
        if description['trailingPE'] is not None:
            pe = round(float(description['trailingPE']), 2)
        else:
            pe = 0
        if description['forwardPE'] is not None:
            fpe = round(float(description['forwardPE']), 2)
        else:
            fpe = 'нет данных'
        if description['exDividendDate'] is not None:
            exDividendDate = description['exDividendDate']
        else:
            exDividendDate = 'нет данных'
        if description['dividendDate'] is not None:
            dividendDate = description['dividendDate']
        else:
            dividendDate = 'нет данных'
        if len(description['earnings_earningsDate']) == 0:
            earn = 'нет данных'
        else:
            earnings_earningsDate = description['earnings_earningsDate']
            earn = ' - '.join(map(str, earnings_earningsDate))

        msg1 = f"__Тикер:__ {str(description['ticker'])}\n" \
               f"__Компания:__ {str(description['longName'])}\n" \
               f"__Сектор:__ {str(description['sector'])}\n" \
               f"__Индустрия:__ {str(description['industry'])}\n" \
               f"__Страна:__ {str(description['country'])}\n \n" \
               f"__Капитализация:__ {str(mc)} Млрд\n" \
               f"__Бета:__ {str(beta) }\n" \
               f"__Объём:__ {str(vol)} Млн\n" \
               f"__Средний объём (3m):__ {str(avol)} Млн\n" \
               f"__P/E:__ {str(pe)} \n" \
               f"__Forward P/E:__ {str(fpe)} \n" \
               f"__Тип:__ {str(description['quoteType'])}\n" \
               f"__Цена:__ {str(description['regularMarketPrice'])}\n" \
               f"__Состояние рынка:__ {str(description['marketState'])}\n" \
               f"__exDividend Date:__ {str(exDividendDate)}\n" \
               f"__Dividend Date:__ {str(dividendDate)}\n" \
               f"__Earnings Date:__ {str(earn)}\n"
        msg2 = ''
        if ("is_fin" in rank and rank["is_fin"]) or ("is_bagger" in rank and rank["is_bagger"]):
            msg3 = {'other': 1, 'rank': rank['rank']}
        else:
            msg3 = {'other': 0, 'rank': rank['rank']}
        for k, v in rank.items():
            if k == "next_earning_date":
                next_earning_date = v
            elif k is None:
                msg2 = 'Нет данных для введённого тикера '
            elif k == 'rank':
                if ("is_fin" in rank and rank["is_fin"]) or ("is_fin" in rank and rank["is_bagger"]):
                    msg2 += '\n' + ins.ranking_v3["other_rank"][v]
                else:
                    msg2 += '\n' + ins.ranking_v3[k][v]
            elif k == "is_fin" or k == "is_bagger":
                continue
            else:
                print(rank)
                msg2 += '\n' + ins.ranking_v3[k][v]
        return msg1, msg2, msg3

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


def none_to_str(s):
    if s is None:
        return '*'
    return str(s)
