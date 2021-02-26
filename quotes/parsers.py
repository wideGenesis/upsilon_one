import os
from time import sleep
from datetime import date, timedelta
from fastnumbers import *
import csv
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import io
import quandl
from scipy.stats import norm
import random
from project_shared import *
from reuterspy import Reuters


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
from quotes.parsers_env import agents


def get_etfdb_flows(driver=None, img_out_path_=IMAGES_OUT_PATH):
    etfs = ['SPY', 'VTI', 'VEA', 'VWO', 'QQQ', 'VXX', 'TLT', 'SHY', 'LQD', 'VCIT']
    with driver:
        for etf in etfs:

            driver.get(f'https://etfdb.com/etf/{etf}/#fund-flows')
            img_path = os.path.join(img_out_path_, f'inflows_{etf}' + '.png')
            # html = driver.page_source
            # debug(html)
            # 'fund-flow-chart-container'
            sleep(5)
            chart = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ".//*[@id='fund-flows']")))
            # chart = driver.find_element_by_xpath()
            # chart = driver.find_element_by_class_name("col-md-12")
            driver.execute_script("return arguments[0].scrollIntoView();", chart)
            image = chart.screenshot_as_png
            image_stream = io.BytesIO(image)
            im = Image.open(image_stream)
            im.save(img_path)
            debug(etf)
            img = Image.open(img_path)
            width, height = img.size
            cropped = img.crop((1, 130, width - 1, height - 45))
            cropped.save(img_path, quality=100, subsampling=0)
    # 56 pixels from the left
    # 44 pixels from the top
    # 320 pixels from the right
    # 43 pixels from the bottom
    driver.quit()
    debug('get_etf_flows complete' + '\n')


# ============================== ADVANCE/DECLINE GET ================================
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


# ============================== YAHOO GET RANKING DATA ================================
def get_ranking_data(ticker, ag=agents()):
    headers = {'User-Agent': ag}
    url = f"https://finance.yahoo.com/quote/{ticker}/analysis?p={ticker}"
    zzz = requests.get(url).text
    soup = BeautifulSoup(zzz, "html.parser")

    # Earnings Estimate
    eet = soup.find("table", attrs={"class": "W(100%) M(0) BdB Bdc($seperatorColor) Mb(25px)", "data-reactid": "5"})
    curr_avg_estimate = eet.find("span", attrs={"data-reactid": "46"}).text
    curr_avg_estimate = fast_float(curr_avg_estimate, default=None)

    next_qtr_avg_estimate = eet.find("span", attrs={"data-reactid": "48"}).text
    next_qtr_avg_estimate = fast_float(next_qtr_avg_estimate, default=None)

    # Revenue Estimate
    ret = soup.find("table", attrs={"class": "W(100%) M(0) BdB Bdc($seperatorColor) Mb(25px)", "data-reactid": "86"})
    revenue_estimate_current_year = ret.find("span", attrs={"data-reactid": "175"}).text
    revenue_estimate_current_year = fast_float(revenue_estimate_current_year[: -1], default=None)

    revenue_estimate_next_year = ret.find("span", attrs={"data-reactid": "177"}).text
    revenue_estimate_next_year = fast_float(revenue_estimate_next_year[: -1], default=None)

    # Earnings History
    eht = soup.find("table", attrs={"class": "W(100%) M(0) BdB Bdc($seperatorColor) Mb(25px)", "data-reactid": "178"})
    date1 = eht.find("span", attrs={"data-reactid": "184"}).text
    date2 = eht.find("span", attrs={"data-reactid": "186"}).text
    date3 = eht.find("span", attrs={"data-reactid": "188"}).text
    date4 = eht.find("span", attrs={"data-reactid": "190"}).text
    value1 = fast_float(eht.find("span", attrs={"data-reactid": "207"}).text, default=None)
    value2 = fast_float(eht.find("span", attrs={"data-reactid": "209"}).text, default=None)
    value3 = fast_float(eht.find("span", attrs={"data-reactid": "211"}).text, default=None)
    value4 = fast_float(eht.find("span", attrs={"data-reactid": "213"}).text, default=None)
    earning_history_eps_actual = {}
    earning_history_eps_actual_yearago = None
    earning_history_eps_actual_nqyearago = None
    if date1 != "Invalid Date":
        earning_history_eps_actual_yearago = value1
        earning_history_eps_actual[datetime.datetime.strptime(date1, "%m/%d/%Y").date()] = value1
    if date2 != "Invalid Date":
        earning_history_eps_actual_nqyearago = value2
        earning_history_eps_actual[datetime.datetime.strptime(date2, "%m/%d/%Y").date()] = value2
    if date3 != "Invalid Date":
        earning_history_eps_actual[datetime.datetime.strptime(date3, "%m/%d/%Y").date()] = value3
    if date4 != "Invalid Date":
        earning_history_eps_actual[datetime.datetime.strptime(date4, "%m/%d/%Y").date()] = value4

    debug(f"### {ticker} ###")
    debug(f"curr_avg_estimate={curr_avg_estimate}")
    debug(f"next_qtr_avg_estimate={next_qtr_avg_estimate}")
    debug(f"revenue_estimate_current_year={revenue_estimate_current_year}")
    debug(f"revenue_estimate_next_year={revenue_estimate_next_year}")
    debug(f"earning_history_eps_actual={earning_history_eps_actual}\n")

    url1 = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}"
    zzz1 = requests.get(url1).text
    soup = BeautifulSoup(zzz1, "html.parser")
    next_earning_date = soup.find("td", attrs={"class": "Ta(end) Fw(600) Lh(14px)",
                                               "data-reactid": "104",
                                               "data-test": "EARNINGS_DATE-value"}).text
    debug(f"next_earning_date={next_earning_date}\n")

    debug(" >>> Reuters Data <<< ")
    reuters = Reuters()
    ticker_list = [ticker + ".O"]
    df1 = reuters.get_income_statement(ticker_list, yearly=False)

    # Total Revenue
    tr = df1.loc[df1['metric'] == 'Total Revenue', ['year', 'metric', 'value', 'quarter']]
    total_revenue_curr = None
    total_revenue_yearago = None
    if len(tr.values) == 5:
        total_revenue_curr = fast_float(tr.values[0][2], default=None)
        total_revenue_yearago = fast_float(tr.values[4][2], default=None)
    debug(f'Total revenue last: {total_revenue_curr}')
    debug(f'Total revenue first: {total_revenue_yearago}')

    # Diluted Normalized EPS
    dneps = df1.loc[df1['metric'] == 'Diluted Normalized EPS', ['year', 'metric', 'value', 'quarter']]
    diluted_normalized_eps_curr = None
    diluted_normalized_eps_yearago = None
    if len(dneps.values) == 5:
        diluted_normalized_eps_curr = fast_float(dneps.values[0][2], default=None)
        diluted_normalized_eps_yearago = fast_float(dneps.values[-1][2], default=None)
    debug(f'Diluted Normalized EPS Last: {diluted_normalized_eps_curr}')
    debug(f'Diluted Normalized EPS First: {diluted_normalized_eps_yearago}')

    # df2 = reuters.get_balance_sheet(ticker_list, yearly=False)
    # df3 = reuters.get_cash_flow(ticker_list, yearly=False)
    df4 = reuters.get_key_metrics(ticker_list)
    # Market Capitalization
    mkt_cap = df4.loc[df4['metric'] == 'Market Capitalization', ['value']].value.values[0]
    mkt_cap = mkt_cap.replace(',', '')
    if mkt_cap[-1] in ['B', 'M']:
        mkt_cap = fast_float(mkt_cap[: -1], default=None)
    else:
        mkt_cap = fast_float(mkt_cap, default=None)

    debug(f'Market Capitalization: {mkt_cap}')

    # Beta
    beta = df4.loc[df4['metric'] == 'Beta', ['value']].value.values[0]
    beta = fast_float(beta, default=None)
    debug(f'Beta: {beta}')

    # Revenue per Share (Annual)
    # revenue_per_share_annual = df4.loc[df4['metric'] == 'Revenue per Share (Annual)', ['value']].value.values[0]
    # debug(f'Revenue Per Share (Annual): {revenue_per_share_annual}')

    # Dividend (Per Share Annual)
    divident_per_share_annual = df4.loc[df4['metric'] == 'Dividend (Per Share Annual)', ['value']].value.values[0]
    divident_per_share_annual =fast_float(divident_per_share_annual, default=None)
    debug(f'Dividend (Per Share Annual): {divident_per_share_annual}')

    # Current Ratio (Quarterly)
    current_ratio_quarterly = df4.loc[df4['metric'] == 'Current Ratio (Quarterly)', ['value']].value.values[0]
    current_ratio_quarterly = fast_float(current_ratio_quarterly, default=None)
    debug(f'Current Ratio (Quarterly): {current_ratio_quarterly}')

    # Long Term Debt/Equity (Quarterly)
    long_term_debt_equity_quarterly = df4.loc[df4['metric'] == 'Long Term Debt/Equity (Quarterly)', ['value']].value.values[0]
    long_term_debt_equity_quarterly = fast_float(long_term_debt_equity_quarterly, default=None)
    debug(f'Long Term Debt/Equity (Quarterly): {long_term_debt_equity_quarterly}')

    # Net Profit Margin % (Annual)
    net_profit_margin_percent_annual = df4.loc[df4['metric'] == 'Net Profit Margin % (Annual)', ['value']].value.values[0]
    net_profit_margin_percent_annual = fast_float(net_profit_margin_percent_annual, default=None)
    debug(f'Net Profit Margin % (Annual): {net_profit_margin_percent_annual}')

    revenue_estimate_current_year_r = None
    if revenue_estimate_current_year is not None:
        if revenue_estimate_current_year > 5:
            revenue_estimate_current_year_r = 2
        elif 0 <= revenue_estimate_current_year <= 5:
            revenue_estimate_current_year_r = 1
        elif revenue_estimate_current_year < 0:
            revenue_estimate_current_year_r = -1

    revenue_estimate_next_year_r = None
    if revenue_estimate_next_year is not None:
        revenue_estimate_next_year_r = 1 if revenue_estimate_next_year > 0 else -1

    curr_avg_estimate_r = None
    if earning_history_eps_actual_yearago is not None and curr_avg_estimate is not None:
        curr_avg_estimate_r = 2 if curr_avg_estimate > earning_history_eps_actual_yearago else -2

    next_qtr_avg_estimate_r = None
    if earning_history_eps_actual_nqyearago is not None and next_qtr_avg_estimate is not None:
        next_qtr_avg_estimate_r = 2 if next_qtr_avg_estimate > earning_history_eps_actual_nqyearago else -2

    total_revenue_r = None
    if total_revenue_curr is not None and total_revenue_yearago is not None:
        total_revenue_r = 1 if total_revenue_curr > total_revenue_yearago else -1

    diluted_normalized_eps_r = None
    if diluted_normalized_eps_yearago is not None and diluted_normalized_eps_curr is not None:
        diluted_normalized_eps_r = 1 if diluted_normalized_eps_curr > diluted_normalized_eps_yearago else -1

    net_profit_margin_percent_annual_r = None
    if net_profit_margin_percent_annual is not None:
        if net_profit_margin_percent_annual > 2:
            net_profit_margin_percent_annual_r = 2
        elif 0 <= net_profit_margin_percent_annual <= 2:
            net_profit_margin_percent_annual_r = 1
        elif 0 > net_profit_margin_percent_annual >= -5:
            net_profit_margin_percent_annual_r = -1
        elif net_profit_margin_percent_annual < -5:
            net_profit_margin_percent_annual_r = -2

    divident_per_share_annual_r = None
    if divident_per_share_annual is not None:
        divident_per_share_annual_r = 2 if divident_per_share_annual > 0 else -2

    mkt_cap_r = None
    if mkt_cap is not None:
        if mkt_cap > 200000:
            mkt_cap_r = 2
        elif 50000 < mkt_cap <= 200000:
            mkt_cap_r = 1
        elif 10000 < mkt_cap <= 50000:
            mkt_cap_r = 0
        elif 2000 < mkt_cap <= 10000:
            mkt_cap_r = -1
        elif 2000 < mkt_cap:
            mkt_cap_r = -2

    beta_r = None
    if beta is not None:
        beta_r = 1 if 0.75 <= beta <= 1.5 else -1

    current_ratio_quarterly_r = None
    if current_ratio_quarterly is not None:
        current_ratio_quarterly_r = 2 if current_ratio_quarterly > 1 else -2

    long_term_debt_equity_quarterly_r = None
    if long_term_debt_equity_quarterly is not None:
        if long_term_debt_equity_quarterly > 3:
            long_term_debt_equity_quarterly_r = -2
        elif 2 <= long_term_debt_equity_quarterly <= 3:
            long_term_debt_equity_quarterly_r = -1
        elif long_term_debt_equity_quarterly < 2:
            long_term_debt_equity_quarterly_r = 1

    debug("-------------- R A N K I N G --------------")
    debug(f'\n'
          f'revenue_estimate: {revenue_estimate_current_year_r}\n'
          f'curr_avg_estimate: {curr_avg_estimate_r}\n'
          f'next_qtr_avg_estimate: {next_qtr_avg_estimate_r}\n'
          f'total_revenue: {total_revenue_r}\n'
          f'diluted_normalized_eps: {diluted_normalized_eps_r}\n'
          f'net_profit_margin_percent_annual: {net_profit_margin_percent_annual_r}\n'
          f'divident_per_share_annual: {divident_per_share_annual_r}\n'
          f'mkt_cap: {mkt_cap_r}\n'
          f'beta: {beta_r}\n'
          f'current_ratio_quarterly: {current_ratio_quarterly_r}\n'
          f'long_term_debt_equity_quarterly: {long_term_debt_equity_quarterly_r}\n')

    finaly_rank = 0
    if revenue_estimate_current_year_r is not None:
        finaly_rank = finaly_rank + revenue_estimate_current_year_r
    if curr_avg_estimate_r is not None:
        finaly_rank = finaly_rank + curr_avg_estimate_r
    if next_qtr_avg_estimate_r is not None:
        finaly_rank = finaly_rank + next_qtr_avg_estimate_r
    if total_revenue_r is not None:
        finaly_rank = finaly_rank + total_revenue_r
    if diluted_normalized_eps_r is not None:
        finaly_rank = finaly_rank + diluted_normalized_eps_r
    if net_profit_margin_percent_annual_r is not None:
        finaly_rank = finaly_rank + net_profit_margin_percent_annual_r
    if divident_per_share_annual_r is not None:
        finaly_rank = finaly_rank + divident_per_share_annual_r
    if mkt_cap_r is not None:
        finaly_rank = finaly_rank + mkt_cap_r
    if beta_r is not None:
        finaly_rank = finaly_rank + mkt_cap_r
    if current_ratio_quarterly_r is not None:
        finaly_rank = finaly_rank + current_ratio_quarterly_r
    if long_term_debt_equity_quarterly_r is not None:
        finaly_rank = finaly_rank + long_term_debt_equity_quarterly_r

    debug(f"Finaly Rank: {finaly_rank}\n", WARNING)

    res = {"rank": finaly_rank,
           "revenue_estimate": revenue_estimate_current_year_r,
           "curr_avg_estimate": curr_avg_estimate_r,
           "next_qtr_avg_estimate": next_qtr_avg_estimate_r,
           "total_revenue": total_revenue_r,
           "diluted_normalized_eps": diluted_normalized_eps_r,
           "net_profit_margin_percent_annual": net_profit_margin_percent_annual_r,
           "divident_per_share_annual": divident_per_share_annual_r,
           "mkt_cap": mkt_cap_r,
           "beta": beta_r,
           "current_ratio_quarterly": current_ratio_quarterly_r,
           "long_term_debt_equity_quarterly_r": long_term_debt_equity_quarterly_r}
    debug('%%% get_ranking_data complete')
    return res


    # revenue_estimate_current_year > 5 % +2 / 0 - 5 % +1 < 0 % -1
    # revenue_estimate_next_year  positive + 1 / negative - 1
    #
    # curr_avg_estimate > earning_history_eps_actual года назад + 2 else -2
    # next_qtr_avg_estimate > earning_history_eps_actual года назад + 2 else -2
    #
    # Total Revenue > квартала год назад + 1 else -1
    # Diluted Normalized EPS > квартала год назад + 1 else -1
    # Net Profit Margin % (Annual) > 2 + 2 / 0 - 2 + 1 / < 0 - 5 - 1 / < -5 - 2
    #
    # Dividend(Per Share Annual) positive + 2 / negative - 2
    #
    # Market Capitalization > 200bln + 2 / 50 - 200bln + 1 / 2 - 10 + 0 / < 2bln - 2
    # Beta 0.75 - 1.5 + 1 else -1
    # Current Ratio(Quarterly) > 1 + 2 / < 1 - 2
    # Long Term Debt / Equity(Quarterly) > 3 - 2 / 2 - 3 - 1 / < 2 + 1
    #
    # Rank = sum of all values
    # return dict{rank: ..., next_report_date: ..., revenue_estimate_current_year: 2, ....}



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


def get_economics(ag=None, img_out_path_=IMAGES_OUT_PATH):
    headers = {'User-Agent': ag}
    url_ = {
        'Interest Rate': 'https://tradingeconomics.com/country-list/interest-rate?continent=g20',
        'Inflation Rate': 'https://tradingeconomics.com/country-list/inflation-rate?continent=g20',
        'Unemployment Rate': 'https://tradingeconomics.com/country-list/unemployment-rate?continent=g20',
        'Composite PMI': 'https://tradingeconomics.com/country-list/composite-pmi?continent=g20'
    }
    items_ = []
    try:
        for k, v in url_.items():
            html = requests.get(v, headers=headers).text
            soup = BeautifulSoup(html, "html.parser")
            items_table = soup.find('table', {"class": "table table-hover"})
            for row in items_table.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) != 0:
                    p = tuple([k])
                    entries_list = []
                    for i in range(0, len(cols)):
                        entries_list.append(cols[i].text.strip())
                        entries_tuple = tuple(entries_list)
                        info = ()
                        info = p + entries_tuple
                    items_.append(info)
        array = np.asarray(items_)
        df = pd.DataFrame(array)
        df.columns = ['Data', 'Country', 'Last', 'Previous', 'Reference', 'Unit']
    except Exception as e05:
        debug(e05)
        return
    df = df.drop(df[(df.Country != 'Russia')
                    & (df.Country != 'China')
                    & (df.Country != 'United States')
                    & (df.Country != 'United Kingdom')
                    & (df.Country != 'Euro Area')
                    & (df.Country != 'France')
                    & (df.Country != 'Germany')
                    & (df.Country != 'Japan')].index)
    filename = os.path.join(img_out_path_, 'economic_data.csv')
    df.to_csv(filename, index=False)
    debug('Get economics complete')


# ============================== TW GET ================================
def get_tw_charts(driver=None, img_out_path_=IMAGES_OUT_PATH):
    treemaps = {
        'sectors': 'https://www.tradingview.com/chart/8ql9Y9yV/',
        'crypto': 'https://www.tradingview.com/chart/HHWJel9w/',
        'rtsi': 'https://www.tradingview.com/chart/PV8hXeeD/',
    }
    try:
        with driver:
            for k, v in treemaps.items():
                im_path = os.path.join(img_out_path_, k + '.png')
                driver.get(v)
                sleep(22)
                elem = driver.find_element_by_class_name("chart-container-border")
                webdriver.ActionChains(driver).move_to_element(elem).perform()
                driver.execute_script("return arguments[0].scrollIntoView();", elem)
                sleep(8)
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
    items_['NYSE Trending Stocks %'] = str(round(items_['NyseA'] * 100 / items_['NyseT'], 2)) + '%' + ' акций NYSE в тренде'
    items_['NASDAQ Trending Stocks %'] = str(round(items_['NasdA'] * 100 / items_['NasdT'], 2)) + '%' + ' акций NASDAQ в тренде'
    items_['SP500 Trending Stocks %'] = str(round(items_['SPXA'] * 100 / items_['SPXT'], 2)) + '%' + ' акций SP500 в тренде'
    items_.pop('NyseT')
    items_.pop('NyseA')
    items_.pop('NasdT')
    items_.pop('NasdA')
    items_.pop('SPXT')
    items_.pop('SPXA')
    with open(img_out_path_+'sma50.csv', 'w+') as f:
        write = csv.DictWriter(f, items_.keys())
        # write.writeheader()
        write.writerow(items_)
    debug('sma50 complete')


# # ============================== Treasury Curve and Div Yield GET ================================



# def qt_curve(img_out_path_=IMAGES_OUT_PATH):
#     x = quandl.get("USTREASURY/YIELD", authtoken="gWq5SV_V-yFkXVMgrwwy", rows=1)
#     print(x)
#     x = str(x)
#     with open(img_out_path_+'treasury_curve.csv', 'w+') as f:
#         f.write(f'{x}')
#     debug('qt_curve complete')

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
    with open(img_out_path_+'spx_yield.csv', 'w+') as f:
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
    with open(img_out_path_+'vix_cont.csv', 'w+') as f:
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

