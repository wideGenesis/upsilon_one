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
    constituents = get_all_etf_holdings()

    # ++++++++ Добавим во вселенную ETFs ++++++++
    for ticker in ETFs:
        constituents[ticker] = ("ETF", 0)

    # ++++++++ положим все в базу ++++++++
    if is_table_exist(UNIVERSE_TABLE_NAME):
        eod_update_universe_table(constituents)
    else:
        create_universe_table()
        eod_insert_universe_data(constituents)


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
            result = pd.DataFrame(asset_dict).T
            df_all = df_all.append(result)
            df_all.drop_duplicates(keep='first', inplace=True)
            print_progress_bar(count, t_len, prefix='Progress:', suffix=f'Complete:{etf}', length=50)
        ticker_list = df_all['symbol'].tolist()
        debug(ticker_list)
        driver.quit()
        return ticker_list
