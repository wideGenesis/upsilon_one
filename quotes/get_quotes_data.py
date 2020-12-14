import os
import sys
import yaml
import time
from datetime import datetime
from random import choice, randint
import pandas as pd
from pandas_datareader import data as pdr
import cmath
from yahoofinancials import YahooFinancials

from bs4 import BeautifulSoup
from finviz.screener import Screener
from finviz.main_func import *


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


conf = yaml.safe_load(open(os.path.abspath('config/settings.yaml')))
PYTHON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(PYTHON_PATH)
os.environ["PYTHONUNBUFFERED"] = "1"

YAHOO_PATH = conf['PATHS']['YAHOO_PATH']
COINS_DATA = conf['PATHS']['COINS_DATA']
HOLDINGS = conf['PATHS']['HOLDINGS']
LOGS = conf['PATHS']['LOGS']
WEBDRIVER = conf['PATHS']['WEBDRIVER']

ETF_FOR_SCRAPE = conf['ETF_FOR_SCRAPE']
WORLD_MEGA_CAPS = conf['WORLD_MEGA_CAPS']


def selenium_init(ua=None):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server=direct://")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument(f'user-agent={ua}')
    driver_path = os.path.join(WEBDRIVER, 'chromedriver_87')
    driver = webdriver.Chrome(driver_path, options=chrome_options)
    print(driver.execute_script("return navigator.userAgent"))
    return driver


def agent_rotation():
    ua = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

    ]
    return choice(ua)


def asset_download(asset_list, start_, end_, filename=None, session_=None, save_path=YAHOO_PATH):
    asset_df = pd.DataFrame([pdr.DataReader(ticker, 'yahoo', start_, end_, session=session_)['Close']
                             for ticker in asset_list]).T
    asset_df.columns = asset_list
    path = os.path.join(save_path, filename)
    asset_df.to_csv(path, index_label='Date')
    print('Assets Data download complete!')


# Не пустой ли объект?
def empty_check(n) -> bool:
    if type(n) == str:
        return n is not None and n != 0 and n != '0'
    else:
        return n is not None and n != 0 and not cmath.isnan(n)


# Округление числа и конвертация его во float
def number_to_float(n) -> float:
    if empty_check(n):
        return round(float(n), 2)
    else:
        return n


# Datetime to str
def dt_to_str(date: datetime) -> str:
    return "%04d-%02d-%02d" % (date.year, date.month, date.day)


# Словарь с ценами
def dic_with_prices(prices: dict, ticker: str, date: datetime, close):
    if date.weekday() > 5:
        print(f'Найден выходной в {ticker} на {date}')
        return
    close = number_to_float(close)
    error_price = (not empty_check(close))
    if error_price:
        print(f'В {ticker} на {date} имеются пустые данные')
        return
    prices[date] = [close]


# YahooFinancials
def download_yahoo_closes(ticker, start_date, end_date, path_to_save=None, adj_close=False):
    try:
        yf = YahooFinancials(ticker)
        data = yf.get_historical_price_data(dt_to_str(start_date), dt_to_str(end_date), 'daily')
    except Exception as e0:
        print(f'Unable to read data for {ticker}: {e0}')
        return 'unable read'

    if data.get(ticker) is None or data[ticker].get('prices') is None or \
            data[ticker].get('timeZone') is None or len(data[ticker]['prices']) == 0:
        print(f'Yahoo: no data for {ticker}')
        return 'no data'

    prices = {}
    for rec in sorted(data[ticker]['prices'], key=lambda r: r['date']):
        date = datetime.datetime.strptime(rec['formatted_date'], '%Y-%m-%d')
        dic_with_prices(prices, ticker, date, rec['close'])
    if adj_close:
        close = 'Adj Close'
    else:
        close = 'Close'
    frame = pd.DataFrame.from_dict(prices, orient='index', columns=[close])
    frame.to_csv(os.path.join(path_to_save, f'{ticker}.csv'), index_label='date')
    if path_to_save is None:
        print(ticker)
        print(frame.head(1))
        return frame
    else:
        print(ticker)
        print(frame.head(1))
        return frame


def get_yahoo_closes(asset_list, start_, end_, filename=None, save_path=YAHOO_PATH):
    asset_df = pd.DataFrame([download_yahoo_closes(ticker, start_, end_, path_to_save=save_path, adj_close=False)['Close'] for ticker in asset_list]).T
    asset_df.columns = asset_list
    new_df = asset_df.copy()
    new_df.dropna(axis=1, inplace=True)
    path = os.path.join(save_path, filename)
    new_df.to_csv(path, index_label='Date')
    print('Assets Data download complete!')


def resampler(path_=None, filename=None, adj_close=False, resample_to='M'):
    if adj_close:
        close = 'Adj Close'
    else:
        close = 'Close'
    logic = {'Open': 'first',
             'High': 'max',
             'Low': 'min',
             close: 'last',
             'Volume': 'sum'}

    offset = pd.offsets.timedelta(days=-6)  # TODO Days
    path = os.path.join(path_, filename)
    df = pd.read_csv(path_=path, filename=None, index_col='Date', parse_dates=True)
    df.resample(resample_to=resample_to, loffset=offset).apply(logic)
    return df


# ==========================================================Download ETFs Holdings======================================
def get_table(soup):
    for t in soup.select('table'):
        header = t.select('thead tr th')
        if len(header) > 2:
            if (header[0].get_text().strip() == 'Symbol'
                    and header[2].get_text().strip().startswith('% Holding')):
                return t
    raise Exception('could not find symbol list table')


def get_etf_holdings(etf_name=None):
    browser = selenium_init()
    url = 'https://www.barchart.com/stocks/quotes/{}/constituents?page=all'.format(etf_name)
    browser.get(url)
    time.sleep(5)
    WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.ID, "main-content-column")))
    try:
        html = browser.page_source
    except Exception as e:
        print(e, 'Waiting 5 sec')
        time.sleep(5)
        html = browser.page_source
    soup = BeautifulSoup(html, features="lxml")
    table = get_table(soup)
    asset_dict = {}
    for row in table.select('tr')[1:-1]:
        try:
            cells = row.select('td')
            symbol = cells[0].get_text().strip()
            # name = cells[1].text.strip()
            celltext = cells[2].get_text().strip()
            percent = float(celltext.rstrip('%'))
            # shares = int(cells[3].text.strip().replace(',', ''))
            if symbol != "" and percent > 1.0:
                asset_dict[symbol] = {
                    'symbol': symbol,
                    # 'name': name,
                    # 'percent': percent,
                    # 'shares': shares,
                }
        except BaseException as ex:
            print(ex)
    browser.quit()
    result = pd.DataFrame(asset_dict).T
    return result


def get_constituents(etfs_=None):
    df_all = pd.DataFrame()
    for etf in etfs_:
        holdings = get_etf_holdings(etf_name=etf)
        print(f'Holdings of {etf} has been downloaded!')
        df_all = df_all.append(holdings)
        df_all.drop_duplicates(keep='first', inplace=True)
    tick_1 = df_all['symbol'].tolist()
    tick_2 = WORLD_MEGA_CAPS

    data_1 = Screener(table='Custom', order='-marketcap', tickers=tick_1)
    data_1.to_csv(os.path.join(HOLDINGS, 'us_mega_caps.csv'))
    time.sleep(30)
    data_2 = Screener(table='Custom', order='-marketcap', tickers=tick_2)
    data_2.to_csv(os.path.join(HOLDINGS, 'world_mega_caps.csv'))
    print('US and World Mega Caps has been downloaded!')


def us_stock_filtration():
    path = os.path.join(HOLDINGS, 'us_mega_caps.csv')
    df = pd.read_csv(path, index_col='No.')
    df.drop(columns={'P/E', 'Price', 'Change', 'Volume'}, axis=1, inplace=True)
    df['Market Cap'] = df['Market Cap'].str.extract(r'(\d+.\d+)').astype(float)
    df = df[df['Market Cap'] > 20.0]
    df = df[df['Sector'] != 'Real Estate']
    df = df[df['Sector'] != 'Financial']
    df = df[df['Country'] == 'USA']
    df.reset_index(drop=True, inplace=True)
    ticker_list = df['Ticker'].tolist()
    df.to_csv(os.path.join(HOLDINGS, 'filtered_us_mega_caps.csv'))
    print('passed 1')
    return ticker_list


def momentum(filename=None):
    path = os.path.join(HOLDINGS, filename)
    data_df = pd.read_csv(path, index_col='Date', parse_dates=True)
    columns = data_df.columns.tolist()
    _mom = data_df.copy()
    for col in columns:
        symm1 = (data_df[col] - data_df[col].shift(21))/data_df[col].shift(21)
        symm3 = (data_df[col] - data_df[col].shift(63))/data_df[col].shift(63)
        zscore_m1 = (symm1 - symm1.rolling(252).mean())/symm1.rolling(252).std()
        zscore_m3 = (symm3 - symm3.rolling(252).mean())/symm3.rolling(252).std()
        _mom[col] = 0.5*zscore_m1 + 0.5*zscore_m3
    _mom.dropna(inplace=True)
    _mom.drop_duplicates(inplace=True)
    _mom.to_csv(os.path.join(HOLDINGS, 'mtum_' + filename))
    return _mom


def rsi(filename=None, n=21):
    path = os.path.join(HOLDINGS, filename)
    data_df = pd.read_csv(path, index_col='Date', parse_dates=True)
    columns = data_df.columns.tolist()
    _rsi = data_df.copy()
    for col in columns:
        delta = data_df[col].diff()
        delta = delta[1:]
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        roll_up1 = up.ewm(span=n).mean()
        roll_down1 = down.abs().ewm(span=n).mean()
        RS1 = roll_up1 / roll_down1
        RSI1 = 100.0 - (100.0 / (1.0 + RS1))
        _rsi[col] = RSI1
    _rsi.dropna(inplace=True)
    _rsi.drop_duplicates(inplace=True)
    _rsi.to_csv(os.path.join(HOLDINGS, 'rsi_' + filename))
    return _rsi


def get_market_cap(ticker):
    yf = YahooFinancials(ticker)
    data = yf.get_market_cap()
    return data


def impulse_cap_sorting(filename=None):
    df = pd.read_csv(os.path.join(HOLDINGS, filename), index_col='Date', parse_dates=True)
    columns = df.columns.tolist()
    mcap_mtum = df.copy()
    last = df.iloc[[-1]]
    for col in columns:
        cap_mom = 0.5*last[col] * 0.5*get_market_cap(col)
        print(col, '\n')
        mcap_mtum[col+'_cap_mom'] = cap_mom
        mcap_mtum.drop(columns={col}, axis=1, inplace=True)
    mcap_mtum.dropna(inplace=True)
    last_sorted = mcap_mtum.T.sort_values(mcap_mtum.last_valid_index(), ascending=False).T
    last_sorted.to_csv(os.path.join(HOLDINGS, 'sorted_' + filename))
    return last_sorted


def index_calc(filename=None, qty=25, limit_1=12, limit_2=5, iterator=0.0018, qld_tmf=False):
    xpath = os.path.join(HOLDINGS, filename)
    df = pd.read_csv(xpath)
    df = df.T
    df['Ticker'] = df.index
    split = df['Ticker'].str.split('_', n=1, expand=True)
    df['Ticker'] = split[0]
    df.drop(['Date'], inplace=True)
    df.set_index('Ticker', inplace=True)
    df['Market Cap'] = df[0]
    df.drop(columns=[0], axis=1, inplace=True)
    df.drop('GOOG', axis=0, inplace=True, errors='ignore')
    df['Port cap'] = df['Market Cap'].iloc[0:qty].sum(axis=0)
    df['Weight'] = df['Market Cap'] * 100 / df['Port cap']
    df.drop(df.index[qty:200], axis=0, inplace=True)
    df.sort_values('Weight', inplace=True, ascending=False)
    df.loc[df['Weight'] <= limit_1, 'Weight_Stage1'] = df['Weight']
    df.loc[df['Weight'] >= limit_1, 'Excess_from_Stage1'] = df['Weight'] - limit_1
    df.loc[df['Weight'] >= limit_1, 'Weight_Stage1'] = limit_1

    df['Exccess_SUM'] = df['Excess_from_Stage1'].iloc[0:qty].sum(axis=0)
    df['Final_Weight'] = df['Weight_Stage1']
    excess = df.iloc[1].Exccess_SUM  # TODO ЧТО И ЗАЧЕМ ЭТО?
    excc = int(round(excess))
    while excc > 0:
        excc = excc - 1
        for index, row in df.iterrows():
            df.loc[df['Final_Weight'] <= limit_2, 'Final_Weight'] = df['Final_Weight'] + iterator
    df['FINAL_SUM_CONTROL'] = df['Final_Weight'].iloc[0:qty].sum(axis=0)
    df['Final_Weight'] = df['Final_Weight'].astype(float).round(2)
    df.drop(columns=[
        'Market Cap',
        'Port cap',
        'Weight',
        'Weight_Stage1',
        'Excess_from_Stage1',
        'Exccess_SUM',

    ], axis=1, inplace=True)
    control_sum = df.iloc[1].FINAL_SUM_CONTROL
    w_qld_tmf = (100 - control_sum)
    print('Sum of weights is \n', df['FINAL_SUM_CONTROL'])
    df.drop(columns=['FINAL_SUM_CONTROL'], axis=1, inplace=True)
    dtemp = df.to_dict()
    d = dtemp['Final_Weight']
    if qld_tmf:
        d.update({'TMF': round(w_qld_tmf, 2)}) #, 'TQQQ': round(w_qld_tmf, 2)})
    else:
        pass
    print('Mom*Cap Weights is \n', d)
    path = os.path.join(HOLDINGS, 'weigths_' + filename)
    df.to_csv(path, index=False)
    return d


coins = ['BTC-USD', 'ETH-USD', 'XRP-USD', 'ADA-USD', 'EOS-USD']

def main():
    start = datetime.datetime(2019, 1, 1)
    end = datetime.datetime.utcnow()
    us = 'us_stocks_closes.csv'
    world = 'world_stocks_closes.csv'
    blend = ''
    us_rsi = 'rsi_us_stocks_closes.csv'
    world_rsi = 'rsi_world_stocks_closes.csv'
    us_mtum = 'mtum_us_stocks_closes.csv'
    world_mtum = 'mtum_world_stocks_closes.csv'

    # Generate us/world mega_caps.csv
    get_constituents(ETF_FOR_SCRAPE)
    print('get_constituents for US complete')

    # Generate us/world closes.csv
    get_yahoo_closes(us_stock_filtration(), start_=start, end_=end, filename=us, save_path=HOLDINGS)
    print('get_yahoo_closes for US complete')
    get_yahoo_closes(WORLD_MEGA_CAPS, start_=start, end_=end, filename=world, save_path=HOLDINGS)
    print('get_yahoo_closes for WORLD complete')

    # Generate rsi/mom csv
    rsi(us)
    momentum(us)
    print('Mom us complete')
    rsi(world)
    momentum(world)
    print('Mom world complete')

    #
    impulse_cap_sorting(filename=us_rsi)
    print('Selection us complete')
    impulse_cap_sorting(filename=world_rsi)
    print('Selection world complete')

    """ Функция вызывает из get_screens"""
    # index_calc(filename='sorted_us_stocks_closes.csv', qty=25, limit_1=12, limit_2=5, iterator=0.0018, qld_tmf=False)
    # print('US Index complete')
    # index_calc(filename='sorted_world_stocks_closes.csv', qty=50, limit_1=7, limit_2=2, iterator=0.00065, qld_tmf=False)
    # print('WORLD Index complete')

    # all_coins = 'all_coins.csv'
    # get_yahoo_closes(coins, start_=start, end_=end, filename=all_coins, save_path=COINS_DATA)
    print('get_yahoo_closes for US complete')


if __name__ == '__main__':
    print(f"Starting indicies reconstruction {os.path.realpath(__file__)}, this may take a while")
    main()


