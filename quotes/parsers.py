import datetime
import os
import re
from time import sleep
from fastnumbers import *
import csv
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import io
import quandl
from scipy.stats import norm
import random

from charter.finance2 import *
from project_shared import *
from yahooquery import Ticker
from PIL import Image
from quotes.parsers_env import agents
import uuid
import numpy as np
from datetime import date, timedelta
from math import sqrt


def correl(ret_df_=None, save_path=None, title=None):
    corr = ret_df_.corr()
    sns.set(rc={'figure.facecolor': 'black', 'xtick.color': 'white', 'ytick.color': 'white', 'text.color': 'white',
                'axes.labelcolor': 'white'})
    sns.set_context('paper', font_scale=0.85)
    g = sns.clustermap(corr, yticklabels=True, annot=True, cmap='RdYlGn', row_colors=None,
                       col_colors=None, figsize=(10, 10))
    plt.setp(g.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)  # ytick rotate
    g.ax_row_dendrogram.set_visible(True)
    g.ax_col_dendrogram.set_visible(False)
    g.fig.suptitle(f'Корреляция - \n{title}', fontsize=25)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor='black', transparent=True)
    buf.seek(0)
    im = Image.open(buf)
    im.save(f'{save_path}.png')
    buf.close()


def scatter_for_risk_premium(price_df: pd = None, save_path=''):
    price_df = price_df.iloc[-1]
    res = {}
    for i, value in enumerate(price_df):
        symbol = re.split(' ', price_df.axes[0].array[i])[0]
        if symbol in res:
            res[symbol].append(value)
        else:
            res[symbol] = [value]
    df = pd.DataFrame.from_dict(res, orient='index')

    df.columns = ['Risk', 'RP Ratio', 'Premium', 'Sharpe']

    sns.set(rc={'figure.facecolor': 'black', 'figure.edgecolor': 'black', 'xtick.color': 'white',
                'ytick.color': 'white', 'text.color': 'white', 'axes.labelcolor': 'white',
                'axes.facecolor': 'black', 'grid.color': '#17171a'})
    sns.set_context('paper', font_scale=1.1)
    palette = sns.color_palette("RdYlGn", n_colors=len(df.index),  as_cmap=True)
    sns.despine()
    ave_risk = df['Risk']
    ave_alpha = df['Premium']
    ave_premia = df['RP Ratio']
    sharpe_mean = df['Sharpe']

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=ave_risk, y=ave_alpha, hue=sharpe_mean, size=sharpe_mean, alpha=0.95,
                    legend=True, sizes=(30, 300), markers=True, palette=palette)

    for line in range(0, df.shape[0]):
        plt.text(df['Risk'][line], df['Premium'][line], df.index[line],
                 horizontalalignment='left', size='x-small', color='white', weight='semibold')

    plt.xlabel("Monthly Risk (%)")
    plt.ylabel("Excess Return over Risk (%)")
    plt.suptitle('Risk-Premium Analysis', fontsize=25)
    plt.legend(title='U Sharpe', loc='center left', bbox_to_anchor=(1.01, 0.5), borderaxespad=0)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor='black', transparent=True, bbox_inches='tight')
    buf.seek(0)
    im = Image.open(buf)
    im.save(f'{save_path}.png')
    buf.close()
    # plt.savefig(path + filename_scatter, facecolor='black', transparent=True, bbox_inches='tight')


# ============================== GET Inspector ================================

def get_inspector_data(portfolio, quarter=63):
    path = f'{PROJECT_HOME_DIR}/results/inspector/'
    benchmarks = {'SPY': 1, 'QQQ': 1, 'ARKK': 1, 'TLT': 1, 'VLUE': 1, 'EEM': 1}
    constituents = {}
    constituents.update(portfolio)
    portfolio.update(benchmarks)
    # debug(f' ### {portfolio} ###')
    # debug(f' ### {constituents} ###')
    tickerlist = portfolio.keys()
    scrape_tickers = tickerlist
    tickers_data = None
    try:
        tickers_data = Ticker(scrape_tickers)
    except Exception as e:
        debug(e, ERROR)

    now = datetime.datetime.now()
    six_month_ago = add_months(now, -7)

    df = tickers_data.history(start=six_month_ago)
    df['hlc3'] = (df['high'] + df['low'] + df['close']) / 3
    df.drop(columns={'open', 'volume', 'adjclose', 'dividends', 'splits', 'high', 'low', 'close'}, errors='ignore',
            inplace=True)
    df.reset_index(level=df.index.names, inplace=True)
    df = (df.assign(idx=df.groupby('symbol').cumcount()).pivot_table(index='date', columns='symbol', values='hlc3'))

    all_symbols = df.columns.tolist()
    bench_df = df.copy()
    for col in all_symbols:
        if col not in benchmarks.keys():
            bench_df.drop(col, axis=1, inplace=True)
    for col in all_symbols:
        if col not in constituents.keys():
            df.drop(col, axis=1, inplace=True)

    stocks = df.columns.tolist()
    benches = bench_df.columns.tolist()

    portfolio_cap = 0.0
    portfolio_weights_pct = {}
    first_value = list(constituents.values())[0]
    if fast_int(first_value) == 0:
        for ticker in stocks:
            portfolio_weights_pct[ticker] = 1 / len(constituents)
    else:
        if first_value.endswith('%'):
            for ticker in stocks:
                portfolio_weights_pct[ticker] = fast_float(re.split('%', first_value)[0])
        else:
            for ticker in stocks:
                portfolio_cap += df[ticker][-1] * fast_int(constituents[ticker])

            for ticker in stocks:
                portfolio_weights_pct[ticker] = (df[ticker][-1] * fast_int(constituents[ticker])) / portfolio_cap

    angular_stocks = pd.DataFrame()  # для коррел матрицы
    ulcer = pd.DataFrame()  # init df для Ulcer

    df['portfolio_pct'] = 0
    df['PORTF price'] = 0
    for col in stocks:
        df[col + ' returns'] = df[col].pct_change() * portfolio_weights_pct[col]
        df['portfolio_pct'] += df[col + ' returns']

        # For Ulcer df - hlc3, не ретурны
        ulcer[col + ' price'] = df[col] * portfolio_weights_pct[col]
        # For Ulcer df - hlc3 * w для портфеля, не ретурны
        df['PORTF price'] += ulcer[col + ' price']

        # ретурны для коррел матрицы конституентов
        angular_stocks[col] = df[col].pct_change()

    # цена портфеля для Ulcer
    ulcer['PORTF price'] = df['PORTF price']
    df.drop(columns={'PORTF price'}, inplace=True)
    
    # квартальный шарп порта
    df[f'port_sharpe_{quarter}'] = (df['portfolio_pct'].rolling(quarter).mean() /
                                    df['portfolio_pct'].rolling(quarter).std()) * sqrt(quarter)

    df[f'port_volatility_{quarter}'] = df['portfolio_pct'].rolling(quarter).std() * sqrt(quarter)  # квартал вола порта
    # месячная аннуализированная/стандартная вола порта
    df[f'port_volatility_21'] = df['portfolio_pct'].rolling(21).std() * sqrt(252)
    df.dropna(inplace=True)

    # расчет бенчей
    for col in benches:
        bench_df[f'{col}_return'] = bench_df[col].pct_change()

        # квартал шарп по бенчам
        bench_df[f'{col}_sharpe_{quarter}'] = (bench_df[col].pct_change().rolling(quarter).mean() /
                                               bench_df[col].pct_change().rolling(quarter).std()) * sqrt(quarter)
        # квартальная вола по бенчам
        bench_df[f'{col}_volatility_{quarter}'] = bench_df[col].pct_change().rolling(quarter).std() * sqrt(quarter)

        # квартальный м2 по бенчам
        # bench_df[f'{col}_m2_{quarter}'] = bench_df[f'{col}_sharpe_{quarter}'] * df[f'port_volatility_{quarter}']
        bench_df[f'{col}_m2_{quarter}'] = df[f'port_sharpe_{quarter}'] * bench_df[f'{col}_volatility_{quarter}']

        # For Ulcer цены бенчей
        ulcer[col + ' price'] = bench_df[col]

        # квартальный диверс ратио по бенчам
        bench_df[f'{col}_dr_{quarter}'] = bench_df[f'{col}_volatility_{quarter}'] * 100/df[f'port_volatility_{quarter}']

        # ретурны для correlation матрицы бенчей
        mask = ['SPY', 'QQQ']
        if col in mask:
            angular_stocks[col] = bench_df[col].pct_change()
        else:
            pass
        bench_df.drop(columns={f'{col}'}, inplace=True)

    metrics = ulcer.columns.tolist()

    for col in metrics:
        ulcer[f'{col}_up'] = 100.0 * (ulcer[col] - ulcer[col].rolling(21).min()) / ulcer[col].rolling(21).min()
        ulcer[f'{col}_up'] = ulcer[f'{col}_up'].rolling(3).mean()
        ulcer[f'{col}_up'] = ulcer[f'{col}_up'] + ulcer[f'{col}_up'].rolling(21).std()
        ulcer[f'{col}_dn'] = 100.0 * (ulcer[col] - ulcer[col].rolling(21).max()) / ulcer[col].rolling(21).max()
        ulcer[f'{col}_dn'] = abs(ulcer[f'{col}_dn'].rolling(3).mean())
        ulcer[f'{col}_dn'] = ulcer[f'{col}_dn'] + ulcer[f'{col}_dn'].rolling(21).std()
        ulcer[f'{col}_ratio'] = ulcer[f'{col}_up'] / ulcer[f'{col}_dn'].rolling(21).max()
        ulcer[f'{col}_premia'] = ulcer[f'{col}_up'] - ulcer[f'{col}_dn']
        ulcer[f'{col}_ratio_mean'] = ulcer[f'{col}_ratio'].iloc[-63:].mean()
        ulcer.drop(columns={f'{col}', f'{col}_up'}, inplace=True)
    ulcer.dropna(inplace=True)

    # расчеты для спай/тлт бенча
    bench_df[f'SPY_TLT_volatility_{quarter}'] =\
        0.6 * bench_df[f'SPY_volatility_{quarter}'] + 0.4 * bench_df[f'TLT_volatility_{quarter}']
    bench_df[f'SPY_TLT_m2_{quarter}'] = df[f'port_sharpe_{quarter}'] * bench_df[f'SPY_TLT_volatility_{quarter}']
    bench_df[f'SPY_TLT_dr_{quarter}'] = bench_df[f'SPY_TLT_volatility_{quarter}'] * 100 / \
        df[f'port_volatility_{quarter}']

    # расчет беты для стресс-теста
    bench_df[f'PORT_TO_SPY_beta_{quarter}'] = \
        bench_df[f'SPY_return'].corr(df['portfolio_pct']) * df[f'port_volatility_{quarter}'] \
        / bench_df[f'SPY_volatility_{quarter}']
    # расчет 3,14 * месячной волы для стресс-теста
    bench_df[f'PORT_WORST_21'] = df[f'port_volatility_21'] * 3.14

    # расчет коррел конституентов
    angular_stocks.dropna(inplace=True)
    angular_stocks['PORTF'] = df['portfolio_pct']
    angular_stocks.dropna(inplace=True)
    filename_h4 = str(uuid.uuid4()).replace('-', '')
    debug(f"Divers filename: {filename_h4}")
    correl(angular_stocks, save_path=f'{path}{filename_h4}',
           title='PORTF vs. ')

    # расчет риск-премий
    # angular_stocks.to_csv(os.path.join(f'{PROJECT_HOME_DIR}/results/inspector/angular.csv'))
    filename_h3 = str(uuid.uuid4()).replace('-', '')
    debug(f"scatter filename: {filename_h3 }")
    scatter_for_risk_premium(ulcer, save_path=f'{path}{filename_h3}')
    df.dropna(inplace=True)
    bench_df.dropna(inplace=True)

    # сбор словарей для визуализаций
    mask_m2 = ['SPY_m2_63', 'QQQ_m2_63', 'ARKK_m2_63', 'VLUE_m2_63', 'EEM_m2_63', 'SPY_TLT_m2_63']
    mask_dr = ['SPY_dr_63', 'QQQ_dr_63', 'ARKK_dr_63', 'VLUE_dr_63', 'EEM_dr_63', 'SPY_TLT_dr_63']
    m2_cols = bench_df[mask_m2].columns.tolist()
    dr_cols = bench_df[mask_dr].columns.tolist()
    divers = {}

    for col in dr_cols:
        name = str(col).replace('_dr_63', '')
        temp = {f'{name}': bench_df[f'{col}'].iloc[-1]}
        divers.update(temp)

    m2 = {}
    for col in m2_cols:
        name = str(col).replace('_m2_63', '')
        temp2 = {f'{name}': bench_df[f'{col}'].iloc[-1]}
        m2.update(temp2)

    filename_h1 = str(uuid.uuid4()).replace('-', '')
    debug(f"Divers filename: {filename_h1}")
    create_custom_histogram(divers, "Уровень диверсификации (%) против бенчмарков", path, filename_h1)

    filename_h2 = str(uuid.uuid4()).replace('-', '')
    debug(f"M2 filename: {filename_h2}")
    create_custom_histogram(m2, "Размер премии (%) бенчмарков в сравнении с портфелем", path, filename_h2)

    result_files = [f'{path}{filename_h1}.png',
                    f'{path}{filename_h2}.png',
                    f'{path}{filename_h3}.png',
                    f'{path}{filename_h4}.png']
    return result_files


# ============================== GET ADV ================================
def advance_decline(ag=None, img_out_path_=IMAGES_OUT_PATH):
    headers = {'User-Agent': ag}
    url_ = 'https://www.marketwatch.com/tools/marketsummary?region=usa&screener=nasdaq'
    items_ = []
    try:
        html = requests.get(url_, headers=headers).text
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find('div', {"id": "marketbreakdown"})
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) != 0:
                entries_list = []
                for i in range(0, len(cols)):
                    entries_list.append(cols[i].text.strip())
                    entries_tuple = tuple(entries_list)
                    info = ()
                    info = entries_tuple
                items_.append(info)
        del items_[5:8]
        del items_[0]
    except TypeError as e02:
        debug(e02)
        return
    with open(img_out_path_ + 'adv.csv', 'w+') as f:
        for rows_ in items_:
            write = csv.writer(f)
            write.writerow(rows_)
    debug('adv complete')


def nyse_nasdaq_stat(img_out_path_=IMAGES_OUT_PATH):
    file = pd.read_csv(os.path.join(img_out_path_, 'adv.csv'), header=None)

    advNY = round(int(file[1].iloc[0]) * 100 / int(file[1].iloc[3]), 2)
    advTV = file[1].iloc[8]
    advAV = file[1].iloc[5]
    advDV = file[1].iloc[6]

    advNA = round(int(file[2].iloc[0]) * 100 / int(file[2].iloc[3]), 2)
    advTVq = file[2].iloc[8]
    advAVq = file[2].iloc[5]
    advDVq = file[2].iloc[6]
    msg = f'NYSE Advancing Issues - {advNY}% \n' \
          f'NYSE Total Volume - {advTV} \n' \
          f'NYSE Advancing Volume - {advAV} \n' \
          f'NYSE Declining Volume - {advDV} \n' \
          f'______________________________\n' \
          f'NASDAQ Advancing Issues - {advNA}% \n' \
          f'NASDAQ Total Volume - {advTVq} \n' \
          f'NASDAQ Advancing Volume - {advAVq} \n' \
          f'NASDAQ Declining Volume - {advDVq} \n'

    return msg


# ============================== GET RANKING DATA III ================================
def get_ranking_data3(tick, ag=agents()):
    debug(f' ### {tick} ###')
    ticker = tick.upper()
    err_info_result = {}
    err_rank_result = {"rank": None, "data": None}
    revenue_data = {}

    if ticker is None or len(ticker) == 0:
        debug(f'Ticker is none, or len = 0 -- [{ticker}]')
        return err_info_result, err_rank_result, revenue_data

    ticker_data = None
    try:
        ticker_data = Ticker(ticker)
    except Exception as e:
        debug(e, ERROR)
        debug(f"Can't get ticker data -- [{ticker}]")
        return err_info_result, err_rank_result

    quoteType = None
    if ticker_data.quotes == 'No data found':
        debug(f"No data found -- [{ticker}]")
        return err_info_result, err_rank_result, revenue_data
    else:
        quoteType = ticker_data.quotes[ticker].get('quoteType', None)
        fullExchangeName = ticker_data.quotes[ticker].get('fullExchangeName')
        if (quoteType is None or
                quoteType == 'MUTUALFUND' or
                quoteType == 'ECNQUOTE' or
                quoteType == 'ETF' or
                (quoteType == 'EQUITY' and fullExchangeName == 'Other OTC')):
            debug(f"quoteType == {quoteType} -- [{ticker}]")
            return err_info_result, err_rank_result, revenue_data

    rank_result = {}
    need_data = ["AdditionalPaidInCapital",
                 "BasicEPS",
                 "CashAndCashEquivalents",
                 "CashDividendsPaid",
                 "CurrentAssets",
                 "CurrentLiabilities",
                 "DilutedEPS",
                 "EBIT",
                 "FreeCashFlow",
                 "InterestExpense",
                 "Inventory",
                 "InvestedCapital",
                 "LongTermDebtAndCapitalLeaseObligation",
                 "NetIncome",
                 "OperatingRevenue",
                 "PretaxIncome",
                 "Receivables",
                 "RetainedEarnings",
                 "ShareIssued",
                 "TaxProvision",
                 "TotalAssets",
                 "TotalLiabilitiesNetMinorityInterest",
                 "TotalNonCurrentAssets",
                 "TotalRevenue"
                 ]
    financial_data_q = None
    try:
        financial_data_q = ticker_data.get_financial_data(need_data, frequency="q", trailing=False)
    except Exception as e:
        debug(e, ERROR)
        return err_info_result, err_rank_result, revenue_data

    if isinstance(financial_data_q, str):
        debug(f"Can't get ticker data -- [{ticker}]")
        return err_info_result, err_rank_result, revenue_data

    valuation = None
    if not isinstance(ticker_data.valuation_measures, str):
        valuation = ticker_data.valuation_measures.loc[ticker_data.valuation_measures["periodType"] == "3M"]

    earnings_trend_data = ticker_data.earnings_trend[ticker]

    # % % % % % % % % % % % % % % % % % % %
    # Description  Block
    # % % % % % % % % % % % % % % % % % % %

    longName = ticker_data.price[ticker].get('longName', '')
    sector = ticker_data.asset_profile[ticker].get('sector', '')
    industry = ticker_data.asset_profile[ticker].get('industry', '')
    country = ticker_data.asset_profile[ticker].get('country', '')
    regularMarketPrice = ticker_data.price[ticker].get('regularMarketPrice', None)
    marketState = ticker_data.price[ticker].get('marketState', '')
    marketCap = ticker_data.price[ticker].get('marketCap', None)
    beta = ticker_data.summary_detail[ticker].get('beta', None)
    volume = ticker_data.summary_detail[ticker].get('volume', None)
    averageVolume = ticker_data.summary_detail[ticker].get('averageVolume', None)
    trailingPE = ticker_data.summary_detail[ticker].get('trailingPE', None)
    forwardPE = ticker_data.summary_detail[ticker].get('forwardPE', None)
    ce_exDividendDate = ticker_data.calendar_events[ticker].get('exDividendDate', None)
    ce_dividendDate = ticker_data.calendar_events[ticker].get('dividendDate', None)
    ce_earnings_earnings = ticker_data.calendar_events[ticker].get('earnings', None)
    ce_earnings_earningsDate = ''
    if ce_earnings_earnings is not None:
        ce_earnings_earningsDate = ce_earnings_earnings.get('earningsDate', '')

    info_result = {'ticker': ticker,
                   'quoteType': quoteType,
                   'longName': longName,
                   'sector': sector,
                   'industry': industry,
                   'country': country,
                   'regularMarketPrice': regularMarketPrice,
                   'marketState': marketState,
                   'marketCap': marketCap,
                   'beta': beta,
                   'volume': volume,
                   'averageVolume': averageVolume,
                   'trailingPE': trailingPE,
                   'forwardPE': forwardPE,
                   'exDividendDate': ce_exDividendDate,
                   'dividendDate': ce_dividendDate,
                   'earnings_earningsDate': ce_earnings_earningsDate}

    # debug('--- Ticker Info ---')
    # Если OperatingRevenue отсутствует или последнее значение OperatingRevenue <= 0 то считаем что это скам
    operating_revenue_ttm1 = None
    operating_revenue_ttm0 = None
    operating_revenue = financial_data_q.get('OperatingRevenue', None)
    if operating_revenue is None or operating_revenue[-1] <= 0:
        # debug(f'operating_revenue={operating_revenue}')
        rank_result = {"rank_type": "NoData", "rank": 0}
        return info_result, rank_result, revenue_data
    else:
        operating_revenue_ttm1 = sum(operating_revenue[1:])
        operating_revenue_ttm0 = sum(operating_revenue[:4])
    # debug(f'operating_revenue_ttm1={operating_revenue_ttm1}   operating_revenue_ttm0={operating_revenue_ttm0}')

    # ttm_1 -- ТТМ на текущий квартал, ttm_0 -- ТТМ на предыдущий квартал
    additional_paid_in_capital_lq1 = 0
    additional_paid_in_capital_lq0 = 0
    additional_paid_in_capital = financial_data_q.get('AdditionalPaidInCapital', None)
    if additional_paid_in_capital is not None:
        if len(additional_paid_in_capital) >= 1:
            additional_paid_in_capital_lq1 = additional_paid_in_capital[-1]
        if len(additional_paid_in_capital) >= 2:
            additional_paid_in_capital_lq0 = additional_paid_in_capital[-2]
    debug(f'additional_paid_in_capital_lq1 = {additional_paid_in_capital_lq1}  '
          f'additional_paid_in_capital_lq0 = {additional_paid_in_capital_lq0}')

    cash_and_cash_equivalents_lq1 = None
    cash_and_cash_equivalents_lq0 = None
    cash_and_cash_equivalents = financial_data_q.get('CashAndCashEquivalents', None)
    if cash_and_cash_equivalents is not None:
        if len(cash_and_cash_equivalents) >= 1:
            cash_and_cash_equivalents_lq1 = cash_and_cash_equivalents[-1]
        if len(cash_and_cash_equivalents) >= 2:
            cash_and_cash_equivalents_lq0 = cash_and_cash_equivalents[-2]
    # debug(f'cash_and_cash_equivalents_lq1 = {cash_and_cash_equivalents_lq1}  '
    #       f'cash_and_cash_equivalents_lq0 = {cash_and_cash_equivalents_lq0}')

    cash_dividends_paid_lq1 = None
    cash_dividends_paid_lq0 = None
    cash_dividends_paid = financial_data_q.get('CashDividendsPaid', None)
    if cash_dividends_paid is not None:
        if len(cash_dividends_paid) >= 1:
            cash_dividends_paid_lq1 = cash_dividends_paid[-1]
        if len(cash_dividends_paid) >= 2:
            cash_dividends_paid_lq0 = cash_dividends_paid[-2]
    # debug(f'cash_dividends_paid_ttm1={cash_dividends_paid_lq1}   cash_dividends_paid_ttm0={cash_dividends_paid_lq0}')

    current_assets_lq1 = None
    current_assets_lq0 = None
    current_assets = financial_data_q.get('CurrentAssets', None)
    if current_assets is not None:
        if len(current_assets) >= 1:
            current_assets_lq1 = current_assets[-1]
        if len(current_assets) >= 2:
            current_assets_lq0 = current_assets[-2]
    # debug(f'current_assets_lq1={current_assets_lq1}   current_assets_lq0={current_assets_lq0}')

    current_liabilities_lq1 = None
    current_liabilities_lq0 = None
    current_liabilities = financial_data_q.get('CurrentLiabilities', None)
    if current_liabilities is not None:
        if len(current_liabilities) >= 1:
            current_liabilities_lq1 = current_liabilities[-1]
        if len(current_liabilities) >= 2:
            current_liabilities_lq0 = current_liabilities[-2]
    # debug(f'current_liabilities_lq1 = {current_liabilities_lq1} '
    #       f'current_liabilities_lq0 = {current_liabilities_lq0} ')

    ebit_ttm1 = None
    ebit_ttm0 = None
    ebit = financial_data_q.get('EBIT', None)
    if ebit is not None:
        ebit_ttm1 = sum(ebit[1:])
        ebit_ttm0 = sum(ebit[:4])
    # debug(f'ebit_ttm1={ebit_ttm1}   ebit_ttm0={ebit_ttm0}')

    fcf_ttm1 = None
    fcf_ttm0 = None
    fcf = financial_data_q.get('FreeCashFlow', None)
    if fcf is None or fcf[-1] == 0:
        # debug(f'fcf={fcf}')
        rank_result = {"rank_type": "NoData", "rank": 0}
        return info_result, rank_result, revenue_data
    else:
        fcf_ttm1 = sum(fcf[1:])
        fcf_ttm0 = sum(fcf[:4])
    # debug(f'fcf_ttm1={fcf_ttm1}   fcf_ttm0={fcf_ttm0}')

    interest_expense_ttm1 = None
    interest_expense_ttm0 = None
    interest_expense = financial_data_q.get('InterestExpense', None)
    if interest_expense is not None:
        interest_expense_ttm1 = sum(interest_expense[1:])
        interest_expense_ttm0 = sum(interest_expense[:4])
    # debug(f'interest_expense_ttm1={interest_expense_ttm1}   interest_expense_ttm0={interest_expense_ttm0}')

    inventory_lq1 = 0
    inventory_lq0 = 0
    inventory = financial_data_q.get('Inventory', None)
    if inventory is not None:
        inventory_lq1 = inventory[-1]
        inventory_lq0 = inventory[-2]
    # debug(f'inventory_lq1 = {inventory_lq1}  '
    #       f'inventory_lq0 = {inventory_lq0}')

    invested_capital_lq = None
    invested_capital = financial_data_q.get('InvestedCapital', None)
    if invested_capital is not None:
        invested_capital_lq = invested_capital[-1]
    # debug(f'invested_capital_lq={invested_capital_lq}')

    long_term_debt_lq1 = None
    long_term_debt_lq0 = None
    long_term_debt = financial_data_q.get('LongTermDebtAndCapitalLeaseObligation', None)
    if long_term_debt is not None:
        long_term_debt_lq1 = long_term_debt[-1]
        long_term_debt_lq0 = long_term_debt[-2]
    # debug(f'long_term_debt_lq1 = {long_term_debt_lq1}  '
    #       f'long_term_debt_lq0 = {long_term_debt_lq0}')

    net_income_ttm1 = None
    net_income_ttm0 = None
    net_income = financial_data_q.get('NetIncome', None)
    if net_income is not None:
        net_income_ttm1 = sum(net_income[1:])
        net_income_ttm0 = sum(net_income[:4])
    # debug(f'net_income_ttm1={net_income_ttm1}   net_income_ttm0={net_income_ttm0}')

    pretax_income_ttm1 = None
    pretax_income_ttm0 = None
    pretax_income = financial_data_q.get('PretaxIncome', None)
    if pretax_income is None or pretax_income[-1] == 0:
        debug(f'pretax_income={pretax_income}')
        rank_result = {"rank_type": "NoData", "rank": 0}
        return info_result, rank_result, revenue_data
    else:
        pretax_income_ttm1 = sum(pretax_income[1:])
        pretax_income_ttm0 = sum(pretax_income[:4])
    # debug(f'pretax_income_ttm1={pretax_income_ttm1}   pretax_income_ttm0={pretax_income_ttm0}')

    receivables_lq1 = 0
    receivables_lq0 = 0
    receivables = financial_data_q.get('Receivables', None)
    if receivables is not None:
        receivables_lq1 = receivables[-1]
        receivables_lq0 = receivables[-2]
    # debug(f'receivables_lq1 = {receivables_lq1}   '
    #       f'receivables_lq0 = {receivables_lq0}')

    retained_earnings_lq1 = 0
    retained_earnings_lq0 = 0
    retained_earnings = financial_data_q.get('RetainedEarnings', None)
    if retained_earnings is not None:
        retained_earnings_lq1 = retained_earnings[-1]
        retained_earnings_lq0 = retained_earnings[-2]
    # debug(f'retained_earnings_lq1 = {retained_earnings_lq1}  '
    #       f'retained_earnings_lq0 = {retained_earnings_lq0}')

    share_issued_lq1 = None
    share_issued_lq0 = None
    share_issued = financial_data_q.get('ShareIssued', None)
    if share_issued is not None:
        share_issued_lq1 = share_issued[-1]
        share_issued_lq0 = share_issued[-2]
    # debug(f'share_issued_lq1 = {share_issued_lq1}   '
    #       f'share_issued_lq0 = {share_issued_lq0}')

    tax_provision_ttm1 = None
    tax_provision_ttm0 = None
    tax_provision = financial_data_q.get('TaxProvision', None)
    if tax_provision is not None:
        tax_provision_ttm1 = sum(tax_provision[1:])
        tax_provision_ttm0 = sum(tax_provision[:4])
    # debug(f'tax_provision_ttm1={tax_provision_ttm1}   tax_provision_ttm0={tax_provision_ttm0}')

    total_assets_lq1 = None
    total_assets_lq0 = None
    total_assets = financial_data_q.get('TotalAssets', None)
    if total_assets is None or total_assets[-1] == 0:
        debug(f'total_assets={total_assets}')
        rank_result = {"rank_type": "NoData", "rank": 0}
        return info_result, rank_result, revenue_data
    else:
        total_assets_lq1 = total_assets[-1]
        total_assets_lq0 = total_assets[-2]
    # debug(f'total_assets_lq1 = {total_assets_lq1}   '
    #       f'total_assets_lq0 = {total_assets_lq0}')

    total_liabilities_lq1 = None
    total_liabilities_lq0 = None
    total_liabilities = financial_data_q.get('TotalLiabilitiesNetMinorityInterest', None)
    if total_liabilities is not None:
        total_liabilities_lq1 = total_liabilities[-1]
        total_liabilities_lq0 = total_liabilities[-2]
    # debug(f'total_liabilities_lq1 = {total_liabilities_lq1}   '
    #       f'total_liabilities_lq0 = {total_liabilities_lq0}')

    total_non_current_assets_lq1 = None
    total_non_current_assets_lq0 = None
    total_non_current_assets = financial_data_q.get('TotalNonCurrentAssets', None)
    if total_non_current_assets is not None:
        total_non_current_assets_lq1 = total_non_current_assets[-1]
        total_non_current_assets_lq0 = total_non_current_assets[-2]
    # debug(f'total_non_current_assets_lq1 = {total_non_current_assets_lq1}   '
    #       f'total_non_current_assets_lq0 = {total_non_current_assets_lq0}')

    market_cap_lq1 = 0
    market_cap = valuation.get('MarketCap', None)
    if market_cap is not None and market_cap.size != 0:
        market_cap_lq1 = market_cap[-1]

    enterprise_value_lq1 = 0
    enterprise_value = valuation.get('EnterpriseValue', None)
    if enterprise_value is not None and enterprise_value.size != 0:
        enterprise_value_lq1 = enterprise_value[-1]

    # debug(f'enterprise_value_lq1={enterprise_value_lq1}')

    earnings_estimate_avg1 = None
    earnings_estimate_avg2 = None
    revenue_estimate_avg1 = None
    revenue_estimate_avg2 = None
    revenue_estimate_avg1_date = None
    revenue_estimate_avg2_date = None
    if not isinstance(earnings_trend_data, str):
        earnings_trend_ticker_trend = earnings_trend_data.get('trend', None)
        if len(earnings_trend_ticker_trend) >= 1:
            earnings_estimate_avg1 = earnings_trend_ticker_trend[0]['earningsEstimate']['avg']
            revenue_estimate_avg1 = earnings_trend_ticker_trend[0]['revenueEstimate']['avg']
            revenue_estimate_avg1_date = earnings_trend_ticker_trend[0]['endDate']
            if isinstance(earnings_estimate_avg1, dict):
                earnings_estimate_avg1 = None
            if isinstance(revenue_estimate_avg1, dict):
                revenue_estimate_avg1 = None

        if len(earnings_trend_ticker_trend) >= 2:
            earnings_estimate_avg2 = earnings_trend_ticker_trend[1]['earningsEstimate']['avg']
            revenue_estimate_avg2 = earnings_trend_ticker_trend[1]['revenueEstimate']['avg']
            revenue_estimate_avg2_date = earnings_trend_ticker_trend[1]['endDate']
            if isinstance(earnings_estimate_avg2, dict):
                earnings_estimate_avg2 = None
            if isinstance(revenue_estimate_avg2, dict):
                revenue_estimate_avg2 = None

    eps_estimate_ttm0 = 0
    eps_estimate_ttm1 = 0
    eps_estimate_ttm2 = 0
    earning_history = ticker_data.earning_history
    eps_actual = earning_history.get("epsActual", None)
    eps_estimate_ttm1 = earnings_estimate_avg1 if earnings_estimate_avg1 is not None else 0
    eps_estimate_ttm2 = earnings_estimate_avg2 if earnings_estimate_avg2 is not None else 0
    if eps_actual is not None and len(eps_actual) == 4 and eps_actual.dtypes.name != 'object':
        eps_estimate_ttm2 += eps_estimate_ttm1 + sum(eps_actual[2:])
        eps_estimate_ttm1 += sum(eps_actual[1:])
        eps_estimate_ttm0 = sum(eps_actual)
    # debug(f'eps_estimate_ttm0 = {eps_estimate_ttm0}   '
    #       f'eps_estimate_ttm1 = {eps_estimate_ttm1}   '
    #       f'eps_estimate_ttm2 = {eps_estimate_ttm2}')

    revenue_estimate_ttm0 = 0
    revenue_estimate_ttm1 = 0
    revenue_estimate_ttm2 = 0
    total_revenue = financial_data_q.get('TotalRevenue', None)
    revenue_estimate_ttm1 = revenue_estimate_avg1 if revenue_estimate_avg1 is not None else 0
    revenue_estimate_ttm2 = revenue_estimate_avg2 if revenue_estimate_avg2 is not None else 0
    if total_revenue is not None and total_revenue.dtype.name != 'object':
        if len(total_revenue) == 5:
            revenue_estimate_ttm2 += revenue_estimate_ttm1 + sum(total_revenue[3:])
            revenue_estimate_ttm1 += sum(total_revenue[2:])
            revenue_estimate_ttm0 = sum(total_revenue[1:])
        elif len(total_revenue) == 4:
            revenue_estimate_ttm2 += revenue_estimate_ttm1 + sum(total_revenue[2:])
            revenue_estimate_ttm1 += sum(total_revenue[1:])
            revenue_estimate_ttm0 = sum(total_revenue)
    # debug(f'revenue_estimate_ttm0 = {revenue_estimate_ttm0}   '
    #       f'revenue_estimate_ttm1 = {revenue_estimate_ttm1}   '
    #       f'revenue_estimate_ttm2 = {revenue_estimate_ttm2}')

    dates = financial_data_q.get('asOfDate', None)
    for rdate, value in zip(dates, total_revenue):
        if not pd.isna(value):
            revenue_data[pd.to_datetime(rdate).strftime('%Y-%m-%d')] = value
    if revenue_estimate_avg1 is not None:
        revenue_data[revenue_estimate_avg1_date] = revenue_estimate_avg1
    if revenue_estimate_avg2 is not None:
        revenue_data[revenue_estimate_avg2_date] = revenue_estimate_avg2
    # debug(f'revenue_data = {revenue_data}')

    # revenue_gowth_rate = []
    # if revenue_estimate_ttm0 != 0 and revenue_estimate_ttm1 != 0 and revenue_estimate_ttm2 != 0:
    #     if revenue_estimate_ttm_1 != 0:
    #         revenue_gowth_rate1 = (revenue_estimate_ttm0 - revenue_estimate_ttm_1)/revenue_estimate_ttm_1 * 100
    #         revenue_gowth_rate.append(revenue_gowth_rate1)
    #     revenue_gowth_rate2 = (revenue_estimate_ttm1 - revenue_estimate_ttm0)/revenue_estimate_ttm0 * 100
    #     revenue_gowth_rate.append(revenue_gowth_rate2)
    #     revenue_gowth_rate3 = (revenue_estimate_ttm2 - revenue_estimate_ttm1)/revenue_estimate_ttm1 * 100
    #     revenue_gowth_rate.append(revenue_gowth_rate3)
    # debug(f"revenue_gowth_rate = {revenue_gowth_rate}")

    # debug(f'\n\n----------- Расчетные величины -----------\n')
    # -------------- Далее расчеты для скоринга --------------
    # Net Operating Profit After Tax = NOPAT = EBIT*(1- (Tax Provision/Pretax Income))
    nopat_ttm1 = 0
    nopat_ttm0 = 0
    if current_liabilities is not None and ebit is not None:
        if tax_provision_ttm1 is not None and pretax_income_ttm1 is not None and ebit_ttm1 is not None:
            nopat_ttm1 = ebit_ttm1 * (1 - (tax_provision_ttm1 / pretax_income_ttm1))
            nopat_ttm0 = ebit_ttm0 * (1 - (tax_provision_ttm0 / pretax_income_ttm0))
        # debug(f'nopat_ttm1={nopat_ttm1}   nopat_ttm0={nopat_ttm0}')

    # Рентабельность всех активов через NOPAT ---  NOPAT/Total Assets
    profitability = 0
    if nopat_ttm1 is not None and total_assets_lq1 is not None:
        if current_liabilities is not None and ebit is not None:
            profitability = nopat_ttm1 / total_assets_lq1
        else:
            profitability = net_income_ttm1 / total_assets_lq1
    # debug(f'profitability > 0 (NOPAT/TOTAL ASSETS)={profitability} ')

    # Дельта рентабельности всех активов через Free Cash Flow --- D_(FCF/Total Assets)
    delta_profitability = (fcf_ttm1 / total_assets_lq1) - (fcf_ttm0 / total_assets_lq0)
    # debug(f'delta_profitability > 0 ={delta_profitability} ')

    # ROIC – рентабельность инвестированного капитала --- NOPAT/Invested Capital
    roic = 0
    if current_liabilities is not None and ebit is not None:
        if invested_capital_lq is not None and invested_capital_lq != 0:
            roic = (nopat_ttm1 / invested_capital_lq)
    else:
        if invested_capital_lq is not None and invested_capital_lq != 0:
            roic = (net_income_ttm1 / invested_capital_lq)
    # debug(f'roic > 0 ={roic} ')

    # Дельта Shareholder’s Equity без учета трежари акций --- D_(Retained Earnings+Additional Paid On Capital)
    delta_shareholders_equity = (retained_earnings_lq1 + additional_paid_in_capital_lq1) - \
                                (retained_earnings_lq0 + additional_paid_in_capital_lq0)
    # debug(f'delta_shareholders_equity > 0 ={delta_shareholders_equity} ')

    # Margin --- D_(NOPAT/Total Operating Revenue)
    if current_liabilities is not None and ebit is not None:
        margin = (nopat_ttm1 / operating_revenue_ttm1) - (nopat_ttm0 / operating_revenue_ttm0)
    else:
        margin = (fcf_ttm1 / operating_revenue_ttm1) - (fcf_ttm0 / operating_revenue_ttm0)
    # debug(f'margin > 0 ={margin} ')

    # Чистая ликвидность --- Cash and equivalents / current liabilities
    net_liquidity = 0
    if current_liabilities_lq1 is not None and current_liabilities_lq1 != 0:
        if current_assets_lq1 is not None:
            net_liquidity = current_assets_lq1 / current_liabilities_lq1
        else:
            net_liquidity = 0
    # debug(f'net_liquidity > 1VG / > 2Bagger ={net_liquidity} ')

    # Улучшение чистой ликвидности --- D_(Cash and equivalents / current liabilities)
    minuend = 0
    if current_liabilities_lq1 is not None and current_liabilities_lq1 != 0:
        minuend = (current_assets_lq1 / current_liabilities_lq1)
    else:
        minuend = (total_assets_lq1 / total_liabilities_lq1)

    subtrahend = 0
    if current_liabilities_lq0 is not None and current_liabilities_lq0 != 0:
        subtrahend = (current_assets_lq0 / current_liabilities_lq0)
    else:
        subtrahend = (total_assets_lq0 / total_liabilities_lq0)

    improving_net_liquidity = minuend - subtrahend
    if improving_net_liquidity < 0:
        improving_net_liquidity = 0
    # debug(f'improving_net_liquidity > 0 ={improving_net_liquidity} ')

    # Уменьшение дебиторской задолженности --- D_(Receivables + Inventory)
    decrease_in_receivables = (receivables_lq1 + inventory_lq1) - (receivables_lq0 + inventory_lq0)
    # debug(f'decrease_in_receivables < 0 ={decrease_in_receivables} ')

    # Плечо – отношение необоротных активов к длинным долгам  --- Non Current Assets/Long Debt
    leverage1 = 0
    if current_liabilities is not None and ebit is not None:
        if long_term_debt_lq1 is not None and long_term_debt_lq1 != 0:
            leverage1 = total_non_current_assets_lq1 / long_term_debt_lq1
    else:
        if long_term_debt_lq1 is not None and long_term_debt_lq1 != 0:
            leverage1 = total_assets_lq1 / long_term_debt_lq1
    # debug(f'leverage < 1 VG / > 1 Bagger ={leverage1} ')

    # Плечо – Дельта отношение  ---  D_(Non Current Assets/Long Debt)
    leverage0 = 0
    if current_liabilities is not None and ebit is not None:
        if long_term_debt_lq0 is not None and long_term_debt_lq0 != 0:
            leverage0 = total_non_current_assets_lq0 / long_term_debt_lq0
    else:
        if long_term_debt_lq0 is not None and long_term_debt_lq0 != 0:
            leverage0 = total_assets_lq0 / long_term_debt_lq0
    delta_leverage = leverage1 - leverage0
    # debug(f'delta_leverage > 0 ={delta_leverage} ')

    # Interest Coverage Оплата процентов  ---  EBIT/Interest Expenses
    interest_coverage = 0
    if interest_expense_ttm1 is not None and interest_expense_ttm1 != 0:
        if ebit_ttm1 is not None:
            interest_coverage = ebit_ttm1 / interest_expense_ttm1
        else:
            interest_coverage = 0
    # debug(f'interest_coverage > 6 ={interest_coverage} ')

    is_value = False
    is_bagger = False
    is_growth = False
    is_nontype = False
    is_fin = False
    if current_liabilities is None and ebit is None:
        is_fin = True
    # debug(f'\n\n----------- Сепараторы -----------\n')
    value_separator = None
    bagger_separator = 0
    growth_separator = 0
    if current_liabilities is not None and ebit is not None:
        value_separator = (enterprise_value_lq1 / fcf_ttm1 * enterprise_value_lq1 / total_assets_lq1)
    else:
        value_separator = (market_cap_lq1 / fcf_ttm1 * market_cap_lq1 / total_assets_lq1)

    if revenue_estimate_ttm1 > 0:
        growth_separator += 1
    if revenue_estimate_ttm2 > 0:
        growth_separator += 1
    if eps_estimate_ttm1 > 0:
        growth_separator += 1
    if eps_estimate_ttm2 > 0:
        growth_separator += 1

    if cash_dividends_paid_lq1 is not None and cash_dividends_paid_lq1 == 0:
        bagger_separator += 1
    if (share_issued_lq1 - share_issued_lq0) > 0:
        bagger_separator += 1
    if net_liquidity > 2:
        bagger_separator += 1
    if leverage1 < 1:
        bagger_separator += 1

    # debug(f"value_separator = {value_separator}")
    # debug(f'growth_separator = {growth_separator}')
    # debug(f'bagger_separator = {bagger_separator}')

    if nopat_ttm1 is None and fcf_ttm1 is None:
        debug(f'nopat_ttm1 is None and fcf_ttm1 is None!!!!', ERROR)
        rank_result = {"rank_type": "NoData", "rank": 0}
        return info_result, rank_result, revenue_data
    if (nopat_ttm1 is not None and nopat_ttm1 <= 0) or (fcf_ttm1 is not None and fcf_ttm1 <= 0):
        if bagger_separator >= 3:
            is_bagger = True
            rank_result["rank_type"] = "Bagger"
        else:
            is_nontype = True
            rank_result["rank_type"] = "NonType"

    elif (nopat_ttm1 is not None and nopat_ttm1 > 0) and (fcf_ttm1 is not None and fcf_ttm1 > 0):
        if 25 > value_separator > 0:
            rank_result["rank_type"] = "Value"
            is_value = True
        elif value_separator >= 25:
            if growth_separator >= 3:
                is_growth = True
                rank_result["rank_type"] = "Growth"
            else:
                is_nontype = True
                rank_result["rank_type"] = "NonType"
        elif pd.isna(value_separator):
            if growth_separator >= 3:
                is_growth = True
                rank_result["rank_type"] = "Growth"
            else:
                is_nontype = True
                rank_result["rank_type"] = "NonType"
    elif (nopat_ttm1 is None or pd.isna(nopat_ttm1)) and (fcf_ttm1 is not None and fcf_ttm1 > 0):
        # debug(f'NOPAT is None', WARNING)
        if 25 > value_separator > 0:
            rank_result["rank_type"] = "Value"
            is_value = True
        elif value_separator >= 25:
            if growth_separator >= 3:
                is_growth = True
                rank_result["rank_type"] = "Growth"
            else:
                is_nontype = True
                rank_result["rank_type"] = "NonType"
        elif pd.isna(value_separator):
            if growth_separator >= 3:
                is_growth = True
                rank_result["rank_type"] = "Growth"
            else:
                is_nontype = True
                rank_result["rank_type"] = "NonType"
    elif (nopat_ttm1 is not None and nopat_ttm1 > 0) and (fcf_ttm1 is None or pd.isna(fcf_ttm1)):
        debug(f'fcf_ttm1 is None', WARNING)
        if 25 > value_separator > 0:
            rank_result["rank_type"] = "Value"
            is_value = True
        elif value_separator >= 25:
            if growth_separator >= 3:
                is_growth = True
                rank_result["rank_type"] = "Growth"
            else:
                is_nontype = True
                rank_result["rank_type"] = "NonType"
        elif pd.isna(value_separator):
            if growth_separator >= 3:
                is_growth = True
                rank_result["rank_type"] = "Growth"
            else:
                is_nontype = True
                rank_result["rank_type"] = "NonType"

    if nopat_ttm1 is not None and not pd.isna(nopat_ttm1) and nopat_ttm0 is not None and not pd.isna(nopat_ttm0):
        if nopat_ttm1 > 0 and nopat_ttm1 > nopat_ttm0:
            rank_result["nopat"] = 2
        elif nopat_ttm1 > 0 and nopat_ttm1 < nopat_ttm0:
            rank_result["nopat"] = 1
        elif nopat_ttm1 < 0 and nopat_ttm1 > nopat_ttm0:
            rank_result["nopat"] = 0
        elif nopat_ttm1 < 0 and nopat_ttm1 < nopat_ttm0:
            rank_result["nopat"] = -1
    else:
        rank_result["nopat"] = None

    # debug(f'\n\n----------- Rank -----------\n')
    rank = 0
    if is_fin:
        if profitability is None or pd.isna(profitability):
            rank_result["profitability"] = None
        elif profitability > 0:
            rank += 1
            rank_result["profitability"] = 1
        elif profitability <= 0:
            rank_result["profitability"] = 0

        if delta_profitability is None or pd.isna(delta_profitability):
            rank_result["delta_profitability"] = None
        elif delta_profitability > 0:
            rank += 1
            rank_result["delta_profitability"] = 1
        elif delta_profitability <= 0:
            rank_result["delta_profitability"] = 1

        if roic is None or pd.isna(roic):
            rank_result["roic"] = None
        elif roic > 0:
            rank += 1
            rank_result["roic"] = 1
        elif roic <= 0:
            rank_result["roic"] = 0

        if margin is None or pd.isna(margin):
            rank_result["margin"] = None
        elif margin > 0:
            rank += 1
            rank_result["margin"] = 1
        elif margin <= 0:
            rank_result["margin"] = 0

        if delta_shareholders_equity is None or pd.isna(delta_shareholders_equity):
            rank_result["delta_shareholders_equity"] = None
        elif delta_shareholders_equity > 0:
            rank += 1
            rank_result["delta_shareholders_equity"] = 1
        elif delta_shareholders_equity <= 0:
            rank_result["delta_shareholders_equity"] = 0

        rank_result["interest_coverage"] = None
        rank_result["net_liquidity"] = None

        if improving_net_liquidity is None or pd.isna(improving_net_liquidity):
            rank_result["improving_net_liquidity"] = None
        elif improving_net_liquidity > 0:
            rank += 1
            rank_result["improving_net_liquidity"] = 1
        elif improving_net_liquidity <= 0:
            rank_result["improving_net_liquidity"] = 0

        rank_result["decrease_in_receivables"] = None
        rank_result["leverage1"] = None

        if leverage0 is None or pd.isna(leverage0):
            rank_result["leverage0"] = None
        elif leverage0 > 0:
            rank += 1
            rank_result["leverage0"] = 1
        elif leverage0 <= 0:
            rank_result["leverage0"] = 0

        if revenue_estimate_ttm1 > revenue_estimate_ttm0:
            rank += 1
            rank_result["revenue_estimate_ttm1"] = 1
        elif revenue_estimate_ttm1 <= revenue_estimate_ttm0:
            rank_result["revenue_estimate_ttm1"] = 0
        elif revenue_estimate_ttm1 is None or pd.isna(revenue_estimate_ttm1):
            rank_result["revenue_estimate_ttm1"] = None

        if revenue_estimate_ttm2 > revenue_estimate_ttm1:
            rank += 1
            rank_result["revenue_estimate_ttm2"] = 1
        elif revenue_estimate_ttm2 <= revenue_estimate_ttm1:
            rank_result["revenue_estimate_ttm2"] = 0
        elif revenue_estimate_ttm2 is None or pd.isna(revenue_estimate_ttm2):
            rank_result["revenue_estimate_ttm2"] = None

        if eps_estimate_ttm1 > eps_estimate_ttm0:
            rank += 1
            rank_result["eps_estimate_ttm1"] = 1
        elif eps_estimate_ttm1 <= eps_estimate_ttm0:
            rank_result["eps_estimate_ttm1"] = 0
        elif eps_estimate_ttm1 is None or pd.isna(eps_estimate_ttm1):
            rank_result["eps_estimate_ttm1"] = None

        if eps_estimate_ttm2 > eps_estimate_ttm1:
            rank += 1
            rank_result["eps_estimate_ttm2"] = 1
        elif eps_estimate_ttm2 <= eps_estimate_ttm1:
            rank_result["eps_estimate_ttm2"] = 0
        elif eps_estimate_ttm2 is None or pd.isna(eps_estimate_ttm2):
            rank_result["eps_estimate_ttm2"] = None

        if value_separator < 25:
            rank += 1
        debug(f'Fin. rank = {rank}\n', WARNING)
    elif is_bagger:
        rank_result["profitability"] = None

        if delta_profitability is None or pd.isna(delta_profitability):
            rank_result["delta_profitability"] = None
        elif delta_profitability > 0:
            rank += 1
            rank_result["delta_profitability"] = 1
        elif delta_profitability <= 0:
            rank_result["delta_profitability"] = 1

        rank_result["roic"] = None

        rank_result["margin"] = None

        rank_result["delta_shareholders_equity"] = None

        if interest_coverage is None or pd.isna(interest_coverage):
            rank_result["interest_coverage"] = None
        elif interest_coverage >= 6:
            rank += 1
            rank_result["interest_coverage"] = 1
        elif interest_coverage < 6:
            rank_result["interest_coverage"] = 0

        if net_liquidity is None or pd.isna(net_liquidity):
            rank_result["net_liquidity"] = None
        elif net_liquidity > 1:
            rank += 1
            rank_result["net_liquidity"] = 1
        elif net_liquidity <= 1:
            rank_result["net_liquidity"] = 0

        if improving_net_liquidity is None or pd.isna(improving_net_liquidity):
            rank_result["improving_net_liquidity"] = None
        elif improving_net_liquidity > 0:
            rank += 1
            rank_result["improving_net_liquidity"] = 1
        elif improving_net_liquidity <= 0:
            rank_result["improving_net_liquidity"] = 0

        if decrease_in_receivables is None or pd.isna(decrease_in_receivables):
            rank_result["decrease_in_receivables"] = None
        elif decrease_in_receivables < 0:
            rank += 1
            rank_result["decrease_in_receivables"] = 1
        elif decrease_in_receivables >= 0:
            rank_result["decrease_in_receivables"] = 0

        if leverage1 is None or pd.isna(leverage1):
            rank_result["leverage1"] = None
        elif leverage1 > 1:
            rank += 1
            rank_result["leverage1"] = 1
        elif leverage1 <= 1:
            rank_result["leverage1"] = 0

        if leverage0 is None or pd.isna(leverage0):
            rank_result["leverage0"] = None
        elif leverage0 > 0:
            rank += 1
            rank_result["leverage0"] = 1
        elif leverage0 <= 0:
            rank_result["leverage0"] = 0

        if revenue_estimate_ttm1 > revenue_estimate_ttm0:
            rank += 1
            rank_result["revenue_estimate_ttm1"] = 1
        elif revenue_estimate_ttm1 <= revenue_estimate_ttm0:
            rank_result["revenue_estimate_ttm1"] = 0
        elif revenue_estimate_ttm1 is None or pd.isna(revenue_estimate_ttm1):
            rank_result["revenue_estimate_ttm1"] = None

        if revenue_estimate_ttm2 > revenue_estimate_ttm1:
            rank += 1
            rank_result["revenue_estimate_ttm2"] = 1
        elif revenue_estimate_ttm2 <= revenue_estimate_ttm1:
            rank_result["revenue_estimate_ttm2"] = 0
        elif revenue_estimate_ttm2 is None or pd.isna(revenue_estimate_ttm2):
            rank_result["revenue_estimate_ttm2"] = None

        if eps_estimate_ttm1 > eps_estimate_ttm0:
            rank += 1
            rank_result["eps_estimate_ttm1"] = 1
        elif eps_estimate_ttm1 <= eps_estimate_ttm0:
            rank_result["eps_estimate_ttm1"] = 0
        elif eps_estimate_ttm1 is None or pd.isna(eps_estimate_ttm1):
            rank_result["eps_estimate_ttm1"] = None

        if eps_estimate_ttm2 > eps_estimate_ttm1:
            rank += 1
            rank_result["eps_estimate_ttm2"] = 1
        elif eps_estimate_ttm2 <= eps_estimate_ttm1:
            rank_result["eps_estimate_ttm2"] = 0
        elif eps_estimate_ttm2 is None or pd.isna(eps_estimate_ttm2):
            rank_result["eps_estimate_ttm2"] = None

        debug(f'Bagger. rank = {rank}\n', WARNING)

    elif is_growth or is_value or is_nontype:
        if profitability is None or pd.isna(profitability):
            rank_result["profitability"] = None
        elif profitability > 0:
            rank += 1
            rank_result["profitability"] = 1
        elif profitability <= 0:
            rank_result["profitability"] = 0

        if delta_profitability is None or pd.isna(delta_profitability):
            rank_result["delta_profitability"] = None
        elif delta_profitability > 0:
            rank += 1
            rank_result["delta_profitability"] = 1
        elif delta_profitability <= 0:
            rank_result["delta_profitability"] = 1

        if roic is None or pd.isna(roic):
            rank_result["roic"] = None
        elif roic > 0:
            rank += 1
            rank_result["roic"] = 1
        elif roic <= 0:
            rank_result["roic"] = 0

        if margin is None or pd.isna(margin):
            rank_result["margin"] = None
        elif margin > 0:
            rank += 1
            rank_result["margin"] = 1
        elif margin <= 0:
            rank_result["margin"] = 0

        if delta_shareholders_equity is None or pd.isna(delta_shareholders_equity):
            rank_result["delta_shareholders_equity"] = None
        elif delta_shareholders_equity > 0:
            rank += 1
            rank_result["delta_shareholders_equity"] = 1
        elif delta_shareholders_equity <= 0:
            rank_result["delta_shareholders_equity"] = 0

        if interest_coverage is None or pd.isna(interest_coverage):
            rank_result["interest_coverage"] = None
        elif interest_coverage >= 6:
            rank += 1
            rank_result["interest_coverage"] = 1
        elif interest_coverage < 6:
            rank_result["interest_coverage"] = 0

        if net_liquidity is None or pd.isna(net_liquidity):
            rank_result["net_liquidity"] = None
        elif net_liquidity > 1:
            rank += 1
            rank_result["net_liquidity"] = 1
        elif net_liquidity <= 1:
            rank_result["net_liquidity"] = 0

        if improving_net_liquidity is None or pd.isna(improving_net_liquidity):
            rank_result["improving_net_liquidity"] = None
        elif improving_net_liquidity > 0:
            rank += 1
            rank_result["improving_net_liquidity"] = 1
        elif improving_net_liquidity <= 0:
            rank_result["improving_net_liquidity"] = 0

        if decrease_in_receivables is None or pd.isna(decrease_in_receivables):
            rank_result["decrease_in_receivables"] = None
        elif decrease_in_receivables < 0:
            rank += 1
            rank_result["decrease_in_receivables"] = 1
        elif decrease_in_receivables >= 0:
            rank_result["decrease_in_receivables"] = 0

        if leverage1 is None or pd.isna(leverage1):
            rank_result["leverage1"] = None
        elif leverage1 > 1:
            rank += 1
            rank_result["leverage1"] = 1
        elif leverage1 <= 1:
            rank_result["leverage1"] = 0

        if leverage0 is None or pd.isna(leverage0):
            rank_result["leverage0"] = None
        elif leverage0 > 0:
            rank += 1
            rank_result["leverage0"] = 1
        elif leverage0 <= 0:
            rank_result["leverage0"] = 0

        if revenue_estimate_ttm1 > revenue_estimate_ttm0:
            rank += 1
            rank_result["revenue_estimate_ttm1"] = 1
        elif revenue_estimate_ttm1 <= revenue_estimate_ttm0:
            rank_result["revenue_estimate_ttm1"] = 0
        elif revenue_estimate_ttm1 is None or pd.isna(revenue_estimate_ttm1):
            rank_result["revenue_estimate_ttm1"] = None

        if revenue_estimate_ttm2 > revenue_estimate_ttm1:
            rank += 1
            rank_result["revenue_estimate_ttm2"] = 1
        elif revenue_estimate_ttm2 <= revenue_estimate_ttm1:
            rank_result["revenue_estimate_ttm2"] = 0
        elif revenue_estimate_ttm2 is None or pd.isna(revenue_estimate_ttm2):
            rank_result["revenue_estimate_ttm2"] = None

        if eps_estimate_ttm1 > eps_estimate_ttm0:
            rank += 1
            rank_result["eps_estimate_ttm1"] = 1
        elif eps_estimate_ttm1 <= eps_estimate_ttm0:
            rank_result["eps_estimate_ttm1"] = 0
        elif eps_estimate_ttm1 is None or pd.isna(eps_estimate_ttm1):
            rank_result["eps_estimate_ttm1"] = None

        if eps_estimate_ttm2 > eps_estimate_ttm1:
            rank += 1
            rank_result["eps_estimate_ttm2"] = 1
        elif eps_estimate_ttm2 <= eps_estimate_ttm1:
            rank_result["eps_estimate_ttm2"] = 0
        elif eps_estimate_ttm2 is None or pd.isna(eps_estimate_ttm2):
            rank_result["eps_estimate_ttm2"] = None

        if is_value:
            if 25 > value_separator > 0:
                rank += 1
            debug(f'Value. rank = {rank}\n', WARNING)
        elif is_growth:
            debug(f'Growth. rank = {rank}\n', WARNING)
        elif is_nontype:
            debug(f'NonType. rank = {rank}\n', WARNING)

    if cash_dividends_paid_lq1 is not None and not pd.isna(cash_dividends_paid_lq1):
        if cash_dividends_paid_lq1 < 0:
            rank_result["cash_dividends_paid"] = 1
        else:
            rank_result["cash_dividends_paid"] = 0
    else:
        rank_result["cash_dividends_paid"] = None

    if share_issued_lq1 is not None and not pd.isna(share_issued_lq1) and share_issued_lq0 is not None and not pd.isna(
            share_issued_lq0):
        if (share_issued_lq1 - share_issued_lq0) <= 0:
            rank_result["D_issued"] = 1
        else:
            rank_result["D_issued"] = 0
    else:
        rank_result["D_issued"] = None

    rank_result["rank"] = rank
    rank_result["is_fin"] = is_fin
    rank_result["is_bagger"] = is_bagger

    return info_result, rank_result, revenue_data


# ============================== FINVIZ TREEMAP GET ================================
def get_finviz_treemaps(driver=None, img_out_path_=IMAGES_OUT_PATH):
    treemaps = {
        'treemap_1d': 'https://finviz.com/map.ashx?t=sec_all',
        'treemap_ytd': 'https://finviz.com/map.ashx?t=sec_all&st=ytd',
        'global_treemap_1d': 'https://finviz.com/map.ashx?t=geo',
        'global_treemap_ytd': 'https://finviz.com/map.ashx?t=geo&st=ytd',
    }
    with driver:
        for k, v in treemaps.items():
            img_path = os.path.join(img_out_path_, k + '.png')
            try:
                driver.get(v)
                sleep(3)
                chart = driver.find_element_by_class_name("hover-canvas")
                image = chart.screenshot_as_png
                image_stream = io.BytesIO(image)
                im = Image.open(image_stream)
                im.save(img_path)
            except Exception as e03:
                debug(e03)
                return
    debug('Get Finviz Treemap complete' + '\n')


# ============================== COIN360 TREEMAP GET ================================
def get_coins360_treemaps(driver=None, img_out_path_=IMAGES_OUT_PATH):
    url_ = 'https://coin360.com/?exceptions=[USDT%2CUSDC]&period=24h&range=[500000000%2C295729609429]'
    with driver:
        img_path = os.path.join(img_out_path_, 'coins_treemap' + '.png')
        try:
            driver.get(url_)
            sleep(5)
            chart = driver.find_element_by_class_name("MapBox")
            image = chart.screenshot_as_png
            image_stream = io.BytesIO(image)
            im = Image.open(image_stream)
            im.save(img_path)
        except Exception as e04:
            debug(e04)
            return
    debug('Get coin360 Treemap complete' + '\n')


def get_economics_v2(driver=None, img_out_path_=IMAGES_OUT_PATH):
    charts = {
        'Interest Rate': 'https://tradingeconomics.com/united-states/interest-rate',
        'Inflation Rate': 'https://tradingeconomics.com/united-states/inflation-cpi',
        'Unemployment Rate': 'https://tradingeconomics.com/united-states/unemployment-rate',
        'Composite PMI': 'https://tradingeconomics.com/united-states/composite-pmi'
    }
    try:
        with driver:
            for k, v in charts.items():
                im_path = os.path.join(img_out_path_, k + '.png')
                driver.get(v)
                sleep(5)
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Forecast"))).click()
                debug(f'Button Forecast has been clicked for {k}')
                five = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "5Y")))
                driver.execute_script("return arguments[0].click();", five)
                debug(f'Button 5y has been clicked for {k}')
                chart = driver.find_element_by_class_name("chart-figure")
                sleep(6)
                image = chart.screenshot_as_png
                image_stream = io.BytesIO(image)
                im = Image.open(image_stream)
                im.save(im_path)
                im = Image.open(im_path)
                img_h = 338
                img_w = 748
                im = im.crop((0, 0, img_w - 26, img_h - 30))
                im.save(im_path, quality=100, subsampling=0)
                debug(f'{k} Chart has been saved')

    except Exception as e06a:
        debug(e06a)
        return
    debug('Get Economics complete' + '\n')


# ============================== TW GET ================================
def get_tw_charts(driver=None, img_out_path_=IMAGES_OUT_PATH):
    treemaps = {
        'sectors': 'https://www.tradingview.com/chart/8ql9Y9yV/',
        'crypto': 'https://www.tradingview.com/chart/HHWJel9w/',
        'rtsi': 'https://www.tradingview.com/chart/PV8hXeeD/',
        'world': 'https://www.tradingview.com/chart/Z9Sidx11/',
    }
    try:
        with driver:
            for k, v in treemaps.items():
                im_path = os.path.join(img_out_path_, k + '.png')
                driver.get(v)
                sleep(15)
                elem = driver.find_element_by_class_name("chart-container-border")
                webdriver.ActionChains(driver).move_to_element(elem).perform()
                driver.execute_script("return arguments[0].scrollIntoView();", elem)
                # sleep(5)
                try:
                    close_button1 = driver.find_element_by_class_name(
                        'tv-dialog__close close-d1KI_uC8 dialog-close-3phLlAHH js-dialog__close')
                    driver.execute_script("arguments[0].click();", close_button1)
                except Exception as e1:
                    debug(e1)
                try:
                    close_button2 = driver.find_element_by_xpath("//button[@class='close-button-7uy97o5_']").click()
                    driver.execute_script("arguments[0].click();", close_button2)
                    sleep(3)
                except Exception as e2:
                    debug(e2)
                try:
                    close_button3 = driver.find_element_by_class_name(
                        'closeIcon-29Jv6tZx')
                    driver.execute_script("arguments[0].click();", close_button3)
                except Exception as e3:
                    debug(e3)

                elem = driver.find_element_by_class_name("layout__area--top")
                webdriver.ActionChains(driver).move_to_element(elem).click().perform()

                chart = driver.find_element_by_class_name("layout__area--center")
                image = chart.screenshot_as_png
                image_stream = io.BytesIO(image)
                im = Image.open(image_stream)
                im.save(im_path)
                add_watermark(im_path, im_path, 100)
                debug(f"IMG Path:{im_path}")
                # driver.get_screenshot_as_file(im_path)
                # im = Image.open(im_path)
                # width, height = im.size
                # cropped = im.crop((56, 44, width - 320, height - 43))
                # cropped.save(im_path, quality=100, subsampling=0)
    except Exception as e06:
        debug(e06)
        return
    debug('Get TW Charts complete' + '\n')


# ============================== SMA50 GET ================================
def get_sma50(ag=None, img_out_path_=IMAGES_OUT_PATH):
    """
    csv load last value
    future - chart # TODO Реализовать историю и графики
    """
    headers = {'User-Agent': ag}
    urls_d = {
        'NyseT': 'https://finviz.com/screener.ashx?v=151&f=exch_nyse&ft=4',
        'NyseA': 'https://finviz.com/screener.ashx?v=151&f=exch_nyse,ta_sma50_pa&ft=4',
        'NasdT': 'https://finviz.com/screener.ashx?v=151&f=exch_nasd&ft=4',
        'NasdA': 'https://finviz.com/screener.ashx?v=151&f=exch_nasd,ta_sma50_pa&ft=4',
        'SPXT': 'https://finviz.com/screener.ashx?v=151&f=idx_sp500&ft=4',
        'SPXA': 'https://finviz.com/screener.ashx?v=151&f=idx_sp500,ta_sma50_pa&ft=4'
    }
    items_ = {}
    try:
        for k, v in urls_d.items():
            sleep(1)
            debug(f'Try get key: {k}')
            html = requests.get(v, headers=headers).text
            soup = BeautifulSoup(html, "html.parser")
            table = soup.find('td', {"class": "count-text"}).text.strip('Total:  ')
            items_[k] = int(table[:-3])
    except TypeError as e01:
        debug(e01)
        return
    items_['NYSE Trending Stocks %'] = str(
        round(items_['NyseA'] * 100 / items_['NyseT'], 2)) + '%' + ' акций NYSE в тренде'
    items_['NASDAQ Trending Stocks %'] = str(
        round(items_['NasdA'] * 100 / items_['NasdT'], 2)) + '%' + ' акций NASDAQ в тренде'
    items_['SP500 Trending Stocks %'] = str(
        round(items_['SPXA'] * 100 / items_['SPXT'], 2)) + '%' + ' акций SP500 в тренде'
    items_.pop('NyseT')
    items_.pop('NyseA')
    items_.pop('NasdT')
    items_.pop('NasdA')
    items_.pop('SPXT')
    items_.pop('SPXA')
    with open(img_out_path_ + 'sma50.csv', 'w+') as f:
        write = csv.DictWriter(f, items_.keys())
        # write.writeheader()
        write.writerow(items_)
    debug('sma50 complete')


# ============================== MOEX TREEMAP GET ================================
def get_moex(driver=None, img_out_path_=IMAGES_OUT_PATH):
    try:
        with driver:
            driver.get('https://smart-lab.ru/q/map/')
            sleep(10)
            im_path = os.path.join(img_out_path_, 'moex_map.png')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "chart_div_shares")))
            chart = driver.find_element_by_id("chart_div_shares")
            sleep(6)
            image = chart.screenshot_as_png
            image_stream = io.BytesIO(image)
            im = Image.open(image_stream)
            im.save(im_path)
            # im = Image.open(im_path)
            # img_h = 338
            # img_w = 748
            # im = im.crop((0, 0, img_w - 2, img_h - 4))
            # im.save(im_path, quality=100, subsampling=0)
            debug(f'Chart has been saved')

    except Exception as e06a:
        debug(e06a)
        return
    debug('Get moexmap complete' + '\n')


def qt_curve(ag=None, img_out_path_=IMAGES_OUT_PATH):
    headers = {'User-Agent': ag}
    xml = 'https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=month(NEW_DATE)%20eq%201%20and%20year(NEW_DATE)%20eq%202021'
    html = requests.get(xml, headers=headers).text
    soup = BeautifulSoup(html, "xml")
    _date = soup.findAll('NEW_DATE')[-1].text.split('T')[0]
    _1m = soup.findAll('BC_1MONTH')[-1].text
    _2m = soup.findAll('BC_2MONTH')[-1].text
    _3m = soup.findAll('BC_3MONTH')[-1].text
    _6m = soup.findAll('BC_6MONTH')[-1].text
    _1y = soup.findAll('BC_1YEAR')[-1].text
    _2y = soup.findAll('BC_2YEAR')[-1].text
    _3y = soup.findAll('BC_3YEAR')[-1].text
    _5y = soup.findAll('BC_5YEAR')[-1].text
    _7y = soup.findAll('BC_7YEAR')[-1].text
    _10y = soup.findAll('BC_10YEAR')[-1].text
    _20y = soup.findAll('BC_20YEAR')[-1].text
    _30y = soup.findAll('BC_30YEAR')[-1].text
    msg = {'Date': _date, '1M': _1m, '2M': _2m, '3M': _3m, '6M': _6m, '1Y': _1y, '2Y': _2y, '3Y': _3y, '5Y': _5y,
           '7Y': _7y, '10Y': _10y, '20Y': _20y, '30Y': _30y}

    with open(img_out_path_ + 'treasury_curve.csv', 'w+') as f:
        write = csv.DictWriter(f, msg.keys())
        write.writeheader()
        write.writerow(msg)
    debug('qt_curve complete')


def spx_yield(img_out_path_=IMAGES_OUT_PATH):
    x = quandl.get("MULTPL/SP500_DIV_YIELD_MONTH", authtoken="gWq5SV_V-yFkXVMgrwwy", rows=1)
    x = str(x)
    with open(img_out_path_ + 'spx_yield.csv', 'w+') as f:
        f.write(f'{x}')
    debug('spx_yield complete')


def vix_curve(driver=None, img_out_path_=IMAGES_OUT_PATH):
    url_ = 'http://vixcentral.com/'
    img_curve = os.path.join(img_out_path_, 'vix_curve' + '.png')
    try:
        with driver:
            driver.get(url_)
            sleep(3)
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='VIX Index']"))).click()
            debug('Vix disabled, button has been clicked')
            sleep(4)
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "highcharts-button-symbol"))).click()
            debug('Menu button has been clicked')
            sleep(5)
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//li[contains(text(),'Download PNG image')]"))).click()
            debug('PNG has been clicked')
            sleep(5)
        im = Image.open('vix-futures-term-structu.png')
        im = im.crop((0, 120, 1200, 750))
        im.save(img_curve, quality=100, subsampling=0)
    except Exception as e61:
        debug(e61)
        return
    debug('Vix_curve complete' + '\n')


def vix_cont(img_out_path_=IMAGES_OUT_PATH):
    vx1 = quandl.get("CHRIS/CBOE_VX1.4", authtoken="gWq5SV_V-yFkXVMgrwwy", rows=1)
    vx2 = quandl.get("CHRIS/CBOE_VX2.4", authtoken="gWq5SV_V-yFkXVMgrwwy", rows=1)
    vx1_c = vx1['Close'].to_list()
    vx1_c = str(vx1_c).strip('[]')
    vx2_c = vx2['Close'].to_list()
    vx2_c = str(vx2_c).strip('[]')
    diff = float(vx2_c) - float(vx1_c)
    if diff > 0:
        vix = 'Contango'
    else:
        vix = 'Backwordation'
    with open(img_out_path_ + 'vix_cont.csv', 'w+') as f:
        f.write(f'{vix}')
    debug('vix_cont complete')


def users_count():
    with open(os.path.join('results', 'users.csv'), 'r') as f0:
        for x in f0:
            x = x.split()
    users = int(x[0]) + norm.ppf(random.uniform(0, 1), loc=2, scale=2)

    with open(os.path.join('results', 'users.csv'), 'w+') as f:
        write = f.write(f'{int(users)}')
    debug(int(users))

# ============================== GET RANKING DATA ================================
# def get_ranking_data(tick, ag=agents()):
#     ticker = tick.upper()
#     if ticker is None or len(ticker) == 0:
#         return {"rank": None, "data": None}
#
#     from yahooquery import Ticker
#     aapl = Ticker('aapl')
#     all_financial = aapl.all_financial_data('q')
#     summary = aapl.summary_detail
#
#     headers = {'User-Agent': ag}
#     url = f"https://finance.yahoo.com/quote/{ticker}/analysis?p={ticker}"
#     try:
#         yahoo_analysis = requests.get(url).text
#         soup = BeautifulSoup(yahoo_analysis, "html.parser")
#     except Exception as e:
#         debug(e, "ERROR")
#         return {"rank": None, "data": None}
#
#     # Earnings Estimate
#     eet = soup.find("table", attrs={"class": "W(100%) M(0) BdB Bdc($seperatorColor) Mb(25px)", "data-reactid": "5"})
#     curr_avg_estimate = eet.find("span", attrs={"data-reactid": "46"}).text
#     curr_avg_estimate = fast_float(curr_avg_estimate, default=None)
#
#     next_qtr_avg_estimate = eet.find("span", attrs={"data-reactid": "48"}).text
#     next_qtr_avg_estimate = fast_float(next_qtr_avg_estimate, default=None)
#
#     # Revenue Estimate
#     ret = soup.find("table", attrs={"class": "W(100%) M(0) BdB Bdc($seperatorColor) Mb(25px)", "data-reactid": "86"})
#     revenue_estimate_current_year = ret.find("span", attrs={"data-reactid": "175"}).text
#     revenue_estimate_current_year = fast_float(revenue_estimate_current_year[: -1], default=None)
#
#     revenue_estimate_next_year = ret.find("span", attrs={"data-reactid": "177"}).text
#     revenue_estimate_next_year = fast_float(revenue_estimate_next_year[: -1], default=None)
#
#     # Earnings History
#     eht = soup.find("table", attrs={"class": "W(100%) M(0) BdB Bdc($seperatorColor) Mb(25px)", "data-reactid": "178"})
#     date1 = eht.find("span", attrs={"data-reactid": "184"}).text
#     date2 = eht.find("span", attrs={"data-reactid": "186"}).text
#     date3 = eht.find("span", attrs={"data-reactid": "188"}).text
#     date4 = eht.find("span", attrs={"data-reactid": "190"}).text
#     value1 = fast_float(eht.find("span", attrs={"data-reactid": "207"}).text, default=None)
#     value2 = fast_float(eht.find("span", attrs={"data-reactid": "209"}).text, default=None)
#     value3 = fast_float(eht.find("span", attrs={"data-reactid": "211"}).text, default=None)
#     value4 = fast_float(eht.find("span", attrs={"data-reactid": "213"}).text, default=None)
#     earning_history_eps_actual = {}
#     earning_history_eps_actual_yearago = None
#     earning_history_eps_actual_nqyearago = None
#     if date1 != "Invalid Date":
#         earning_history_eps_actual_yearago = value1
#         earning_history_eps_actual[datetime.datetime.strptime(date1, "%m/%d/%Y").date()] = value1
#     if date2 != "Invalid Date":
#         earning_history_eps_actual_nqyearago = value2
#         earning_history_eps_actual[datetime.datetime.strptime(date2, "%m/%d/%Y").date()] = value2
#     if date3 != "Invalid Date":
#         earning_history_eps_actual[datetime.datetime.strptime(date3, "%m/%d/%Y").date()] = value3
#     if date4 != "Invalid Date":
#         earning_history_eps_actual[datetime.datetime.strptime(date4, "%m/%d/%Y").date()] = value4
#
#     debug(f"### {ticker} ###")
#     debug(f"curr_avg_estimate={curr_avg_estimate}")
#     debug(f"next_qtr_avg_estimate={next_qtr_avg_estimate}")
#     debug(f"revenue_estimate_current_year={revenue_estimate_current_year}")
#     debug(f"revenue_estimate_next_year={revenue_estimate_next_year}")
#     debug(f"earning_history_eps_actual={earning_history_eps_actual}\n")
#
#     next_earning_date = None
#     url1 = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}"
#     try:
#         yahoo_quotes = requests.get(url1).text
#         soup = BeautifulSoup(yahoo_quotes, "html.parser")
#         next_earning_date = soup.find("td", attrs={"class": "Ta(end) Fw(600) Lh(14px)",
#                                                    "data-reactid": "104",
#                                                    "data-test": "EARNINGS_DATE-value"}).text
#     except Exception as e:
#         debug(e, "ERROR")
#         pass
#
#     debug(f"next_earning_date={next_earning_date}\n")
#
#     debug(" >>> Reuters Data <<< ")
#     reuters = Reuters()
#     postfix_list = ['.Z', '.O', '.N', '.A']
#     ticker_list = []
#     df1 = None
#     found_postfix = ""
#     for postfix in postfix_list:
#         ticker_list = [ticker + postfix]
#         try:
#             debug(f'Try get {ticker + postfix}')
#             df1 = reuters.get_income_statement(ticker_list, yearly=False)
#         except Exception as e:
#             debug(e, "ERROR")
#         if df1.size > 0:
#             found_postfix = postfix
#             break
#         sleep(2)
#
#     if df1 is None or df1.size == 0:
#         debug(f"df1 is None or df1.size == 0", WARNING)
#         return {"rank": None, "data": None}
#
#     debug(f'%%% 1. Find ticker on: {ticker_list} %%%', WARNING)
#     # Total Revenue
#     tr = df1.loc[df1['metric'] == 'Total Revenue', ['year', 'metric', 'value', 'quarter']]
#     total_revenue_curr = None
#     total_revenue_yearago = None
#     if len(tr.values) == 5:
#         total_revenue_curr = fast_float(tr.values[0][2], default=None)
#         total_revenue_yearago = fast_float(tr.values[4][2], default=None)
#     debug(f'Total revenue last: {total_revenue_curr}')
#     debug(f'Total revenue first: {total_revenue_yearago}')
#
#     # Diluted Normalized EPS
#     dneps = df1.loc[df1['metric'] == 'Diluted Normalized EPS', ['year', 'metric', 'value', 'quarter']]
#     diluted_normalized_eps_curr = None
#     diluted_normalized_eps_yearago = None
#     if len(dneps.values) == 5:
#         diluted_normalized_eps_curr = fast_float(dneps.values[0][2], default=None)
#         diluted_normalized_eps_yearago = fast_float(dneps.values[-1][2], default=None)
#     debug(f'Diluted Normalized EPS Last: {diluted_normalized_eps_curr}')
#     debug(f'Diluted Normalized EPS First: {diluted_normalized_eps_yearago}')
#
#     # df2 = reuters.get_balance_sheet(ticker_list, yearly=False)
#     # df3 = reuters.get_cash_flow(ticker_list, yearly=False)
#     df4 = None
#     try:
#         debug(f'Try get {ticker_list}')
#         df4 = reuters.get_key_metrics(ticker_list)
#     except Exception as e:
#         debug(e, "ERROR")
#     for postfix in postfix_list:
#         if postfix == found_postfix:
#             continue
#         sleep(2)
#         ticker_list = [ticker + postfix]
#         try:
#             debug(f'Try get {ticker + postfix}')
#             df4 = reuters.get_key_metrics(ticker_list)
#         except Exception as e:
#             debug(e, "ERROR")
#         if df4.size > 0:
#             found_postfix = postfix
#             break
#
#     if df4 is None or df4.size == 0:
#         debug(f"df1 is None or df1.size == 0", WARNING)
#         return {"rank": None, "data": None}
#
#     debug(f'%%% 2. Find ticker on: {ticker_list} %%%', WARNING)
#
#     # Market Capitalization
#     mkt_cap = df4.loc[df4['metric'] == 'Market Capitalization', ['value']].value.values[0]
#     mkt_cap = mkt_cap.replace(',', '')
#     if mkt_cap[-1] in ['B', 'M', 'b', 'm']:
#         mkt_cap = fast_float(mkt_cap[: -1], default=None)
#     else:
#         mkt_cap = fast_float(mkt_cap, default=None)
#
#     debug(f'Market Capitalization: {mkt_cap}')
#
#     # Beta
#     beta = df4.loc[df4['metric'] == 'Beta', ['value']].value.values[0]
#     beta = fast_float(beta, default=None)
#     debug(f'Beta: {beta}')
#
#     # Revenue per Share (Annual)
#     # revenue_per_share_annual = df4.loc[df4['metric'] == 'Revenue per Share (Annual)', ['value']].value.values[0]
#     # debug(f'Revenue Per Share (Annual): {revenue_per_share_annual}')
#
#     # Dividend (Per Share Annual)
#     divident_per_share_annual = df4.loc[df4['metric'] == 'Dividend (Per Share Annual)', ['value']].value.values[0]
#     divident_per_share_annual = fast_float(divident_per_share_annual, default=None)
#     debug(f'Dividend (Per Share Annual): {divident_per_share_annual}')
#
#     # Current Ratio (Quarterly)
#     current_ratio_quarterly = df4.loc[df4['metric'] == 'Current Ratio (Quarterly)', ['value']].value.values[0]
#     current_ratio_quarterly = fast_float(current_ratio_quarterly, default=None)
#     debug(f'Current Ratio (Quarterly): {current_ratio_quarterly}')
#
#     # Long Term Debt/Equity (Quarterly)
#     long_term_debt_equity_quarterly = \
#         df4.loc[df4['metric'] == 'Long Term Debt/Equity (Quarterly)', ['value']].value.values[0]
#     long_term_debt_equity_quarterly = fast_float(long_term_debt_equity_quarterly, default=None)
#     debug(f'Long Term Debt/Equity (Quarterly): {long_term_debt_equity_quarterly}')
#
#     # Net Profit Margin % (Annual)
#     net_profit_margin_percent_annual = df4.loc[df4['metric'] == 'Net Profit Margin % (Annual)', ['value']].value.values[
#         0]
#     net_profit_margin_percent_annual = fast_float(net_profit_margin_percent_annual, default=None)
#     debug(f'Net Profit Margin % (Annual): {net_profit_margin_percent_annual}')
#
#     revenue_estimate_current_year_r = None
#     if revenue_estimate_current_year is not None:
#         if revenue_estimate_current_year > 5:
#             revenue_estimate_current_year_r = 2
#         elif 0 <= revenue_estimate_current_year <= 5:
#             revenue_estimate_current_year_r = 1
#         elif revenue_estimate_current_year < 0:
#             revenue_estimate_current_year_r = -1
#
#     revenue_estimate_next_year_r = None
#     if revenue_estimate_next_year is not None:
#         revenue_estimate_next_year_r = 1 if revenue_estimate_next_year > 0 else -1
#
#     curr_avg_estimate_r = None
#     if earning_history_eps_actual_yearago is not None and curr_avg_estimate is not None:
#         curr_avg_estimate_r = 2 if curr_avg_estimate > earning_history_eps_actual_yearago else -2
#
#     next_qtr_avg_estimate_r = None
#     if earning_history_eps_actual_nqyearago is not None and next_qtr_avg_estimate is not None:
#         next_qtr_avg_estimate_r = 2 if next_qtr_avg_estimate > earning_history_eps_actual_nqyearago else -2
#
#     total_revenue_r = None
#     if total_revenue_curr is not None and total_revenue_yearago is not None:
#         total_revenue_r = 1 if total_revenue_curr > total_revenue_yearago else -1
#
#     diluted_normalized_eps_r = None
#     if diluted_normalized_eps_yearago is not None and diluted_normalized_eps_curr is not None:
#         diluted_normalized_eps_r = 1 if diluted_normalized_eps_curr > diluted_normalized_eps_yearago else -1
#
#     net_profit_margin_percent_annual_r = None
#     if net_profit_margin_percent_annual is not None:
#         if net_profit_margin_percent_annual > 2:
#             net_profit_margin_percent_annual_r = 2
#         elif 0 <= net_profit_margin_percent_annual <= 2:
#             net_profit_margin_percent_annual_r = 1
#         elif 0 > net_profit_margin_percent_annual >= -5:
#             net_profit_margin_percent_annual_r = -1
#         elif net_profit_margin_percent_annual < -5:
#             net_profit_margin_percent_annual_r = -2
#
#     divident_per_share_annual_r = None
#     if divident_per_share_annual is not None:
#         divident_per_share_annual_r = 2 if divident_per_share_annual > 0 else -2
#     else:
#         divident_per_share_annual_r = -2
#
#     mkt_cap_r = None
#     if mkt_cap is not None:
#         if mkt_cap > 200000:
#             mkt_cap_r = 2
#         elif 50000 < mkt_cap <= 200000:
#             mkt_cap_r = 1
#         elif 10000 < mkt_cap <= 50000:
#             mkt_cap_r = 0
#         elif 2000 < mkt_cap <= 10000:
#             mkt_cap_r = -1
#         elif 2000 < mkt_cap:
#             mkt_cap_r = -2
#
#     beta_r = None
#     if beta is not None:
#         beta_r = 1 if 0.75 <= beta <= 1.5 else -1
#
#     current_ratio_quarterly_r = None
#     if current_ratio_quarterly is not None:
#         current_ratio_quarterly_r = 2 if current_ratio_quarterly > 1 else -2
#
#     long_term_debt_equity_quarterly_r = None
#     if long_term_debt_equity_quarterly is not None:
#         if long_term_debt_equity_quarterly > 30:
#             long_term_debt_equity_quarterly_r = -2
#         elif 20 <= long_term_debt_equity_quarterly <= 30:
#             long_term_debt_equity_quarterly_r = -1
#         elif long_term_debt_equity_quarterly < 20:
#             long_term_debt_equity_quarterly_r = 1
#     else:
#         long_term_debt_equity_quarterly_r = -5
#
#     debug("-------------- R A N K I N G --------------")
#     debug(f'\n'
#           f'revenue_estimate: {revenue_estimate_current_year_r}\n'
#           f'revenue_estimate_next_year: {revenue_estimate_next_year_r}\n'
#           f'curr_avg_estimate: {curr_avg_estimate_r}\n'
#           f'next_qtr_avg_estimate: {next_qtr_avg_estimate_r}\n'
#           f'total_revenue: {total_revenue_r}\n'
#           f'diluted_normalized_eps: {diluted_normalized_eps_r}\n'
#           f'net_profit_margin_percent_annual: {net_profit_margin_percent_annual_r}\n'
#           f'divident_per_share_annual: {divident_per_share_annual_r}\n'
#           f'mkt_cap: {mkt_cap_r}\n'
#           f'beta: {beta_r}\n'
#           f'current_ratio_quarterly: {current_ratio_quarterly_r}\n'
#           f'long_term_debt_equity_quarterly: {long_term_debt_equity_quarterly_r}\n')
#
#     finaly_rank = 0
#     if revenue_estimate_current_year_r is not None:
#         finaly_rank = finaly_rank + revenue_estimate_current_year_r
#     if revenue_estimate_next_year_r is not None:
#         finaly_rank = finaly_rank + revenue_estimate_next_year_r
#     if curr_avg_estimate_r is not None:
#         finaly_rank = finaly_rank + curr_avg_estimate_r
#     if next_qtr_avg_estimate_r is not None:
#         finaly_rank = finaly_rank + next_qtr_avg_estimate_r
#     if total_revenue_r is not None:
#         finaly_rank = finaly_rank + total_revenue_r
#     if diluted_normalized_eps_r is not None:
#         finaly_rank = finaly_rank + diluted_normalized_eps_r
#     if net_profit_margin_percent_annual_r is not None:
#         finaly_rank = finaly_rank + net_profit_margin_percent_annual_r
#     if divident_per_share_annual_r is not None:
#         finaly_rank = finaly_rank + divident_per_share_annual_r
#     if mkt_cap_r is not None:
#         finaly_rank = finaly_rank + mkt_cap_r
#     if beta_r is not None:
#         finaly_rank = finaly_rank + beta_r
#     if current_ratio_quarterly_r is not None:
#         finaly_rank = finaly_rank + current_ratio_quarterly_r
#     if long_term_debt_equity_quarterly_r is not None:
#         finaly_rank = finaly_rank + long_term_debt_equity_quarterly_r
#
#     debug(f"Finaly Rank: {finaly_rank}\n", WARNING)
#
#     res = {"rank": finaly_rank,
#            "revenue_estimate": revenue_estimate_current_year_r,
#            "revenue_estimate_next_year": revenue_estimate_next_year_r,
#            "curr_avg_estimate": curr_avg_estimate_r,
#            "next_qtr_avg_estimate": next_qtr_avg_estimate_r,
#            "total_revenue": total_revenue_r,
#            "diluted_normalized_eps": diluted_normalized_eps_r,
#            "net_profit_margin_percent_annual": net_profit_margin_percent_annual_r,
#            "divident_per_share_annual": divident_per_share_annual_r,
#            "mkt_cap": mkt_cap_r,
#            "beta": beta_r,
#            "current_ratio_quarterly": current_ratio_quarterly_r,
#            "long_term_debt_equity_quarterly_r": long_term_debt_equity_quarterly_r,
#            "next_earning_date": next_earning_date}
#
#     debug(f"RESULT DICT: {res} ")
#     debug('%%% get_ranking_data complete')
#     return res
#
#     # revenue_estimate_current_year > 5 % +2 / 0 - 5 % +1 < 0 % -1
#     # revenue_estimate_next_year  positive + 1 / negative - 1
#     #
#     # curr_avg_estimate > earning_history_eps_actual года назад + 2 else -2
#     # next_qtr_avg_estimate > earning_history_eps_actual года назад + 2 else -2
#     #
#     # Total Revenue > квартала год назад + 1 else -1
#     # Diluted Normalized EPS > квартала год назад + 1 else -1
#     # Net Profit Margin % (Annual) > 2 + 2 / 0 - 2 + 1 / < 0 - 5 - 1 / < -5 - 2
#     #
#     # Dividend(Per Share Annual) positive + 2 / negative - 2
#     #
#     # Market Capitalization > 200bln + 2 / 50 - 200bln + 1 / 2 - 10 + 0 / < 2bln - 2
#     # Beta 0.75 - 1.5 + 1 else -1
#     # Current Ratio(Quarterly) > 1 + 2 / < 1 - 2
#     # Long Term Debt / Equity(Quarterly) > 3 - 2 / 2 - 3 - 1 / < 2 + 1
#     #
#     # Rank = sum of all values
#     # return dict{rank: ..., next_report_date: ..., revenue_estimate_current_year: 2, ....}
# ============================== GET RANKING DATA II ================================
# def get_ranking_data2(tick, ag=agents()):
#     ticker = tick.upper()
#     err_info_result = {}
#     err_rank_result = {"rank": None, "data": None}
#     if ticker is None or len(ticker) == 0:
#         debug(f'Ticker is none, or len = 0 -- [{ticker}]')
#         return err_info_result, err_rank_result
#
#     ticker_data = None
#     try:
#         ticker_data = Ticker(ticker)
#     except Exception as e:
#         debug(e, ERROR)
#         debug(f"Can't get ticker data -- [{ticker}]")
#         return err_info_result, err_rank_result
#
#     quoteType = None
#     if ticker_data.quotes == 'No data found':
#         debug(f"No data found -- [{ticker}]")
#         return err_info_result, err_rank_result
#     else:
#         quoteType = ticker_data.quotes[ticker].get('quoteType', None)
#         fullExchangeName = ticker_data.quotes[ticker].get('fullExchangeName')
#         if (quoteType is None or
#                 quoteType == 'MUTUALFUND' or
#                 quoteType == 'ECNQUOTE' or
#                 quoteType == 'ETF' or
#                 (quoteType == 'EQUITY' and fullExchangeName == 'Other OTC')):
#             debug(f"quoteType == {quoteType} -- [{ticker}]")
#             return err_info_result, err_rank_result
#
#     all_financial_data_q = ticker_data.all_financial_data('q')
#     # all_financial_data_a = ticker_data.all_financial_data('a')
#
#     # % % % % % % % % % % % % % % % % % % %
#     # Description  Block
#     # % % % % % % % % % % % % % % % % % % %
#
#     longName = ticker_data.price[ticker].get('longName', '')
#     sector = ticker_data.asset_profile[ticker].get('sector', '')
#     industry = ticker_data.asset_profile[ticker].get('industry', '')
#     country = ticker_data.asset_profile[ticker].get('country', '')
#     regularMarketPrice = ticker_data.price[ticker].get('regularMarketPrice', None)
#     marketState = ticker_data.price[ticker].get('marketState', '')
#     marketCap = ticker_data.price[ticker].get('marketCap', None)
#     beta = ticker_data.summary_detail[ticker].get('beta', None)
#     volume = ticker_data.summary_detail[ticker].get('volume', None)
#     averageVolume = ticker_data.summary_detail[ticker].get('averageVolume', None)
#     trailingPE = ticker_data.summary_detail[ticker].get('trailingPE', None)
#     forwardPE = ticker_data.summary_detail[ticker].get('forwardPE', None)
#     ce_exDividendDate = ticker_data.calendar_events[ticker].get('exDividendDate', None)
#     ce_dividendDate = ticker_data.calendar_events[ticker].get('dividendDate', None)
#     ce_earnings_earnings = ticker_data.calendar_events[ticker].get('earnings', None)
#     ce_earnings_earningsDate = ''
#     if ce_earnings_earnings is not None:
#         ce_earnings_earningsDate = ce_earnings_earnings.get('earningsDate', '')
#
#     # % % % % % % % % % % % % % %
#     # Estimetes  Block
#     # % % % % % % % % % % % % % % %
#     et_0y_revenueEstimate_growth = None
#     et_p1y_revenueEstimate_growth = None
#     et_earningsEstimate_avg = None
#     et_p1q_earningsEstimate_avg = None
#     earnings_trend_data = ticker_data.earnings_trend[ticker]
#     if not isinstance(earnings_trend_data, str):
#         earnings_trend_ticker_trend = earnings_trend_data.get('trend', None)
#         if len(earnings_trend_ticker_trend) >= 3:
#             et_0y_revenueEstimate_growth = earnings_trend_ticker_trend[2]['revenueEstimate']['growth']
#             if isinstance(et_0y_revenueEstimate_growth, dict):
#                 et_0y_revenueEstimate_growth = None
#
#         if len(earnings_trend_ticker_trend) >= 4:
#             et_p1y_revenueEstimate_growth = earnings_trend_ticker_trend[3]['revenueEstimate']['growth']
#             if isinstance(et_p1y_revenueEstimate_growth, dict):
#                 et_p1y_revenueEstimate_growth = None
#
#         if len(earnings_trend_ticker_trend) >= 1:
#             et_earningsEstimate_avg = earnings_trend_ticker_trend[0]['earningsEstimate']['avg']
#             if isinstance(et_earningsEstimate_avg, dict):
#                 et_earningsEstimate_avg = None
#
#         if len(earnings_trend_ticker_trend) >= 2:
#             et_p1q_earningsEstimate_avg = earnings_trend_ticker_trend[1]['earningsEstimate']['avg']
#             if isinstance(et_p1q_earningsEstimate_avg, dict):
#                 et_p1q_earningsEstimate_avg = None
#
#     e_earningsChart_quarterly = None
#     earning_chart_data = ticker_data.earnings[ticker]
#     if not isinstance(earning_chart_data, str):
#         e_earningsChart = earning_chart_data.get('earningsChart', None)
#         if e_earningsChart is not None:
#             e_earningsChart_quarterly = e_earningsChart.get('quarterly', None)
#
#     # % % % % % % % % % % % % %
#     # Current  Block
#     # % % % % % % % % % % % % %
#
#     total_revenue_last = None
#     total_revenue_yearago = None
#     total_revenue = all_financial_data_q.get('TotalRevenue', None)
#     if total_revenue is not None:
#         total_revenue_values = total_revenue.values
#         for i in reversed(total_revenue):
#             total_revenue_last = fast_float(i, default=None)
#             if not pd.isna(total_revenue_last):
#                 break
#         total_revenue_yearago = fast_float(all_financial_data_q.TotalRevenue.values[1], default=None)
#
#     diluted_eps_last = None
#     diluted_eps_yearago = None
#     diluted_eps = all_financial_data_q.get('DilutedEPS', None)
#     if diluted_eps is not None:
#         for i in reversed(diluted_eps):
#             diluted_eps_last = fast_float(i, default=None)
#             if not pd.isna(diluted_eps_last):
#                 break
#         diluted_eps_yearago = fast_float(all_financial_data_q.DilutedEPS.values[1], default=None)
#
#     ebit = None
#     ebit_data = all_financial_data_q.get('EBIT', None)
#     if ebit_data is not None:
#         for i in reversed(ebit_data):
#             ebit = fast_float(i, default=None)
#             if not pd.isna(ebit):
#                 break
#
#     interestExpense = None
#     interestExpense_data = all_financial_data_q.get('InterestExpense', None)
#     if interestExpense_data is not None:
#         for i in reversed(interestExpense_data):
#             interestExpense = fast_float(i, default=None)
#             if not pd.isna(interestExpense):
#                 break
#
#     profitMargins = ticker_data.financial_data[ticker].get('profitMargins', None)
#     trailingAnnualDividendRate = ticker_data.summary_detail[ticker].get('trailingAnnualDividendRate', None)
#     trailingAnnualDividendYield = ticker_data.summary_detail[ticker].get('trailingAnnualDividendYield', None)
#
#     repurchase_of_capital_stock = all_financial_data_q.get('RepurchaseOfCapitalStock', None)
#     repurchase_of_capital_stock_avg = repurchase_of_capital_stock.mean(
#         0) if repurchase_of_capital_stock is not None else None
#
#     currentRatio = ticker_data.financial_data[ticker].get('currentRatio', None)
#     debtToEquity = ticker_data.financial_data[ticker].get('debtToEquity', None)
#
#     # % % % % % % % % % % % % % % % %
#     # RANK   BLOCK
#     # % % % % % % % % % % % % % % %
#     et_0y_revenueEstimate_growth_r = None
#     if et_0y_revenueEstimate_growth is not None:
#         if et_0y_revenueEstimate_growth > 0.05:
#             et_0y_revenueEstimate_growth_r = 4
#         elif 0.05 >= et_0y_revenueEstimate_growth > 0.0:
#             et_0y_revenueEstimate_growth_r = 3
#         elif et_0y_revenueEstimate_growth < 0.0:
#             et_0y_revenueEstimate_growth_r = -2
#
#     et_p1y_revenueEstimate_growth_r = None
#     if et_p1y_revenueEstimate_growth is not None:
#         if et_p1y_revenueEstimate_growth > 0:
#             et_p1y_revenueEstimate_growth_r = 2
#         else:
#             et_p1y_revenueEstimate_growth_r = -2
#
#     et_earningsEstimate_r = None
#     if et_earningsEstimate_avg is not None and e_earningsChart_quarterly is not None and len(
#             e_earningsChart_quarterly) >= 2:
#         old_earning = e_earningsChart_quarterly[1]['actual']
#         if et_earningsEstimate_avg > old_earning:
#             et_earningsEstimate_r = 2
#         else:
#             et_earningsEstimate_r = -2
#     else:  # если старый None а новый есть то +2, старый есть а текущего нет, то none!!!!!!!!!!!!!!!!!!!!!
#         if et_earningsEstimate_avg is not None and e_earningsChart_quarterly is None:
#             et_earningsEstimate_r = 2
#         else:
#             et_earningsEstimate_r = None
#
#     et_p1q_earningsEstimate_r = None
#     if et_p1q_earningsEstimate_avg is not None and e_earningsChart_quarterly is not None and len(
#             e_earningsChart_quarterly) >= 3:
#         if et_p1q_earningsEstimate_avg > e_earningsChart_quarterly[2]['actual']:
#             et_p1q_earningsEstimate_r = 3
#         else:
#             et_p1q_earningsEstimate_r = -3
#     else:  # если старый None а новый есть то +2, старый есть а текущего нет, то none!!!!!!!!!!!!!!!!!!!!!
#         if et_p1q_earningsEstimate_avg is not None and e_earningsChart_quarterly is None:
#             et_p1q_earningsEstimate_r = 3
#         else:
#             et_p1q_earningsEstimate_r = None
#
#     total_revenue_r = None
#     if total_revenue_last is not None and total_revenue_yearago is not None:
#         if total_revenue_last > total_revenue_yearago:
#             total_revenue_r = 2
#         else:
#             total_revenue_r = -2
#
#     diluted_eps_r = None
#     if diluted_eps_last is not None and diluted_eps_yearago is not None:
#         if diluted_eps_last > diluted_eps_yearago:
#             diluted_eps_r = 1
#         else:
#             diluted_eps_r = -1
#
#     profitMargins_r = None
#     if profitMargins is not None:
#         if profitMargins > 0.5:
#             profitMargins_r = 3
#         elif 0.25 < profitMargins <= 0.5:
#             profitMargins_r = 2
#         elif 0.05 < profitMargins <= 0.25:
#             profitMargins_r = 1
#         elif -0.05 < profitMargins <= 0.05:
#             profitMargins_r = 0
#         elif profitMargins <= -0.05:
#             profitMargins_r = -3
#
#     trailingAnnualDividendYield_r = None
#     if trailingAnnualDividendYield is not None:
#         if trailingAnnualDividendYield > 0:
#             trailingAnnualDividendYield_r = 1
#         else:
#             trailingAnnualDividendYield_r = -1
#     else:
#         trailingAnnualDividendYield_r = -1
#
#     repurchase_of_capital_stock_avg_r = None
#     if repurchase_of_capital_stock_avg is not None:
#         if repurchase_of_capital_stock_avg < 0:
#             repurchase_of_capital_stock_avg_r = 2
#         else:
#             repurchase_of_capital_stock_avg_r = -2
#     else:
#         repurchase_of_capital_stock_avg_r = -2
#
#     marketCap_r = None
#     if marketCap is not None:
#         if marketCap > 200000000000:
#             marketCap_r = 2
#         elif 200000000000 >= marketCap > 50000000000:
#             marketCap_r = 1
#         elif 50000000000 >= marketCap > 10000000000:
#             marketCap_r = 0
#         elif 10000000000 >= marketCap >= 2000000000:
#             marketCap_r = -1
#         elif marketCap < 2000000000:
#             marketCap_r = -2
#
#     beta_r = None
#     if beta is not None:
#         if 0.75 <= beta <= 1.5:
#             beta_r = 1
#         else:
#             beta_r = -1
#
#     currentRatio_r = None
#     if currentRatio is not None:
#         if currentRatio > 1:
#             currentRatio_r = 2
#         else:
#             currentRatio_r = -2
#
#     debtToEquity_r = None
#     if debtToEquity is not None and not pd.isna(debtToEquity):
#         if debtToEquity > 300:
#             debtToEquity_r = -2
#         elif 200 <= debtToEquity <= 300:
#             debtToEquity_r = -1
#         elif debtToEquity < 200:
#             debtToEquity_r = 1
#         elif debtToEquity < 100:
#             debtToEquity_r = 2
#     else:
#         debtToEquity_r = -4
#
#     interest_coverage_r = None
#     if ebit is None and interestExpense is None:
#         interest_coverage_r = None
#     if ebit is None and interestExpense is not None and interestExpense < 0:
#         interest_coverage_r = -5
#     if ebit is not None and interestExpense is not None and interestExpense == 0:
#         interest_coverage_r = 2
#     if ebit is not None and ebit > 0 and interestExpense is not None and interestExpense > 0:
#         interest_coverage = ebit / abs(interestExpense)
#         if interest_coverage > 21:
#             interest_coverage_r = 2
#         if 6 < interest_coverage <= 21:
#             interest_coverage_r = 1
#         if 1 < interest_coverage <= 6:
#             interest_coverage_r = -1
#         if interest_coverage < 1:
#             interest_coverage_r = -2
#
#     rank = 0
#     if et_0y_revenueEstimate_growth_r is not None:
#         rank += et_0y_revenueEstimate_growth_r
#     if et_p1y_revenueEstimate_growth_r is not None:
#         rank += et_p1y_revenueEstimate_growth_r
#     if et_earningsEstimate_r is not None:
#         rank += et_earningsEstimate_r
#     if et_p1q_earningsEstimate_r is not None:
#         rank += et_p1q_earningsEstimate_r
#     if total_revenue_r is not None:
#         rank += total_revenue_r
#     if diluted_eps_r is not None:
#         rank += diluted_eps_r
#     if profitMargins_r is not None:
#         rank += profitMargins_r
#     if trailingAnnualDividendYield_r is not None:
#         rank += trailingAnnualDividendYield_r
#     if repurchase_of_capital_stock_avg_r is not None:
#         rank += repurchase_of_capital_stock_avg_r
#     if marketCap_r is not None:
#         rank += marketCap_r
#     if beta_r is not None:
#         rank += beta_r
#     if currentRatio_r is not None:
#         rank += currentRatio_r
#     if debtToEquity_r is not None:
#         rank += debtToEquity_r
#     if interest_coverage_r is not None:
#         rank += interest_coverage_r
#
#     debug("-------------- I N F O --------------")
#     debug(f'Ticker: ### {ticker} ###\n')
#     # debug(f'\n'
#     #       f'Ticker: ### {ticker} ###\n'
#     #       f'quoteType: {quoteType}\n'
#     #       f'longName: {longName}\n'
#     #       f'sector: {sector}\n'
#     #       f'industry: {industry}\n'
#     #       f'country: {country}\n'
#     #       f'regularMarketPrice: {regularMarketPrice}\n'
#     #       f'marketState: {marketState}\n'
#     #       f'marketCap: {marketCap}\n'
#     #       f'beta: {beta}\n'
#     #       f'volume: {volume}\n'
#     #       f'averageVolume: {averageVolume}\n'
#     #       f'trailingPE: {trailingPE}\n'
#     #       f'forwardPE: {forwardPE}\n'
#     #       f'exDividendDate: {ce_exDividendDate}\n'
#     #       f'dividendDate: {ce_dividendDate}\n'
#     #       f'earnings_earningsDate: {ce_earnings_earningsDate}\n'
#     #       )
#     # debug("-------------- R A N K I N G --------------")
#     # debug(f'\n'
#     #       f'et_0y_revenueEstimate_growth: {et_0y_revenueEstimate_growth_r}\n'
#     #       f'et_p1y_revenueEstimate: {et_p1y_revenueEstimate_growth_r}\n'
#     #       f'et_earningsEstimate: {et_earningsEstimate_r}\n'
#     #       f'et_p1q_earningsEstimate: {et_p1q_earningsEstimate_r}\n'
#     #       f'total_revenue: {total_revenue_r}\n'
#     #       f'diluted_eps: {diluted_eps_r}\n'
#     #       f'profitMargins: {profitMargins_r}\n'
#     #       f'trailingAnnualDividendYield: {trailingAnnualDividendYield_r}\n'
#     #       f'repurchase_of_capital_stock_avg: {repurchase_of_capital_stock_avg_r}\n'
#     #       f'marketCap: {marketCap_r}\n'
#     #       f'beta: {beta_r}\n'
#     #       f'currentRatio: {currentRatio_r}\n'
#     #       f'debtToEquity: {debtToEquity_r}\n'
#     #       f'interest_coverage: {interest_coverage_r}\n')
#
#     debug(f"Finaly Rank : {rank}\n", WARNING)
#
#     rank_result = {"rank": rank,
#                    "et_0y_revenueEstimate_growth": et_0y_revenueEstimate_growth_r,
#                    "et_p1y_revenueEstimate": et_p1y_revenueEstimate_growth_r,
#                    "et_earningsEstimate": et_earningsEstimate_r,
#                    "et_p1q_earningsEstimate": et_p1q_earningsEstimate_r,
#                    "total_revenue": total_revenue_r,
#                    "diluted_eps": diluted_eps_r,
#                    "profitMargins": profitMargins_r,
#                    "trailingAnnualDividendYield": trailingAnnualDividendYield_r,
#                    "repurchase_of_capital_stock_avg": repurchase_of_capital_stock_avg_r,
#                    "marketCap": marketCap_r,
#                    "beta": beta_r,
#                    "currentRatio": currentRatio_r,
#                    "debtToEquity": debtToEquity_r,
#                    "interest_coverage": interest_coverage_r}
#
#     info_result = {'ticker': ticker,
#                    'quoteType': quoteType,
#                    'longName': longName,
#                    'sector': sector,
#                    'industry': industry,
#                    'country': country,
#                    'regularMarketPrice': regularMarketPrice,
#                    'marketState': marketState,
#                    'marketCap': marketCap,
#                    'beta': beta,
#                    'volume': volume,
#                    'averageVolume': averageVolume,
#                    'trailingPE': trailingPE,
#                    'forwardPE': forwardPE,
#                    'exDividendDate': ce_exDividendDate,
#                    'dividendDate': ce_dividendDate,
#                    'earnings_earningsDate': ce_earnings_earningsDate}
#
#     # debug(f"INFO DICT: {info_result} \n\n")
#     # debug(f"RESULT DICT: {rank_result} ")
#     debug('%%% get_ranking_data complete')
#     return info_result, rank_result


# ============================== GET RANKING DATA III ================================

# def get_etfdb_flows(driver=None, img_out_path_=IMAGES_OUT_PATH):
#     etfs = ['SPY', 'VTI', 'VEA', 'VWO', 'QQQ', 'VXX', 'TLT', 'SHY', 'LQD', 'VCIT']
#     with driver:
#         for etf in etfs:
#             driver.get(f'https://etfdb.com/etf/{etf}/#fund-flows')
#             img_path = os.path.join(img_out_path_, f'inflows_{etf}' + '.png')
#             # html = driver.page_source
#             # debug(html)
#             # 'fund-flow-chart-container'
#             sleep(5)
#             chart = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, ".//*[@id='fund-flows']")))
#             # chart = driver.find_element_by_xpath()
#             # chart = driver.find_element_by_class_name("col-md-12")
#             driver.execute_script("return arguments[0].scrollIntoView();", chart)
#             image = chart.screenshot_as_png
#             image_stream = io.BytesIO(image)
#             im = Image.open(image_stream)
#             im.save(img_path)
#             debug(etf)
#             img = Image.open(img_path)
#             width, height = img.size
#             cropped = img.crop((1, 130, width - 1, height - 45))
#             cropped.save(img_path, quality=100, subsampling=0)
#     # 56 pixels from the left
#     # 44 pixels from the top
#     # 320 pixels from the right
#     # 43 pixels from the bottom
#     driver.quit()
#     debug('get_etf_flows complete' + '\n')


# ============================== ADVANCE/DECLINE GET ================================
# ============================== Inflows GET ================================
# def get_flows(driver=None, img_out_path_=IMAGES_OUT_PATH):
#     etfs = ['VCIT', 'SPY', 'VTI', 'VEA', 'VWO', 'QQQ', 'VXX', 'TLT', 'SHY', 'LQD']
#     with driver:
#         driver.get('https://www.etf.com/etfanalytics/etf-fund-flows-tool')
#         sleep(10)
#         html = driver.page_source
#         debug(html)
#         try:
#             elem = driver.find_element_by_xpath(".//*[@id='edit-tickers']")
#             debug('elem 1 has been located')
#         except Exception:
#             return
#         elem.send_keys("GLD, SPY, VTI, VEA, VWO, QQQ, VXX, TLT, SHY, LQD, VCIT")
#         debug('keys has been send')
#         sleep(0.7)
#         today = date.today()
#         day7 = timedelta(days=7)
#         delta = today - day7
#         start_d = delta.strftime("%Y-%m-%d")
#         end_d = today.strftime("%Y-%m-%d")
#         elem = driver.find_element_by_xpath(".//*[@id='edit-startdate-datepicker-popup-0']")
#         elem.send_keys(start_d)
#         sleep(1)
#         elem = driver.find_element_by_xpath(".//*[@id='edit-enddate-datepicker-popup-0']")
#         elem.send_keys(end_d)
#         sleep(1)
#         try:
#             WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, ".//*[@id='edit-submitbutton']"))).click()
#             debug('Button has been clicked')
#         except Exception as e1:
#             debug('Button click error. Try to re-run the scraper', e1)
#             return
#         sleep(8)
#         try:
#             elem = driver.find_element_by_xpath(".//*[@id='fundFlowsTitles']")
#             debug('elem 2-Titles has been located')
#         except Exception as e2:
#             debug('Titles elem error. Try to re-run the scraper', e2)
#             return
#         webdriver.ActionChains(driver).move_to_element(elem).perform()
#         driver.execute_script("return arguments[0].scrollIntoView();", elem)
#         sleep(1)
#
#         for etf in etfs:
#             sleep(2)
#             debug(etf)
#             tag = ".//*[@id=\'" + f'{etf}' + "_nf']"
#             tag2 = ".//*[@id=\'container_" + f'{etf}' + "'" + "]"
#             icon = driver.find_element_by_xpath(tag)  # ".//*[@id='{etf}_nf']"
#             driver.execute_script("arguments[0].click();", icon)
#             sleep(3)
#             graph = driver.find_element_by_xpath(tag2)  # ".//*[@id='container_{etf}']"
#             # driver.execute_script("return arguments[0].scrollIntoView();", graph)
#             sleep(1)
#             image = graph.screenshot_as_png
#             image_stream = io.BytesIO(image)
#             im = Image.open(image_stream)
#             im.save(os.path.join(img_out_path_, f'inflows_{etf}.png'))
#     debug('Get Fund Flows complete' + '\n')
