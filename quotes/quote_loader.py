import os
import yaml
import logging
from quotes.yahoo_downloader import *
from datetime import date, timedelta
from sqlalchemy import create_engine
from alchemysession import AlchemySessionContainer
from quotes.sql_queries import *

# conf = yaml.safe_load(open(os.path.dirname(__file__)+'\\'+'../config/settings.yaml'))
conf = yaml.safe_load(open('/home/gene/projects/upsilon_one/config/settings.yaml'))

# ============================== SQL Connect ======================

SQL_DB_NAME = conf['SQL']['DB_NAME']
SQL_USER = conf['SQL']['DB_USER']
SQL_PASSWORD = conf['SQL']['DB_PASSWORD']
SQL_URI = 'mysql+pymysql://{}:{}@localhost/{}'.format(SQL_USER, SQL_PASSWORD, SQL_DB_NAME)

engine = create_engine(SQL_URI, pool_recycle=3600)
container = AlchemySessionContainer(engine=engine)
alchemy_session = container.new_session('default')

DEFAULT_START_QUOTES_DATE = SQL_USER = conf['SQL']['DEFAULT_START_QUOTES_DATE']
QUOTE_TABLE_NAME = conf['SQL_TABLE_NAMES']['QUOTE_TABLE_NAME']
UNIVERSE_TABLE_NAME = conf['SQL_TABLE_NAMES']['UNIVERSE_TABLE_NAME']
TICKERS = conf['ETF_FOR_SCRAPE']
TICKERS += conf['ETFs']


# ============================== Logging Setup ======================
# logging.basicConfig(
#     filemode='w',
#     filename=os.path.abspath('logs/quote_loader.log'),
#     format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
#     level=logging.DEBUG)
# logging.getLogger('telethon').setLevel(level=logging.DEBUG)

def update_universe_prices():
    tickers = get_universe(UNIVERSE_TABLE_NAME, engine)
    print("[update_universe_prices] TICKERS: " + str(tickers))
    # Проверяем есть ли таблица, если нет ее надо создать
    is_update = False
    if is_table_exist(QUOTE_TABLE_NAME, engine):
        print("## Table is exist")
        td = timedelta(days=1)
        # Таблица есть
        start_table_date = get_start_table_date(QUOTE_TABLE_NAME, engine)
        # если в таблице есть данные то должна быть хотябы одна стартовая дата
        # если стартовой даты нет, то таблица скорее всего пуста и тогда начинать закачку нужно с нуля
        if start_table_date is None:
            print("### start_table_date is None")
            start_table_date = date.fromisoformat(DEFAULT_START_QUOTES_DATE)

        # если в таблице есть данные то должна быть хотябы одна конечная дата
        # если конечной даты нет, то таблица скорее всего пуста и тогда начинать закачку нужно с нуля
        end_table_date = get_last_table_date(QUOTE_TABLE_NAME, engine)
        if end_table_date is None:
            print("### end_table_date is None")
            end_table_date = date.fromisoformat(DEFAULT_START_QUOTES_DATE)
        else:
            end_table_date = end_table_date + td

        today = date.today()
        # в самом  простом случае апдейтить таблицу надо с последней даты в таблице по сегодняшнюю
        for ticker in tickers:
            print("### Try update ticker:" + str(ticker))
            is_ticker_exist = ticker_lookup(ticker, QUOTE_TABLE_NAME, engine)
            if is_ticker_exist:
                if (end_table_date - td) != today:
                    is_update = True
                    print("(ticker exist) Start date:" + str(end_table_date) + "; End date:" + str(today))
                    download_quotes_to_db(ticker, end_table_date, today, QUOTE_TABLE_NAME, is_update, engine)
                else:
                    print("Nothing to update. The table is up to date.")
            else:
                print("(ticker not exist) Start date:" + str(start_table_date) + "; End date:" + str(today))
                download_quotes_to_db(ticker, start_table_date, today, QUOTE_TABLE_NAME, is_update, engine)
    else:
        print("__Table is not exists__")
        create_quotes_table(QUOTE_TABLE_NAME, engine)
        for ticker in tickers:
            print("Ticker:" + ticker)
            start_date = date.fromisoformat(DEFAULT_START_QUOTES_DATE)
            # end_date = date(2020, 1, 1)
            end_date = date.today()
            download_quotes_to_db(ticker, start_date, end_date, QUOTE_TABLE_NAME, is_update, engine)


def main():
    print("__Start main__")
    # Проверяем есть ли таблица, если нет ее надо создать
    is_update = False
    if is_table_exist(QUOTE_TABLE_NAME, engine):
        print("## Table is exist")
        td = timedelta(days=1)
        # Таблица есть
        start_table_date = get_start_table_date(QUOTE_TABLE_NAME, engine)
        # если в таблице есть данные то должна быть хотябы одна стартовая дата
        # если стартовой даты нет, то таблица скорее всего пуста и тогда начинать закачку нужно с нуля
        if start_table_date is None:
            print("### start_table_date is None")
            start_table_date = date.fromisoformat(DEFAULT_START_QUOTES_DATE)

        # если в таблице есть данные то должна быть хотябы одна конечная дата
        # если конечной даты нет, то таблица скорее всего пуста и тогда начинать закачку нужно с нуля
        end_table_date = get_last_table_date(QUOTE_TABLE_NAME, engine)
        if end_table_date is None:
            print("### end_table_date is None")
            end_table_date = date.fromisoformat(DEFAULT_START_QUOTES_DATE)
        else:
            end_table_date = end_table_date + td

        today = date.today()
        # в самом  простом случае апдейтить таблицу надо с последней даты в таблице по сегодняшнюю
        for ticker in TICKERS:
            print("### Try update ticker:" + ticker)
            is_ticker_exist = ticker_lookup(ticker, QUOTE_TABLE_NAME, engine)
            if is_ticker_exist:
                if (end_table_date - td) != today:
                    is_update = True
                    print("(ticker exist) Start date:" + str(end_table_date) + "; End date:" + str(today))
                    download_quotes_to_db(ticker, end_table_date, today, QUOTE_TABLE_NAME, is_update, engine)
                else:
                    print("Nothing to update. The table is up to date.")
            else:
                print("(ticker not exist) Start date:" + str(start_table_date) + "; End date:" + str(today))
                download_quotes_to_db(ticker, start_table_date, today, QUOTE_TABLE_NAME, is_update, engine)
    else:
        print("__Table is not exists__")
        create_quotes_table(QUOTE_TABLE_NAME, engine)
        for ticker in TICKERS:
            print("Ticker:" + ticker)
            start_date = date.fromisoformat(DEFAULT_START_QUOTES_DATE)
            # end_date = date(2020, 1, 1)
            end_date = date.today()
            download_quotes_to_db(ticker, start_date, end_date, QUOTE_TABLE_NAME, is_update, engine)


if __name__ == '__main__':
    print("*********** Start ***********")
    main()
