import os
from time import sleep
from datetime import date, timedelta
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
                debug(f'img_out_path_:{img_out_path_}')
                debug(f'k:{k}')
                im_path = os.path.join(img_out_path_, k + '.png')
                debug(f'im_path:{im_path}')
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

