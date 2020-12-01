#!/usr/bin/env python3

import os
import yaml
from time import sleep
from datetime import date, datetime, timedelta
import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
from PIL import Image, ImageFilter
from quotes.parsers_env import firefox_init, agents



conf = yaml.safe_load(open('config/settings.yaml'))
LOGS = conf['PATHS']['LOGS']
WEBDRIVER = conf['PATHS']['WEBDRIVER']
IMAGES_OUT_PATH = conf['PATHS']['IMAGES_OUT_PATH']


# ============================== Inflows GET ================================
def get_flows(driver=None, img_out_path_=None):
    etfs = ['VCIT', 'SPY', 'VTI', 'VEA', 'VWO', 'QQQ', 'VXX', 'TLT', 'SHY', 'LQD']
    with driver:
        driver.get('https://www.etf.com/etfanalytics/etf-fund-flows-tool')
        sleep(8)
        elem = driver.find_element_by_xpath(".//*[@id='edit-tickers']")
        elem.send_keys("GLD, SPY, VTI, VEA, VWO, QQQ, VXX, TLT, SHY, LQD, VCIT")
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
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, ".//*[@id='edit-submitbutton']"))).click()
        except Exception as e1:
            print('Try to re-run the scraper', e1)
            exit()
        sleep(5)
        elem = driver.find_element_by_xpath(".//*[@id='fundFlowsTitles']")
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
    with open(os.path.join('results', 'img_out', 'adv.csv'), 'w+') as f:
        for rows_ in items_:
            write = csv.writer(f)
            write.writerow(rows_)
    print('adv complete')


# ============================== FINVIZ TREEMAP GET ================================
def get_finviz_treemaps(driver=None, img_out_path_=None):
    display = Display(visible=0, size=(1920, 1080))
    display.start()
    treemaps = {
        'treemap_1d': 'https://finviz.com/map.ashx?t=sec_all',
        'treemap_ytd': 'https://finviz.com/map.ashx?t=sec_all&st=ytd',
        'global_treemap': 'https://finviz.com/map.ashx?t=geo',
        'global_treemap_ytd': 'https://finviz.com/map.ashx?t=geo&st=ytd',
    }
    with driver:
        for k, v in treemaps.items():
            img_path = os.path.join(img_out_path_, k + '.png')
            driver.get(v)
            sleep(3)
            elem = driver.find_element_by_id('body')
            # elem = driver.find_element_by_class_name('chart')
            location = elem.location
            size = elem.size
            driver.save_screenshot(img_path)
            x = location['x']
            y = location['y']
            width = location['x'] + size['width']
            height = location['y'] + size['height']
            im = Image.open(img_path)
            im = im.crop((int(x), int(y), int(width)+20, int(height)+16))
            # im = im.crop((int(x), int(y), int(width), int(height)))
            im.save(img_path)
    display.stop()
    print('Get Finviz Treemap complete' + '\n')



# # ============================== COIN360 TREEMAP GET ================================
# def get_coins360_treemaps():
#     display = Display(visible=0, size=(1920, 1080))
#     display.start()
#     url_ = 'https://coin360.com/?exceptions=[USDT%2CUSDC]&period=24h&range=[500000000%2C295729609429]'
#     filename = 'coins_treemap'
#     driver = firefox_init()
#     with driver:  # TODO WARNING! ATTENTION!
#         img_path = os.path.join(IMAGES_OUT_PATH, filename + '.png')
#         driver.get(url_)
#         sleep(10)
#         elem = driver.find_element_by_id('app')
#         location = elem.location
#         size = elem.size
#         driver.save_screenshot(img_path)
#         x = location['x']
#         y = location['y']
#         width = location['x'] + size['width']
#         height = location['y'] + size['height']
#         im = Image.open(img_path)
#         im = im.crop((int(x), int(y+80), int(width), int(height-25)))
#         im.save(img_path)
#         print('Get coin360 Treemap complete' + '\n')
#     display.stop()

# def scrape_economics():
#     headers = {'User-Agent': agent_rotation()}
#     url_ = {
#         'Interest Rate': 'https://tradingeconomics.com/country-list/interest-rate?continent=g20',
#         'Inflation Rate': 'https://tradingeconomics.com/country-list/inflation-rate?continent=g20',
#         'Unemployment Rate': 'https://tradingeconomics.com/country-list/unemployment-rate?continent=g20',
#         'Composite PMI': 'https://tradingeconomics.com/country-list/composite-pmi?continent=g20'
#     }
#     items_ = []
#     for k, v in url_.items():
#         html = requests.get(v, headers=headers).text
#         soup = BeautifulSoup(html, "html.parser")
#         # identify table we want to scrape
#         items_table = soup.find('table', {"class": "table table-hover"})
#         for row in items_table.find_all('tr'):
#             cols = row.find_all('td')
#             if len(cols) != 0:
#                 p = tuple([k])
#                 entries_list = []
#                 for i in range(0, len(cols)):
#                     entries_list.append(cols[i].text.strip())
#                     entries_tuple = tuple(entries_list)
#                     info = ()
#                     info = p + entries_tuple
#                 items_.append(info)
#     array = np.asarray(items_)
#     df = pd.DataFrame(array)
#     df.columns = ['Data', 'Country', 'Last', 'Previous', 'Reference', 'Unit']
#
#     df = df.drop(df[(df.Country != 'Russia')
#                     & (df.Country != 'China')
#                     & (df.Country != 'United States')
#                     & (df.Country != 'United Kingdom')
#                     & (df.Country != 'Euro Area')
#                     & (df.Country != 'France')
#                     & (df.Country != 'Germany')
#                     & (df.Country != 'Japan')].index)
#     filename = os.path.join(YAHOO_PATH, 'economic_data.csv')
#     df.to_csv(filename, index=False)
#
#
# # ============================== TW GET ================================
#
#
# def get_tw(url):
#     filename = str(url).split('/')
#     driver = firefox_init()
#     driver.get(url)
#     sleep(23)
#     # try:
#     #     driver.find_element_by_xpath("//button[@class='close-button-7uy97o5_']").click()
#     #     sleep(3)
#     # except Exception as e:
#     #     print(e)
#     img_path = os.path.join(IMAGES_OUT_PATH, f'{filename[4]}' + '.png')
#     driver.get_screenshot_as_file(img_path)
#     driver.quit()
#
#
# def tw_multi_render():
#     with mp.Pool(processes=4) as pool:
#         urls = ['https://www.tradingview.com/chart/8ql9Y9yV/',
#                 'https://www.tradingview.com/chart/Z9Sidx11/',
#                 'https://www.tradingview.com/chart/HHWJel9w/',
#                 'https://www.tradingview.com/chart/PV8hXeeD/'
#                 ]
#         pool.map(get_tw, [url for url in urls])
#
#     img1 = os.path.join(IMAGES_OUT_PATH, '8ql9Y9yV.png')
#     spdr = os.path.join(IMAGES_OUT_PATH, 'sectors.png')
#     img2 = os.path.join(IMAGES_OUT_PATH, 'Z9Sidx11.png')
#     vola = os.path.join(IMAGES_OUT_PATH, 'volatility.png')
#     img3 = os.path.join(IMAGES_OUT_PATH, 'HHWJel9w.png')
#     crpt = os.path.join(IMAGES_OUT_PATH, 'crypto.png')
#     img4 = os.path.join(IMAGES_OUT_PATH, 'PV8hXeeD.png')
#     rtsi = os.path.join(IMAGES_OUT_PATH, 'rtsi.png')
#
#     crop(img1, spdr, 56, 44, 320, 43)
#     crop(img2, vola, 56, 44, 320, 43)
#     crop(img3, crpt, 56, 44, 320, 43)
#     crop(img4, rtsi, 56, 44, 320, 43)
#     print('Get TW Charts complete' + '\n')
#
# # ============================== ADVANCE/DECLINE GET ================================
#
#
# def advance_decline():
#     headers = {'User-Agent': agent_rotation()}
#     url_ = 'https://www.marketwatch.com/tools/marketsummary?region=usa&screener=nasdaq'
#     items_ = []
#     html = requests.get(url_, headers=headers).text
#     soup = BeautifulSoup(html, "html.parser")
#     table = soup.find('div', {"id": "marketbreakdown"})
#     for row in table.find_all('tr'):
#         cols = row.find_all('td')
#         if len(cols) != 0:
#             entries_list = []
#             for i in range(0, len(cols)):
#                 entries_list.append(cols[i].text.strip())
#                 entries_tuple = tuple(entries_list)
#                 info = ()
#                 info = entries_tuple
#             items_.append(info)
#     del items_[5:8]
#     with open(os.path.join('results', 'img_out', 'adv.csv'), 'w+') as f:
#         for rows_ in items_:
#             write = csv.writer(f)
#             # write.writerow(fields)
#             write.writerow(rows_)
#     print('adv complete')
#
#
# def get_sma50():
#     """
#     parse
#     calc
#     csv save
#     csv load last value
#     future - chart
#     """
#     headers = {'User-Agent': agent_rotation()}
#     urls_d = {
#         'NyseT': 'https://finviz.com/screener.ashx?v=151&f=exch_nyse&ft=4',
#         'NyseA': 'https://finviz.com/screener.ashx?v=151&f=exch_nyse,ta_sma50_pa&ft=4',
#         'NasdT': 'https://finviz.com/screener.ashx?v=151&f=exch_nasd&ft=4',
#         'NasdA': 'https://finviz.com/screener.ashx?v=151&f=exch_nasd,ta_sma50_pa&ft=4',
#         'SPXT': 'https://finviz.com/screener.ashx?v=151&f=idx_sp500&ft=4',
#         'SPXA': 'https://finviz.com/screener.ashx?v=151&f=idx_sp500,ta_sma50_pa&ft=4'
#     }
#     items_ = {}
#     for k, v in urls_d.items():
#         html = requests.get(v, headers=headers).text
#         soup = BeautifulSoup(html, "html.parser")
#         table = soup.find('td', {"class": "count-text"}).text.strip('Total:  ')
#
#         items_[k] = int(table[:-3])
#     items_['NYSE Trending Stocks %'] = round(items_['NyseA'] * 100 / items_['NyseT'], 2)
#     items_['NASDAQ Trending Stocks %'] = round(items_['NasdA'] * 100 / items_['NasdT'], 2)
#     items_['SP500 Trending Stocks %'] = round(items_['SPXA'] * 100 / items_['SPXT'], 2)
#     items_.pop('NyseT')
#     items_.pop('NyseA')
#     items_.pop('NasdT')
#     items_.pop('NasdA')
#     items_.pop('SPXT')
#     items_.pop('SPXA')
#
#     print(items_)
#     with open(os.path.join('results', 'img_out', 'sma50.csv'), 'w+') as f:
#         write = csv.DictWriter(f, items_.keys())
#         # write.writerow(fields)
#         write.writeheader()
#         write.writerow(items_)
#     print('sma50 complete')

# Call
# get_flows(driver=firefox_init(webdriver_path=WEBDRIVER, agent_rotation=agents()), img_out_path_=IMAGES_OUT_PATH)
# advance_decline(ag=None)
get_finviz_treemaps(driver=firefox_init(webdriver_path=WEBDRIVER, agent_rotation=agents()), img_out_path_=IMAGES_OUT_PATH)