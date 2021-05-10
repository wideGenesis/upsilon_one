import pandas as pd

from quotes.yahoo_downloader import *
from datetime import date, timedelta
from quotes.sql_queries import *
from project_shared import *
from quotes.eodhistoricaldata import *
from yahooquery import Ticker


def update_universe_prices(exclude_sectors=EXCLUDE_SECTORS, not_exclude_tickers=NOT_EXCLUDE_TICKERS):
    tickers = get_universe()
    # ==================== Доформируем вселенную ====================
    #  Сначала забираем сектора компаний и их капитализацию для дальнейшей фильтрации
    #  И удалим из вселенной те акции сектора которых не подходят и эти сектора явно указаны в конфиге EXCLUDE_SECTORS
    #  При этом оставим те акции, тикеры которых явно указаны в конфиге NOT_EXCLUDE_TICKERS, даже если
    #  у них не подходящий сектор
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

    # ++++++++ Добавим во вселенную ETFs ++++++++
    for ticker in ETFs:
        ticker_data[ticker] = ("ETF", 0)

    # ++++++++ Проапдейтим вселенную
    set_universe_mkt_cap(ticker_data)

    # ==================== Теперь проапдейтим/закачаем данные по OHLC по всем тикерам вселенной
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


def update_universe_prices1(universe=None):
    tickers = []
    if universe is None:
        tickers = get_universe_for_update()
    else:
        tickers = universe
    t_len = len(tickers)

    # ==================== Теперь проапдейтим/закачаем данные по OHLC по всем тикерам вселенной
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
        if not is_debug_init():
            print_progress_bar(0, t_len, prefix='Progress:', suffix='Complete', length=50)
        for count, ticker in enumerate(tickers, start=1):
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
            if not is_debug_init():
                print_progress_bar(count, t_len, prefix='Progress:', suffix=f'Complete:{ticker}:[{count}:{t_len}]   ',
                                   length=50)
            else:
                debug(f'Complete:{ticker}:[{count}:{t_len}]')
    else:
        debug("__Table is not exists__")
        create_quotes_table()
        if not is_debug_init():
            print_progress_bar(0, t_len, prefix='Progress:', suffix='Complete', length=50)
        for count, ticker in enumerate(tickers, start=1):
            start_date = date.fromisoformat(DEFAULT_START_QUOTES_DATE)
            end_date = date.today()
            download_quotes_to_db(ticker, start_date, end_date, is_update)
            if not is_debug_init():
                print_progress_bar(count, t_len, prefix='Progress:', suffix=f'Complete:{ticker}:[{count}:{t_len}]   ',
                                   length=50)
            else:
                debug(f'Complete:{ticker}:[{count}:{t_len}]')
    debug("Complete update_universe_prices1")


def eod_update_universe_prices(universe=None):
    tickers = []
    if universe is None:
        tickers = get_universe_for_update()
    else:
        tickers = universe
    t_len = len(tickers)
    # ==================== Теперь проапдейтим/закачаем данные по OHLC по всем тикерам вселенной
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
        for count, ticker in enumerate(tickers, start=1):
            # print("### Try update ticker:" + str(ticker))
            if count > 0 and count % 15 == 0:
                sleep(3)
            if ticker_lookup(ticker):
                if (end_table_date - td) != today:
                    is_update = True
                    # print("(ticker exist) Start date:" + str(end_table_date) + "; End date:" + str(today))
                    get_historical_adjprices(ticker, end_table_date, today, is_update)
                # else:
                #     print("Nothing to update. The table is up to date.")
            else:
                # print("(ticker not exist) Start date:" + str(start_table_date) + "; End date:" + str(today))
                get_historical_adjprices(ticker, start_table_date, today, is_update)
            print_progress_bar(count, t_len, prefix='Progress:', suffix=f'Complete:{ticker}:[{count}:{t_len}]   ',
                               length=50)
    else:
        debug("__Table is not exists__")
        create_quotes_table()
        print_progress_bar(0, t_len, prefix='Progress:', suffix='Complete', length=50)
        for count, ticker in enumerate(tickers):
            if count > 0 and count % 15 == 0:
                sleep(3)
            start_date = date.fromisoformat(DEFAULT_START_QUOTES_DATE)
            end_date = date.today()
            get_historical_adjprices(ticker, start_date, end_date, is_update)
            print_progress_bar(count, t_len, prefix='Progress:', suffix=f'Complete:{ticker}:[{count}:{t_len}]   ',
                               length=50)
    debug("Complete eod_update_universe_prices")


def ohlc_data_updater(universe, is_update=False, sd=None, ed=None, table_name=QUOTE_TABLE_NAME):
    if not is_table_exist(table_name):
        debug("__Table is not exists__")
        debug(f"Try create table {table_name}")
        create_quotes_table(table_name)
    t_len = len(universe)
    end_date = date.today()
    if ed is not None:
        end_date = ed
    if not is_debug_init():
        print_progress_bar(0, t_len, prefix='Progress:', suffix='Complete', length=50)
    for count, ticker in enumerate(universe, start=1):
        start_date = datetime.datetime.strptime(DEFAULT_START_QUOTES_DATE, "%Y-%m-%d").date()
        if sd is not None:
            start_date = sd
        else:
            if ticker_lookup(ticker, table_name):
                start_date = find_max_date_by_ticker(ticker, table_name) + timedelta(days=1)
        if is_update:
            if ticker not in DELISTED_TICKERS and ticker not in RECENTLY_DELISTED:
                download_quotes_to_db(ticker, start_date, end_date, is_update, table_name)
        else:
            if ticker not in DELISTED_TICKERS:
                download_quotes_to_db(ticker, start_date, end_date, is_update, table_name)
            else:
                get_historical_adjprices(ticker, start_date, end_date, is_update, table_name)
        if not is_debug_init():
            print_progress_bar(count, t_len, prefix='Progress:', suffix=f'Complete:{ticker}:[{count}:{t_len}]   ',
                               length=50)
        else:
            debug(f'Complete:{ticker}:[{count}:{t_len}]')

    debug("Complete ohlc_data_updater")


def get_ohlc_data_by_ticker(tick, period="1y", interval="1d"):
    closes_df = pd.DataFrame()
    ticker = tick.upper()
    if ticker is None or len(ticker) == 0:
        debug(f'Ticker is none, or len = 0 -- [{ticker}]')
        return closes_df

    ticker_data = None
    try:
        ticker_data = Ticker(ticker)
    except Exception as e:
        debug(e, ERROR)
        debug(f"Can't get ticker data -- [{ticker}]")
        return closes_df
    df = ticker_data.history(period=period, interval=interval)
    closes_df = df.get("close") if df.get("close") is not None else pd.DataFrame()
    return closes_df


def main():
    td = timedelta(days=4)
    ed = date.today()
    sd = ed - td
    ohlc = get_ohlc_dict_by_port_id("parking", start_date=sd, end_date=ed)
    debug("OHLC:" + str(ohlc))
    exit()
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
