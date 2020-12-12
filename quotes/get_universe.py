from time import sleep
import pandas as pd
from dataclasses import dataclass
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC





@dataclass
class ConstituentsScraper:

    __slots__ = [
        'driver',
        'holdings_url',
        'bottom_percent',
        'etfs_list',
    ]

    def __init__(self,
                 driver=None,
                 holdings_url=None,
                 bottom_percent: float = 1.0,
                 etfs_list: list = None):
        self.driver = driver
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

    def get_etf_holdings(self, etf):
        print(etf)
        url = self.holdings_url.format(etf)
        print(url)
        with self.driver:
            self.driver.get(url)
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "main-content-column")))
            try:
                html = self.driver.page_source
            except Exception as e:
                print(e, 'Waiting 5 sec')
                sleep(5)
                html = self.driver.page_source
            soup = BeautifulSoup(html, features="lxml")
            print(soup.prettify())
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
                        asset_dict[symbol] = {
                            'symbol': symbol,
                            # 'name': name,
                            # 'percent': percent,
                            # 'shares': shares,
                        }
                except BaseException as ex:
                    print(ex)
            result = pd.DataFrame(asset_dict).T
        return result

    def etfs_scraper(self):
        df_all = pd.DataFrame()
        for etf in self.etfs_list:
            holdings = self.get_etf_holdings(etf)
            print(f'Holdings of {etf} has been downloaded!')
            df_all = df_all.append(holdings)
            df_all.drop_duplicates(keep='first', inplace=True)
        ticker_list = df_all['symbol'].tolist()
        print(ticker_list)
        return ticker_list


