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
import quandl
from scipy.stats import norm
import random


# ============================== Inflows GET ================================
def get_flows(driver=None, img_out_path_=None):
    etfs = ['VCIT', 'SPY', 'VTI', 'VEA', 'VWO', 'QQQ', 'VXX', 'TLT', 'SHY', 'LQD']
    with driver:
        driver.get('https://www.etf.com/etfanalytics/etf-fund-flows-tool')
        sleep(10)
        try:
            elem = driver.find_element_by_xpath(".//*[@id='edit-tickers']")
            print(elem)
            print('elem 1 has been located')
        except Exception as e0:
            print('Trying to reload the page', e0)
            driver.refresh()
        elem.send_keys("GLD, SPY, VTI, VEA, VWO, QQQ, VXX, TLT, SHY, LQD, VCIT")
        print('keys has been send')
        sleep(0.7)
        today = date.today()
        day7 = timedelta(days=7)  # TODO Меняется ли размер окна от колва дней?
        delta = today - day7
        start_d = delta.strftime("%Y-%m-%d")
        end_d = today.strftime("%Y-%m-%d")
        elem = driver.find_element_by_xpath(".//*[@id='edit-startdate-datepicker-popup-0']")
        elem.send_keys(start_d)
        sleep(0.6)
        elem = driver.find_element_by_xpath(".//*[@id='edit-enddate-datepicker-popup-0']")
        elem.send_keys(end_d)
        sleep(0.5)
        try:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, ".//*[@id='edit-submitbutton']"))).click()
            print('Button has been clicked')
        except Exception as e1:
            print('Button click error. Try to re-run the scraper', e1)
            return None
        sleep(10)
        try:
            elem = driver.find_element_by_xpath(".//*[@id='fundFlowsTitles']")
            print('elem 2-Titles has been located')

        except Exception as e2:
            print('Titles elem error. Try to re-run the scraper', e2)
            return None
        webdriver.ActionChains(driver).move_to_element(elem).perform()
        driver.execute_script("return arguments[0].scrollIntoView();", elem)
        sleep(1)

        for etf in etfs:
            sleep(2)
            print(etf)
            tag = ".//*[@id=\'" + f'{etf}' + "_nf']"
            tag2 = ".//*[@id=\'container_" + f'{etf}' + "'" + "]"
            icon = driver.find_element_by_xpath(tag)  # ".//*[@id='{etf}_nf']"
            driver.execute_script("arguments[0].click();", icon)
            sleep(3)
            graph = driver.find_element_by_xpath(tag2)  # ".//*[@id='container_{etf}']"
            driver.execute_script("return arguments[0].scrollIntoView();", graph)
            sleep(1)
            driver.save_screenshot(os.path.join(img_out_path_, f'inflows_{etf}.png'))
            img = Image.open(os.path.join(img_out_path_, f'inflows_{etf}.png'))
            img_crop = img.crop((360, 367, 995, 665))
            img_crop.save(os.path.join(img_out_path_, f'inflows_{etf}.png'), quality=100, subsampling=0)
    print('Get Fund Flows complete' + '\n')


def get_flows2(driver=None, img_out_path_=None):
    etfs = ['VCIT', 'SPY', 'VTI', 'VEA', 'VWO', 'QQQ', 'VXX', 'TLT', 'SHY', 'LQD']
    with driver:
        driver.get('https://www.etf.com/etfanalytics/etf-fund-flows-tool')
        sleep(10)
        html = driver.page_source
        print(html)
        # for i in range(0, 20):
        while True:
            try:
                elem = driver.find_element_by_xpath(".//*[@id='edit-tickers']")
                print('elem 1 has been located')
                break
            except Exception as e10:
                print(f'Trying to reload the page', e10)
                driver.refresh()
                continue
                # break
        elem.send_keys("GLD, SPY, VTI, VEA, VWO, QQQ, VXX, TLT, SHY, LQD, VCIT")
        print('keys has been send')
        sleep(0.7)
        today = date.today()
        day7 = timedelta(days=7)  # TODO Меняется ли размер окна от колва дней?
        delta = today - day7
        start_d = delta.strftime("%Y-%m-%d")
        end_d = today.strftime("%Y-%m-%d")
        elem = driver.find_element_by_xpath(".//*[@id='edit-startdate-datepicker-popup-0']")
        elem.send_keys(start_d)
        sleep(0.6)
        elem = driver.find_element_by_xpath(".//*[@id='edit-enddate-datepicker-popup-0']")
        elem.send_keys(end_d)
        sleep(0.5)
        try:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, ".//*[@id='edit-submitbutton']"))).submit()
            print('Button has been clicked')
        except Exception as e1:
            print('Button click error. Try to re-run the scraper', e1)
            return None
        sleep(10)
        html = driver.page_source
        print(html)
        # if html:
        #     soup = BeautifulSoup(html, 'html.parser')

        try:
            # elem = driver.find_element_by_xpath(".//*[@id='fundFlowsTablesWrapper']")
            elem = driver.find_element_by_class_name("top_fund_flows_tables")
            print('elem 2-Titles has been located')
        except Exception as e2:
            print('Titles elem error. Try to re-run the scraper', e2)
            return None
        webdriver.ActionChains(driver).move_to_element(elem).perform()
        driver.execute_script("return arguments[0].scrollIntoView();", elem)
        sleep(1)

        for etf in etfs:
            sleep(2)
            print(etf)
            tag = ".//*[@id=\'" + f'{etf}' + "_nf']"
            tag2 = ".//*[@id=\'container_" + f'{etf}' + "'" + "]"
            icon = driver.find_element_by_xpath(tag)  # ".//*[@id='{etf}_nf']"
            driver.execute_script("arguments[0].click();", icon)
            sleep(3)
            graph = driver.find_element_by_xpath(tag2)  # ".//*[@id='container_{etf}']"
            driver.execute_script("return arguments[0].scrollIntoView();", graph)
            sleep(1)
            driver.save_screenshot(os.path.join(img_out_path_, f'inflows_{etf}.png'))
            img = Image.open(os.path.join(img_out_path_, f'inflows_{etf}.png'))
            img_crop = img.crop((360, 367, 995, 665))
            img_crop.save(os.path.join(img_out_path_, f'inflows_{etf}.png'), quality=100, subsampling=0)
    print('Get Fund Flows complete' + '\n')


# ============================== ADVANCE/DECLINE GET ================================
def advance_decline(ag=None):
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
        print(e02)
        return
    with open(os.path.join('results', 'img_out', 'adv.csv'), 'w+') as f:
        for rows_ in items_:
            write = csv.writer(f)
            write.writerow(rows_)
    print('adv complete')


# ============================== FINVIZ TREEMAP GET ================================
def get_finviz_treemaps(driver=None, img_out_path_=None):
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
                elem = driver.find_element_by_id('body')
                driver.execute_script("return arguments[0].scrollIntoView();", elem)
                driver.save_screenshot(img_path)
                im = Image.open(img_path)
                im = im.crop((210, 0, 1330, 625))
                im.save(img_path, quality=100, subsampling=0)
            except Exception as e03:
                print(e03)
                return
    print('Get Finviz Treemap complete' + '\n')


# ============================== COIN360 TREEMAP GET ================================
def get_coins360_treemaps(driver=None, img_out_path_=None):
    url_ = 'https://coin360.com/?exceptions=[USDT%2CUSDC]&period=24h&range=[500000000%2C295729609429]'
    with driver:
        img_path = os.path.join(img_out_path_, 'coins_treemap' + '.png')
        try:
            driver.get(url_)
            sleep(5)
            elem = driver.find_element_by_id('app')
            location = elem.location
            size = elem.size
            driver.save_screenshot(img_path)
            x = location['x']
            y = location['y']
            width = location['x'] + size['width']
            height = location['y'] + size['height']
            im = Image.open(img_path)
            im = im.crop((int(x), int(y+80), int(width), int(height-20)))
            im.save(img_path, quality=100, subsampling=0)
        except Exception as e04:
            print(e04)
            return
    print('Get coin360 Treemap complete' + '\n')


def get_economics(ag=None, img_out_path_=None):
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
        print(e05)
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


# ============================== TW GET ================================
def get_tw_charts(driver=None, img_out_path_=None):
    treemaps = {
        'sectors': 'https://www.tradingview.com/chart/8ql9Y9yV/',
        'volatility': 'https://www.tradingview.com/chart/Z9Sidx11/',
        'crypto': 'https://www.tradingview.com/chart/HHWJel9w/',
        'rtsi': 'https://www.tradingview.com/chart/PV8hXeeD/',
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
                sleep(5)
                try:
                    close_button1 = driver.find_element_by_class_name(
                        'tv-dialog__close close-d1KI_uC8 dialog-close-3phLlAHH js-dialog__close')
                    driver.execute_script("arguments[0].click();", close_button1)
                except Exception as e1:
                    print(e1)
                try:
                    close_button2 = driver.find_element_by_xpath("//button[@class='close-button-7uy97o5_']").click()
                    driver.execute_script("arguments[0].click();", close_button2)
                    sleep(3)
                except Exception as e2:
                    print(e2)
                driver.get_screenshot_as_file(im_path)
                im = Image.open(im_path)
                width, height = im.size
                cropped = im.crop((56, 44, width - 320, height - 43))
                cropped.save(im_path, quality=100, subsampling=0)
    except Exception as e06:
        print(e06)
        return
    print('Get TW Charts complete' + '\n')


# ============================== SMA50 GET ================================
def get_sma50(ag=None):
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
            html = requests.get(v, headers=headers).text
            soup = BeautifulSoup(html, "html.parser")
            table = soup.find('td', {"class": "count-text"}).text.strip('Total:  ')
            items_[k] = int(table[:-3])
    except TypeError as e01:
        print(e01)
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
    with open(os.path.join('results', 'img_out', 'sma50.csv'), 'w+') as f:
        write = csv.DictWriter(f, items_.keys())
        # write.writeheader()
        write.writerow(items_)
    print('sma50 complete')


# ============================== Treasury Curve and Div Yield GET ================================
def qt_curve():
    x = quandl.get("USTREASURY/YIELD", authtoken="gWq5SV_V-yFkXVMgrwwy", rows=1)
    x = str(x)
    with open(os.path.join('results', 'img_out', 'treasury_curve.csv'), 'w+') as f:
        f.write(f'{x}')


def spx_yield():
    x = quandl.get("MULTPL/SP500_DIV_YIELD_MONTH", authtoken="gWq5SV_V-yFkXVMgrwwy", rows=1)
    x = str(x)
    with open(os.path.join('results', 'img_out', 'spx_yield.csv'), 'w+') as f:
        f.write(f'{x}')


def vix_curve(driver=None, img_out_path_=None):
    url_ = 'http://vixcentral.com/'
    img_curve = os.path.join(img_out_path_, 'vix_curve' + '.png')
    with driver:
        driver.get(url_)
        sleep(3)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='VIX Index']"))).click()
        print('Vix disabled, button has been clicked')
        sleep(4)
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "highcharts-button-symbol"))).click()
        print('Menu button has been clicked')
        sleep(5)
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(text(),'Download PNG image')]"))).click()
        print('PNG has been clicked')
        sleep(5)
    im = Image.open('vix-futures-term-structu.png')
    im = im.crop((0, 120, 1200, 750))
    im.save(img_curve, quality=100, subsampling=0)
    print('Vix_curve complete' + '\n')


def vix_cont():
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
    with open(os.path.join('results', 'img_out', 'vix_cont.csv'), 'w+') as f:
        f.write(f'{vix}')


def users_count():
    with open(os.path.join('results', 'img_out', 'users.csv'), 'r') as f0:
        for x in f0:
            x = x.split()
    users = int(x[0]) + norm.ppf(random.uniform(0, 1), loc=2, scale=2)

    with open(os.path.join('results', 'img_out', 'users.csv'), 'w+') as f:
        write = f.write(f'{int(users)}')
    print(int(users))
    return users
