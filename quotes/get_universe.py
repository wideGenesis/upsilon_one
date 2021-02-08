from time import sleep
import pandas as pd
from .sql_queries import *
from dataclasses import dataclass
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from quotes.eodhistoricaldata import *


def eod_get_and_save_holdings():
    debug("Start eod_get_and_save_holdings")
    constituents = get_all_etf_holdings()

    # ++++++++ Добавим во вселенную ETFs ++++++++
    for ticker in ETFs:
        constituents[ticker] = ("ETF", 0, "US")

    # ++++++++ положим все в базу ++++++++
    if is_table_exist(UNIVERSE_TABLE_NAME):
        eod_update_universe_table(constituents)
    else:
        create_universe_table()
        eod_insert_universe_data(constituents)
    debug("END eod_get_and_save_holdings")


def get_and_save_holdings(driver):
    universe = ConstituentsScraper(holdings_url=ETF_HOLDINGS_URL, etfs_list=ETF_FOR_SCRAPE)
    constituents = universe.get_etf_holdings(driver=driver)
    # print(constituents)
    if is_table_exist(UNIVERSE_TABLE_NAME):
        update_universe_table(constituents)
    else:
        create_universe_table()
        insert_universe_data(constituents)


def get_universe_from_db(table_name, engine):
    return get_universe(table_name, engine)


FMP_API_KEY = f'5d0aeca6a9e10d5c77140a33607d3872'


def get_last_nasdaq_events():
    debug("#Start get last nasdaq events")
    jsn = None
    session = requests.Session()
    url = f'https://financialmodelingprep.com/api/v3/historical/nasdaq_constituent'
    params = {'apikey': FMP_API_KEY}
    request_result = session.get(url, params=params)
    if request_result.status_code == requests.codes.ok:
        jsn = request_result.text
    else:
        debug(f"Can't get NASDAQ historical events", ERROR)
    return jsn


def create_max_universe_list():
    # Возьмем все событя добавления и выбытия акций из Насдака
    jsn = get_last_nasdaq_events()
    result_events = {}
    global_universe = ['WMT', 'NEE', 'XEL']
    if jsn is not None:
        hist_events = json.loads(jsn)
        for item in hist_events:
            upd = {}
            event_date = datetime.datetime.strptime(item['date'], "%Y-%m-%d").date()
            if item['removedTicker'] is not None and item['removedTicker'] != "":
                upd = {item['removedTicker']: 'Remove'}
                if item['removedTicker'] not in global_universe:
                    global_universe.append(item['removedTicker'])
            if item['addedSecurity'] is not None and item['addedSecurity'] != "":
                upd = {item['symbol']: 'Add'}
                if item['symbol'] not in global_universe:
                    global_universe.append(item['symbol'])
            if event_date in result_events:
                result_events[event_date].update(upd)
            else:
                result_events[event_date] = upd

    # ++++ Заберем текущие конституенты индекса NDX
    # Это и будет текущей вселенной
    curr_universe = get_index_constituent('NDX')

    # ++++ Все соберем в global_universe для того что бы по всем данным обновлять цены.
    for ticker in curr_universe.keys():
        if ticker not in global_universe:
            global_universe.append(ticker)

    # ++++ Заберем текущие конституенты всех нужных нам ETF
    debug("Start eod_get_and_save_holdings")
    constituents = get_all_etf_holdings()
    for ticker in constituents.keys():
        if ticker not in global_universe:
            global_universe.append(ticker)

    # ++++++++ Добавим ETFs ++++++++
    for ticker in ETFs:
        if ticker not in global_universe:
            global_universe.append(ticker)

    # ++++++++ Добавим VIX ++++++++
    if '^VIX' not in global_universe:
        global_universe.append('^VIX')

    # ++++++++ Перепроверим вообще все используемые тикеры ++++++++
    all_used_tickers = get_all_uniq_tickers()
    for ticker in all_used_tickers:
        if ticker not in global_universe:
            global_universe.append(ticker)

    return global_universe


@dataclass
class ConstituentsScraper:
    __slots__ = [
        'holdings_url',
        'bottom_percent',
        'etfs_list',
    ]

    def __init__(self,
                 holdings_url=None,
                 bottom_percent: float = 1.0,
                 etfs_list: list = None):
        self.holdings_url = holdings_url
        self.bottom_percent = bottom_percent
        self.etfs_list = etfs_list

    def get_table(self, soup):
        for t in soup.select('table'):
            header = t.select('thead tr th')
            if len(header) > 2:
                if (header[0].get_text().strip() == 'Symbol'
                        and header[2].get_text().strip().startswith('% Holding')):
                    return t
        raise Exception('could not find symbol list table')

    def get_etf_holdings(self, driver):
        df_all = pd.DataFrame()
        t_len = len(self.etfs_list)
        debug(str(self.etfs_list))
        print_progress_bar(0, t_len, prefix='Progress:', suffix='Complete', length=50)
        for count, etf in enumerate(self.etfs_list):
            # print(etf)
            url = self.holdings_url.format(etf)
            try:
                driver.get(url)
                sleep(5)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "main-content-column")))
                html = driver.page_source
            except Exception as e:
                print(e, 'Waiting 10 sec')
                driver.get(url)
                sleep(10)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "main-content-column")))
                html = driver.page_source
            soup = BeautifulSoup(html, features="lxml")
            table = self.get_table(soup)
            asset_dict = {}
            for row in table.select('tr')[1:-1]:
                try:
                    cells = row.select('td')
                    symbol = cells[0].get_text().strip()
                    # name = cells[1].text.strip()
                    celltext = cells[2].get_text().strip()
                    percent = float(celltext.rstrip('%'))
                    # shares = int(cells[3].text.strip().replace(',', ''))
                    if symbol != "" and percent > self.bottom_percent:
                        # print("Symbol:" + str(symbol))
                        asset_dict[symbol] = {
                            'symbol': symbol,
                            # 'name': name,
                            # 'percent': percent,
                            # 'shares': shares,
                        }
                except BaseException as ex:
                    print(ex)
            if etf == "ARKF":
                debug("asset_dict:" + str(asset_dict))
            result = pd.DataFrame(asset_dict).T
            df_all = df_all.append(result)
            df_all.drop_duplicates(keep='first', inplace=True)
            print_progress_bar(count, t_len, prefix='Progress:', suffix=f'Complete:{etf}', length=50)
        ticker_list = df_all['symbol'].tolist()
        debug(ticker_list)
        driver.quit()
        return ticker_list
