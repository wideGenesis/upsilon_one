from quotes.yahoo_downloader import *
from datetime import date, timedelta
from quotes.sql_queries import *
from project_shared import *


def update_universe_prices(exclude_sectors=EXCLUDE_SECTORS, not_exclude_tickers=NOT_EXCLUDE_TICKERS):
    tickers = get_universe()
    debug(f'Tickers: {str(tickers)}')
    ticker_data = {}
    debug("#Try get market caps")
    t_len = len(tickers)
    print_progress_bar(0, t_len, prefix='Progress:', suffix='Complete', length=50)
    for count, ticker in enumerate(tickers):
        mkt_cap, sector = get_sector_and_market_cap(ticker)
        c_str = f'[{ticker}:{sector}]'
        if (sector not in exclude_sectors and sector is not None) or ticker in not_exclude_tickers:
            ticker_data[ticker] = (sector, mkt_cap)
        else:
            delete_from_universe(ticker)
        print_progress_bar(count, t_len, prefix='Progress:', suffix=f'Complete:{c_str}', length=50)
        # print(f'cap[{ticker}]={str(cap)}')
    debug("#Update market cap in db")
    set_universe_mkt_cap(ticker_data)
    debug("TICKERS: " + str(tickers))
    # Проверяем есть ли таблица, если нет ее надо создать
    is_update = False
    if is_table_exist(QUOTE_TABLE_NAME):
        debug("## Table is exist")
        td = timedelta(days=1)
        # Таблица есть
        start_table_date = get_start_table_date()
        # если в таблице есть данные то должна быть хотябы одна стартовая дата
        # если стартовой даты нет, то таблица скорее всего пуста и тогда начинать закачку нужно с нуля
        if start_table_date is None:
            debug("### start_table_date is None")
            start_table_date = date.fromisoformat(DEFAULT_START_QUOTES_DATE)

        # если в таблице есть данные то должна быть хотябы одна конечная дата
        # если конечной даты нет, то таблица скорее всего пуста и тогда начинать закачку нужно с нуля
        end_table_date = get_last_table_date()
        if end_table_date is None:
            debug("### end_table_date is None")
            end_table_date = date.fromisoformat(DEFAULT_START_QUOTES_DATE)
        else:
            end_table_date = end_table_date + td

        today = date.today()
        # в самом  простом случае апдейтить таблицу надо с последней даты в таблице по сегодняшнюю
        print_progress_bar(0, t_len, prefix='Progress:', suffix='Complete', length=50)
        for count, ticker in enumerate(ticker_data):
            # print("### Try update ticker:" + str(ticker))
            if ticker_lookup(ticker):
                if (end_table_date - td) != today:
                    is_update = True
                    # print("(ticker exist) Start date:" + str(end_table_date) + "; End date:" + str(today))
                    download_quotes_to_db(ticker, end_table_date, today, is_update)
                # else:
                #     print("Nothing to update. The table is up to date.")
            else:
                # print("(ticker not exist) Start date:" + str(start_table_date) + "; End date:" + str(today))
                download_quotes_to_db(ticker, start_table_date, today, is_update)
            print_progress_bar(count, t_len, prefix='Progress:', suffix=f'Complete:{ticker}', length=50)
    else:
        debug("__Table is not exists__")
        create_quotes_table()
        print_progress_bar(0, t_len, prefix='Progress:', suffix='Complete', length=50)
        for count, ticker in enumerate(ticker_data):
            start_date = date.fromisoformat(DEFAULT_START_QUOTES_DATE)
            end_date = date.today()
            download_quotes_to_db(ticker, start_date, end_date, is_update)
            print_progress_bar(count, t_len, prefix='Progress:', suffix=f'Complete:{ticker}', length=50)


def main():
    print("__Start main__")
    tickers = get_universe(UNIVERSE_TABLE_NAME, engine)
    # Проверяем есть ли таблица, если нет ее надо создать
    is_update = False
    if is_table_exist(QUOTE_TABLE_NAME):
        print("## Table is exist")
        td = timedelta(days=1)
        # Таблица есть
        start_table_date = get_start_table_date()
        # если в таблице есть данные то должна быть хотябы одна стартовая дата
        # если стартовой даты нет, то таблица скорее всего пуста и тогда начинать закачку нужно с нуля
        if start_table_date is None:
            print("### start_table_date is None")
            start_table_date = date.fromisoformat(DEFAULT_START_QUOTES_DATE)

        # если в таблице есть данные то должна быть хотябы одна конечная дата
        # если конечной даты нет, то таблица скорее всего пуста и тогда начинать закачку нужно с нуля
        end_table_date = get_last_table_date()
        if end_table_date is None:
            print("### end_table_date is None")
            end_table_date = date.fromisoformat(DEFAULT_START_QUOTES_DATE)
        else:
            end_table_date = end_table_date + td

        today = date.today()
        # в самом  простом случае апдейтить таблицу надо с последней даты в таблице по сегодняшнюю
        for ticker in tickers:
            print("### Try update ticker:" + ticker)
            is_ticker_exist = ticker_lookup(ticker)
            if is_ticker_exist:
                if (end_table_date - td) != today:
                    is_update = True
                    print("(ticker exist) Start date:" + str(end_table_date) + "; End date:" + str(today))
                    download_quotes_to_db(ticker, end_table_date, today, is_update)
                else:
                    print("Nothing to update. The table is up to date.")
            else:
                print("(ticker not exist) Start date:" + str(start_table_date) + "; End date:" + str(today))
                download_quotes_to_db(ticker, start_table_date, today, is_update)
    else:
        print("__Table is not exists__")
        create_quotes_table()
        for ticker in tickers:
            print("Ticker:" + ticker)
            start_date = date.fromisoformat(DEFAULT_START_QUOTES_DATE)
            # end_date = date(2020, 1, 1)
            end_date = date.today()
            download_quotes_to_db(ticker, start_date, end_date, is_update)


if __name__ == '__main__':
    print("*********** Start ***********")
    main()
