import logging
import multiprocessing as mp
import os
import sys
import pathlib
from datetime import date, datetime, timedelta
from random import choice
from time import sleep
# from mlfinlab.online_portfolio_selection import *
# from alpha_vantage.cryptocurrencies import CryptoCurrencies
import mplfinance as mpf
import numpy as np
import pandas as pd
import requests
import yaml
import csv
from PIL import Image, ImageFilter
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
import schedule
from get_quotes_data import index_calc
from yahoo_downloader import download_yahoo, load_csv


# ============================== Environment Setup ======================
conf = yaml.safe_load(open(os.path.abspath('config/settings.yaml')))
PYTHON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(PYTHON_PATH)
os.environ["PYTHONUNBUFFERED"] = "1"
YAHOO_PATH = conf['PATHS']['YAHOO_PATH']
LOGS = conf['PATHS']['LOGS']
WEBDRIVER = conf['PATHS']['WEBDRIVER']
COINMARKETCAP = conf['COINMARKETCAP']['KEY']
COINS_DATA = conf['PATHS']['COINS_DATA']
IMAGES_OUT_PATH = conf['PATHS']['IMAGES_OUT_PATH']
ALPHA_VANTAGE = conf['ALPHA_VANTAGE']['API_KEY']
start_date = datetime(2019, 1, 1)
end_date = datetime.utcnow()

logging.basicConfig(
    filename='error.log',
    filemode='w',
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO)
logging.getLogger('crypto_wsj').setLevel(level=logging.WARNING)


# ============================== Functions ======================
def crop(img_path, img_path_save, a, b, c, d):
    # 56 pixels from the left
    # 44 pixels from the top
    # 320 pixels from the right
    # 43 pixels from the bottom
    img = Image.open(img_path)
    img = img.filter(ImageFilter.DETAIL)
    width, height = img.size
    print(width, height)
    cropped = img.crop((a, b, width - c, height - d))
    cropped.save(img_path_save, quality=100, subsampling=0)



#
# def selenium_init():
#     chrome_options = Options()
#     chrome_options.add_argument("--window-size=1920,1080")
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--proxy-server=direct://")
#     chrome_options.add_argument("--proxy-bypass-list=*")
#     chrome_options.add_argument("--start-maximized")
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('--ignore-certificate-errors')
#     chrome_options.add_argument(f'user-agent={agent_rotation()}')
#     chrome_options.add_argument("--enable-javascript")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_extension(os.path.join(WEBDRIVER, 'cfhdojbkjhnklbpkdaibdccddilifddb.crx'))
#     driver_path = os.path.join(WEBDRIVER, 'chromedriver_86')
#     driver = webdriver.Chrome(driver_path, options=chrome_options)
#     print(driver.execute_script("return navigator.userAgent"))
#     sleep(1)
#     return driver


def firefox_init():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.http.use-cache", False)
    profile.set_preference("javascript.enabled", True)
    profile.set_preference("general.useragent.override", f"{agent_rotation()}")
    ff_options = webdriver.FirefoxOptions()
    ff_options.add_argument('-window-size=1980,1080')
    ff_options.add_argument('-headless')
    driver = webdriver.Firefox(executable_path=os.path.join(WEBDRIVER, 'geckodriver_0_28'),
                               firefox_profile=profile, options=ff_options)
    # driver.install_addon(os.path.join(WEBDRIVER, 'adblock_plus-3.10-an+fx.xpi'), temporary=True)
    p = str(pathlib.Path('adblock_for_firefox-4.24.1-fx.xpi').parent.absolute()) + \
        '/quotes/webdriver/adblock_for_firefox-4.24.1-fx.xpi'
    driver.install_addon(str(os.path.abspath(p)), temporary=True)
    # driver.set_window_size(1600, 1200)
    driver.maximize_window()
    sleep(1)
    print(driver.execute_script("return navigator.userAgent"))
    return driver


def returns(file_path=None, filename=None):
    df = pd.read_csv(os.path.join(file_path, filename), index_col='Date', parse_dates=True)
    df_pch = df.pct_change(periods=1)
    df_pch.dropna(inplace=True)
    return df_pch
# ============================== TOP CRYPTO GET ================================


def ptable_to_csv(table, filename, headers=True):
    raw = table.get_string()
    data = [tuple(filter(None, map(str.strip, splitline)))
            for line in raw.splitlines()
            for splitline in [line.split('|')] if len(splitline) > 1]
    with open(filename, 'w') as f:
        for d in data:
            f.write('{}\n'.format(','.join(d)))
    print('cointop100 successfully saved!' + '\n')

#
# def get_top100_crypto():
#     api = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY='
#     api += COINMARKETCAP
#     raw_data = requests.get(api).json()
#     data = raw_data['data']
#     table = PrettyTable()
#
#     for currency in data:
#         name = currency['name']
#         price = currency['quote']['USD']['price']
#         volume24 = currency['quote']['USD']['volume_24h']
#         change_24h = currency['quote']['USD']['percent_change_24h']
#         change_7d = currency['quote']['USD']['percent_change_7d']
#         change_cap = currency['quote']['USD']['market_cap']
#         if change_cap >= 100000000 and volume24 >= 300000 and change_24h <= 20:
#             # TODO придумать условия для 2х портов для ебанатиков и на неделю
#             table.add_row([name, price, volume24, change_24h, change_7d, change_cap])
#
#     table.field_names = ["Name", "Price", "Volume 24h", "Change 24h", "Change 7d", "Market Cap"]
#     table.sortby = "Change 24h"
#     table.reversesort = True
#     path = os.path.join(COINS_DATA, 'cointop100.csv')
#     ptable_to_csv(table, path, headers=True)
#

# def download_daily_crypto_price(tickers, cc, data_path=COINS_DATA):
#     first_date_list = []
#     counter = 0
#     for ticker in tickers:
#         counter += 1  # alpha_vantage only allows 5 ticker downloads per min so...
#         if counter % 5 == 0:  # pause script for 1 min every 5 downloads:
#             sleep(60)
#         try:
#             ticker_data, ticker_meta_data = cc.get_digital_currency_daily(symbol=ticker, market='USD')
#             ticker_data = ticker_data.rename(columns={
#                 "1b. open (USD)": "open",
#                 "2b. high (USD)": "high",
#                 "3b. low (USD)": "low",
#                 "4b. close (USD)": "adjusted_close",
#                 "5. volume": "volume",
#                 "6. market cap (USD)": "mcap"
#             })
#             ticker_data.drop(columns={
#                 "1a. open (USD)",
#                 "2a. high (USD)",
#                 "3a. low (USD)",
#                 "4a. close (USD)"
#             }, axis=1, inplace=True)
#         except Exception as e:
#             print(str(e) + "...a problem calling the alpha_vantage API. \n")
#             sys.exit(1)  # quit this script
#         adjusted_close = ticker_data['adjusted_close'].loc[ticker_data['adjusted_close'] > 0]
#         adjusted_close = adjusted_close.sort_index()
#         adjusted_close.to_csv(data_path + ticker + '.csv', header=True)
#         first_date = adjusted_close.index.min()
#         first_date_list.append(first_date)
#     max_first_date = pd.Series(first_date_list).max()
#     return max_first_date.strftime('%Y-%m-%d')


# def crypto_download():
#     cc = CryptoCurrencies(key=ALPHA_VANTAGE, output_format='pandas')
#     coins = conf['CRYPTO_ASSETS']
#     print(coins)
#     max_first_date = download_daily_crypto_price(coins, cc)
#     print(max_first_date)
#
#
# def coins_merge():
#     coins_list = conf['CRYPTO_ASSETS']
#     main_df = pd.DataFrame()
#     for coin in coins_list:
#         path = os.path.join(COINS_DATA, f'{coin}.csv')
#         coins_df = pd.read_csv(path, index_col='date', parse_dates=True)
#         coins_df.rename({'adjusted_close': f'{coin}'}, axis=1, inplace=True)
#         if len(main_df) == 0:
#             main_df = coins_df
#         else:
#             main_df = pd.merge(main_df, coins_df, left_index=True, right_index=True)
#     main_df.dropna(inplace=True)
#     path = os.path.join(COINS_DATA, 'all_coins.csv')
#     main_df.to_csv(path, index_label='date')
#     print('Coins Data preparation complete!')


# def get_coins_portfolio():
#     closes = os.path.join(COINS_DATA, 'all_coins.csv')
#     coins_prices = pd.read_csv(closes, index_col='date', parse_dates=True)
#
#     btc = coins_prices.copy()
#     btc.drop(columns=['TUSD'], inplace=True)
#
#     btc_port = BAH()
#     pamr0 = PAMR(optimization_method=1, epsilon=0.4, agg=20)
#     olmar1 = OLMAR(reversion_method=1, epsilon=10, window=20)
#
#     btc_port.allocate(asset_prices=btc, resample_by='D', weights=None, verbose=True)
#     pamr0.allocate(asset_prices=coins_prices, resample_by='D', verbose=True)
#     olmar1.allocate(asset_prices=coins_prices, resample_by='D', verbose=True)
#
#     # s1 = (olmar1.portfolio_return - 1) * 100
#     # s2 = (pamr0.portfolio_return - 1) * 100
#     s1 = olmar1.portfolio_return
#     s2 = pamr0.portfolio_return
#     port = 0.5*s1 + 0.5*s2
#
#     # print('olmar1_all_weights \n', olmar1.all_weights)
#     # print('pamr0_all_weights \n', pamr0.all_weights)
#
#     port_ret = (port['Returns'] - port['Returns'].shift(1)) / port['Returns'].shift(1)
#     bench_ret = (btc['BTC'] - btc['BTC'].shift(1)) / btc['BTC'].shift(1)
#     import quantstats as qs
#     qs.reports.html(port_ret, benchmark=bench_ret, output=os.path.join(COINS_DATA, 'btc.html'))


# def get_crypto():
#     crypto_download()
#     coins_merge()
    # get_coins_portfolio()

# ============================== TW GET ================================


def get_tw(url):
    filename = str(url).split('/')
    driver = firefox_init()
    driver.get(url)
    sleep(23)
    # try:
    #     driver.find_element_by_xpath("//button[@class='close-button-7uy97o5_']").click()
    #     sleep(3)
    # except Exception as e:
    #     print(e)
    img_path = os.path.join(IMAGES_OUT_PATH, f'{filename[4]}' + '.png')
    driver.get_screenshot_as_file(img_path)
    driver.quit()


def tw_multi_render():
    with mp.Pool(processes=4) as pool:
        urls = ['https://www.tradingview.com/chart/8ql9Y9yV/',
                'https://www.tradingview.com/chart/Z9Sidx11/',
                'https://www.tradingview.com/chart/HHWJel9w/',
                'https://www.tradingview.com/chart/PV8hXeeD/'
                ]
        pool.map(get_tw, [url for url in urls])

    img1 = os.path.join(IMAGES_OUT_PATH, '8ql9Y9yV.png')
    spdr = os.path.join(IMAGES_OUT_PATH, 'sectors.png')
    img2 = os.path.join(IMAGES_OUT_PATH, 'Z9Sidx11.png')
    vola = os.path.join(IMAGES_OUT_PATH, 'volatility.png')
    img3 = os.path.join(IMAGES_OUT_PATH, 'HHWJel9w.png')
    crpt = os.path.join(IMAGES_OUT_PATH, 'crypto.png')
    img4 = os.path.join(IMAGES_OUT_PATH, 'PV8hXeeD.png')
    rtsi = os.path.join(IMAGES_OUT_PATH, 'rtsi.png')

    crop(img1, spdr, 56, 44, 320, 43)
    crop(img2, vola, 56, 44, 320, 43)
    crop(img3, crpt, 56, 44, 320, 43)
    crop(img4, rtsi, 56, 44, 320, 43)
    print('Get TW Charts complete' + '\n')

# ============================== ADVANCE/DECLINE GET ================================


def advance_decline():
    headers = {'User-Agent': agent_rotation()}
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
            # write.writerow(fields)
            write.writerow(rows_)
    print('adv complete')


def get_sma50():
    """
    parse
    calc
    csv save
    csv load last value
    future - chart
    """
    headers = {'User-Agent': agent_rotation()}
    urls_d = {
        'NyseT': 'https://finviz.com/screener.ashx?v=151&f=exch_nyse&ft=4',
        'NyseA': 'https://finviz.com/screener.ashx?v=151&f=exch_nyse,ta_sma50_pa&ft=4',
        'NasdT': 'https://finviz.com/screener.ashx?v=151&f=exch_nasd&ft=4',
        'NasdA': 'https://finviz.com/screener.ashx?v=151&f=exch_nasd,ta_sma50_pa&ft=4',
        'SPXT': 'https://finviz.com/screener.ashx?v=151&f=idx_sp500&ft=4',
        'SPXA': 'https://finviz.com/screener.ashx?v=151&f=idx_sp500,ta_sma50_pa&ft=4'
    }
    items_ = {}
    for k, v in urls_d.items():
        html = requests.get(v, headers=headers).text
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find('td', {"class": "count-text"}).text.strip('Total:  ')

        items_[k] = int(table[:-3])
    items_['NYSE Trending Stocks %'] = round(items_['NyseA'] * 100 / items_['NyseT'], 2)
    items_['NASDAQ Trending Stocks %'] = round(items_['NasdA'] * 100 / items_['NasdT'], 2)
    items_['SP500 Trending Stocks %'] = round(items_['SPXA'] * 100 / items_['SPXT'], 2)
    items_.pop('NyseT')
    items_.pop('NyseA')
    items_.pop('NasdT')
    items_.pop('NasdA')
    items_.pop('SPXT')
    items_.pop('SPXA')

    print(items_)
    with open(os.path.join('results', 'img_out', 'sma50.csv'), 'w+') as f:
        write = csv.DictWriter(f, items_.keys())
        # write.writerow(fields)
        write.writeheader()
        write.writerow(items_)
    print('sma50 complete')


# def get_etf_flows():
#     driver = firefox_init()
#     etfs = ['SPY', 'VTI', 'VEA', 'VWO', 'QQQ', 'VXX', 'TLT', 'SHY', 'LQD', 'VCIT']
#
#     with driver:
#         for etf in etfs:
#             img_path = os.path.join(IMAGES_OUT_PATH, f'inflows_{etf}' + '.png')
#             driver.get(f'https://etfdb.com/etf/{etf}/#fund-flows')
#             sleep(7)
#             driver.save_screenshot(img_path)
#             infl = os.path.join(IMAGES_OUT_PATH, f'inflows_{etf}' + '.png')
#             crop(infl, infl, 570, 390, 725, 350)
#     driver.quit()
#     print('get_etf_flows complete' + '\n')

# ============================== Inflows GET ================================


def get_flows():
    etfs = ['VCIT', 'SPY', 'VTI', 'VEA', 'VWO', 'QQQ', 'VXX', 'TLT', 'SHY', 'LQD']
    # etfs = ['QQQ', 'VTI', 'VXX']
    # display = Display(visible=0, size=(1920, 1080))
    # display.start()
    driver = firefox_init()
    with driver:
        driver.get('https://www.etf.com/etfanalytics/etf-fund-flows-tool')
        sleep(8)
        elem = driver.find_element_by_xpath(".//*[@id='edit-tickers']")
        elem.send_keys("GLD, SPY, VTI, VEA, VWO, QQQ, VXX, TLT, SHY, LQD, VCIT")
        sleep(0.7)
        today = date.today()
        day7 = timedelta(days=21)  # TODO Меняется ли размер окна от колва дней?
        delta = today - day7
        start_d = delta.strftime("%Y-%m-%d")
        end_d = today.strftime("%Y-%m-%d")
        elem = driver.find_element_by_xpath(".//*[@id='edit-startdate-datepicker-popup-0']")
        elem.send_keys(start_d)
        sleep(0.6)
        elem = driver.find_element_by_xpath(".//*[@id='edit-enddate-datepicker-popup-0']")
        elem.send_keys(end_d)
        sleep(0.5)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, ".//*[@id='edit-submitbutton']"))).click()
        # driver.find_element_by_xpath(".//*[@id='edit-submitbutton']").click()
        sleep(5)
        elem = driver.find_element_by_xpath(".//*[@id='fundFlowsTitles']")
        webdriver.ActionChains(driver).move_to_element(elem).perform()
        driver.execute_script("return arguments[0].scrollIntoView();", elem)
        sleep(1)

        for etf in etfs:  # TODO или надо скролить один раз перед запросом первого окна или скролить окно для каждого(сейчас для каждого)
            sleep(2)
            print(etf)
            tag = ".//*[@id=\'" + f'{etf}' + "_nf']"
            tag2 = ".//*[@id=\'container_" + f'{etf}' + "'" + "]"
            icon = driver.find_element_by_xpath(tag)  # ".//*[@id='{etf}_nf']"
            # driver.execute_script("return arguments[0].scrollIntoView();", icon)
            driver.execute_script("arguments[0].click();", icon)
            sleep(3)
            graph = driver.find_element_by_xpath(tag2)  # ".//*[@id='container_{etf}']"
            driver.execute_script("return arguments[0].scrollIntoView();", graph)
            sleep(1)
            driver.save_screenshot(os.path.join(IMAGES_OUT_PATH, f'inflows_{etf}.png'))
            img = Image.open(os.path.join(IMAGES_OUT_PATH, f'inflows_{etf}.png'))
            img_crop = img.crop((360, 367, 980, 650))
            img_crop.save(os.path.join(IMAGES_OUT_PATH, f'inflows_{etf}.png'), quality=100, subsampling=0)
    # display.stop()
    print('Get Fund Flows complete' + '\n')

# ============================== FINVIZ TREEMAP GET ================================


def get_finviz_us_treemaps(url_, filename):
    display = Display(visible=0, size=(1920, 1080))
    display.start()
    driver = firefox_init()
    with driver:  # TODO WARNING!
        img_path = os.path.join(IMAGES_OUT_PATH, filename + '.png')
        driver.get(url_)
        sleep(5)
        elem = driver.find_element_by_id('body')
        location = elem.location
        size = elem.size
        driver.save_screenshot(img_path)
        x = location['x']
        y = location['y']
        width = location['x'] + size['width']
        height = location['y'] + size['height']
        im = Image.open(img_path)
        im = im.crop((int(x), int(y), int(width)+20, int(height)+16))
        im.save(img_path)
    display.stop()
    print('Get Finviz Treemap complete' + '\n')


def get_finviz():
    get_finviz_us_treemaps('https://finviz.com/map.ashx?t=sec_all', 'treemap_1d')
    get_finviz_us_treemaps('https://finviz.com/map.ashx?t=sec_all&st=ytd', 'treemap_ytd')
    get_finviz_us_treemaps('https://finviz.com/map.ashx?t=geo', 'global_treemap')
    get_finviz_us_treemaps('https://finviz.com/map.ashx?t=geo&st=ytd', 'global_treemap_ytd')
# ============================== AI INDICES GET ================================


def get_features(ticker_list, filename, data_dir_, start_date_, end_date_):
    for ticker_ in ticker_list.keys():
        download_yahoo(ticker_, data_dir_, start_date_, end_date_)

    main_df = pd.DataFrame()
    for ticker_, w in ticker_list.items():
        df = load_csv(ticker_, data_dir_)
        df.drop(columns={'Dividend'}, axis=1, inplace=True)
        df['Open'] = w * df['Open']
        df['High'] = w * df['High']
        df['Low'] = w * df['Low']
        df['Close'] = w * df['Close']
        df['Volume'] = w * df['Volume']
        df.dropna(inplace=True)
        if len(main_df) == 0:
            main_df = df
        else:
            main_df['Open'] = main_df['Open'] + df['Open']
            main_df['High'] = main_df['High'] + df['High']
            main_df['Low'] = main_df['Low'] + df['Low']
            main_df['Close'] = main_df['Close'] + df['Close']
            main_df['Volume'] = main_df['Volume'] + df['Volume']
    main_df.dropna(inplace=True)
    main_df['Open'] = main_df['Open'] / 1000
    main_df['High'] = main_df['High'] / 1000
    main_df['Low'] = main_df['Low'] / 1000
    main_df['Close'] = main_df['Close'] / 1000
    main_df['Volume'] = main_df['Volume'] / 1000

    path = os.path.join(YAHOO_PATH, f'{filename}' + '.csv')
    main_df.to_csv(path, index_label='Date')


def get_mpl_charts(filename):
    daily = pd.read_csv(os.path.join(YAHOO_PATH, f'{filename}.csv'), index_col=0, parse_dates=True)
    end_date_ = datetime.utcnow()
    daily.index.name = 'Date'
    daily = daily.loc['2020-01-01':f'{end_date_}', :]

    mc = mpf.make_marketcolors(
        up='limegreen', down='red',
        edge='#e3e3e3',
        wick='white',
        volume='inherit',
    )
    my_style = mpf.make_mpf_style(base_mpf_style='nightclouds',
                                  marketcolors=mc,
                                  gridcolor='#404040',
                                  edgecolor='#404040',
                                  y_on_right=True)
    mpf.plot(daily,
             type='candle',
             style=my_style,
             volume=True,
             volume_panel=1,
             show_nontrading=False,
             title='\n' + f'{filename}',
             ylabel='Price ($)',
             ylabel_lower='Volume',
             panel_ratios=(7, 3),
             savefig=dict(fname=IMAGES_OUT_PATH + f'{filename}.png', dpi=300, pad_inches=1)
             )


def render_index(ticker_list, filename):
    get_features(ticker_list, filename, YAHOO_PATH, start_date, end_date)
    get_mpl_charts(filename)
    ai = os.path.join(IMAGES_OUT_PATH, f'{filename}.png')
    crop(ai, ai, 400, 200, 90, 100)


def get_indicies():
    US_INDEX = index_calc(filename='sorted_rsi_us_stocks_closes.csv',
                              qty=25, limit_1=12, limit_2=5, iterator=0.0018, qld_tmf=False)
    print('US Index reconstruction complete')
    WORLD_INDEX = index_calc(filename='sorted_rsi_world_stocks_closes.csv',
                                 qty=50, limit_1=7, limit_2=2, iterator=0.0008, qld_tmf=False)
    print('World Index reconstruction complete')
    render_index(US_INDEX, 'us_index')
    render_index(WORLD_INDEX, 'world_index')
    print('Indicies reconstruction complete!' + '\n')
# ============================== COIN360 TREEMAP GET ================================


def get_coins360_treemaps():
    display = Display(visible=0, size=(1920, 1080))
    display.start()
    url_ = 'https://coin360.com/?exceptions=[USDT%2CUSDC]&period=24h&range=[500000000%2C295729609429]'
    filename = 'coins_treemap'
    driver = firefox_init()
    with driver:  # TODO WARNING! ATTENTION!
        img_path = os.path.join(IMAGES_OUT_PATH, filename + '.png')
        driver.get(url_)
        sleep(10)
        elem = driver.find_element_by_id('app')
        location = elem.location
        size = elem.size
        driver.save_screenshot(img_path)
        x = location['x']
        y = location['y']
        width = location['x'] + size['width']
        height = location['y'] + size['height']
        im = Image.open(img_path)
        im = im.crop((int(x), int(y+80), int(width), int(height-25)))
        im.save(img_path)
        print('Get coin360 Treemap complete' + '\n')
    display.stop()


# ============================== Core Data GET ================================


def agent_rotation():
    ua = [
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

    ]
    return choice(ua)


def scrape_economics():
    headers = {'User-Agent': agent_rotation()}
    url_ = {
        'Interest Rate': 'https://tradingeconomics.com/country-list/interest-rate?continent=g20',
        'Inflation Rate': 'https://tradingeconomics.com/country-list/inflation-rate?continent=g20',
        'Unemployment Rate': 'https://tradingeconomics.com/country-list/unemployment-rate?continent=g20',
        'Composite PMI': 'https://tradingeconomics.com/country-list/composite-pmi?continent=g20'
    }
    items_ = []
    for k, v in url_.items():
        html = requests.get(v, headers=headers).text
        soup = BeautifulSoup(html, "html.parser")
        # identify table we want to scrape
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

    df = df.drop(df[(df.Country != 'Russia')
                    & (df.Country != 'China')
                    & (df.Country != 'United States')
                    & (df.Country != 'United Kingdom')
                    & (df.Country != 'Euro Area')
                    & (df.Country != 'France')
                    & (df.Country != 'Germany')
                    & (df.Country != 'Japan')].index)
    filename = os.path.join(YAHOO_PATH, 'economic_data.csv')
    df.to_csv(filename, index=False)


# ============================== Calls ================================
def main():
    # get_sma50()
    #
    # get_flows()  # From ETF.COM
    # reporter()
    # get_crypto()
    get_coins360_treemaps()
    tw_multi_render()
    advance_decline()
    # get_etf_flows()
    get_finviz()
    get_indicies()
    scrape_economics()
    #
    # schedule.every(10).minutes.do(reporter)
    # schedule.every(1440).minutes.do(get_crypto)
    # schedule.every(15).minutes.do(get_coins360_treemaps)
    # schedule.every(15).minutes.do(tw_multi_render)
    # schedule.every(60).minutes.do(advance_decline)
    # schedule.every(720).minutes.do(get_etf_flows)
    # schedule.every(15).minutes.do(get_finviz)
    # schedule.every(480).minutes.do(get_indicies)
    # schedule.every().monday.do(scrape_economics)

    while True:
        schedule.run_pending()
        sleep(5)


if __name__ == '__main__':
    print(f"Starting scrapers {os.path.realpath(__file__)}, this may take a while")
    main()
