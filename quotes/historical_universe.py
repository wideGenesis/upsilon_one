import json
from datetime import timedelta, date, datetime
from project_shared import *
from quotes.sql_queries import *
from quotes.quote_loader import *
from quotes.eodhistoricaldata import *
import simfin as sf
from simfin.names import *
import pandas as pd


def create_nasdaq_hist_universe():
    # ++++ Подгрузим исторические события - когда добавлялись тикеры, а когда удалялись
    # переформатируем насвой лад - нужно что бы дата была ключем
    with open('nasdaq_100_historical_events.json') as json_file:
        hist_events = json.load(json_file)
    result_events = {}
    global_universe = []
    for item in hist_events:
        upd = {}
        event_date = datetime.datetime.strptime(item['date'], "%Y-%m-%d").date()
        if item['removedTicker'] is not None and item['removedTicker'] != "":
            upd = {item['removedTicker']: 'Remove'}
            global_universe.append(item['removedTicker'])
        if item['addedSecurity'] is not None and item['addedSecurity'] != "":
            upd = {item['symbol']: 'Add'}
            global_universe.append(item['symbol'])
        if event_date in result_events:
            result_events[event_date].update(upd)
        else:
            result_events[event_date] = upd

    # for key, value in result_events.items():
    # debug(f"Date[{key.strftime('%Y-%m-%d')}]: {value}")

    # ++++ Заберем текущие конституенты индекса NDX
    # Это и будет текущей вселенной
    curr_universe = get_index_constituent('NDX')

    # debug(f"len(curr_universe)={len(curr_universe)}")
    # debug(f"curr_universe:{curr_universe}")

    # ++++ Все соберем в global_universe для того что бы по всем данным обновлять цены.
    for ticker in curr_universe.keys():
        if ticker not in global_universe:
            global_universe.append(ticker)

    # debug(f"len(global_universe)={len(global_universe)}")
    # debug(f"global_universe:{global_universe}")

    # ++++ Обновляем цены по всем тикерам из global_universe
    eod_update_universe_prices(global_universe)

    # ++++ Подгружаем данные SimFin для поиска исторических маркет капов
    sf.set_api_key('free')
    sf.set_data_dir(SIMFIN_PATH)
    df_all = sf.load_shareprices(variant='daily', market='us')

    # ++++ Далее идут основные расчеты  ++++++++++++++
    # для начала подготовим стартовые даты и все такое
    # потом если сегодня не первое число месяца, то расчитаем вселенную для текущего месяца
    final_date = datetime.datetime.strptime(DEFAULT_START_QUOTES_DATE, "%Y-%m-%d").date()
    # debug(f"Final Date[{final_date.strftime('%Y-%m-%d')}]")
    cur_universe_date = date.today()
    prev_universe_date = date.today()
    td = timedelta(1)
    if cur_universe_date.day > 1:
        cur_universe_date = date(cur_universe_date.year, cur_universe_date.month, 1) - td
        # debug(f'Current universe date: {cur_universe_date.strftime("%Y-%m-%d")}')
        for ev_date, event in result_events.items():
            if cur_universe_date <= ev_date < prev_universe_date:
                for ticker, cmd in event.items():
                    if cmd == 'Remove':
                        sector, mkt_cap, exchange = get_tickerdata(ticker)
                        if (((sector not in EXCLUDE_SECTORS and sector is not None)
                             or ticker in NOT_EXCLUDE_TICKERS)
                                and ticker not in EXCLUDE_TICKERS and exchange in VALID_EXCHANGE):
                            # debug(f"Add ticker: {ticker}")
                            curr_universe[ticker] = (sector, mkt_cap, exchange)
                    if cmd == "Add":
                        if ticker in curr_universe:
                            # debug(f"Remove ticker: {ticker}")
                            curr_universe.pop(ticker)
    # Добавим во вселенную тикеры из исключенных секторов MA, V, PYPL
    sector, mkt_cap, exchange = get_tickerdata("MA")
    curr_universe["MA"] = (sector, mkt_cap, exchange)
    sector, mkt_cap, exchange = get_tickerdata("V`")
    curr_universe["V"] = (sector, mkt_cap, exchange)
    sector, mkt_cap, exchange = get_tickerdata("PYPL")
    curr_universe["PYPL"] = (sector, mkt_cap, exchange)
    # Проверка на достаточность данных в тикерах
    # Данных должно быть за 12 месяцев до текущей даты вселенной cur_universe_date
    checked_universe = check_enough_data(curr_universe, cur_universe_date, is_last=True)

    # ++++ Взять все исторические маркет капы
    universe_to_save = {}
    for ticker, value in checked_universe.items():
        hist_mkt_cap = find_mktcap(df_all, cur_universe_date, ticker, value[1])
        new_value = (value[0], hist_mkt_cap, value[2])
        universe_to_save[ticker] = new_value

    # Сохраним ткущую вселенную в БД
    save_universe(cur_universe_date, universe_to_save)

    debug(f"Universe for date [{cur_universe_date.strftime('%Y-%m-%d')}]: {universe_to_save}")

    # ++++ Основной цикл создания исторических вселенных
    while cur_universe_date >= final_date:
        prev_universe_date = cur_universe_date
        cur_universe_date = date(cur_universe_date.year, cur_universe_date.month, 1) - td
        # debug(f'Current universe date: {cur_universe_date.strftime("%Y-%m-%d")}')
        for ev_date, event in result_events.items():
            if cur_universe_date <= ev_date < prev_universe_date:
                for ticker, cmd in event.items():
                    if cmd == 'Remove':
                        sector, mkt_cap, exchange = get_tickerdata(ticker)
                        if (((sector not in EXCLUDE_SECTORS and sector is not None)
                             or ticker in NOT_EXCLUDE_TICKERS)
                                and ticker not in EXCLUDE_TICKERS and exchange in VALID_EXCHANGE):
                            # debug(f"Add ticker: {ticker}")
                            curr_universe[ticker] = (sector, mkt_cap, exchange)
                    if cmd == "Add":
                        if ticker in curr_universe:
                            # debug(f"Remove ticker: {ticker}")
                            curr_universe.pop(ticker)

        # Добавим во вселенную тикеры из исключенных секторов MA, V, PYPL
        sector, mkt_cap, exchange = get_tickerdata("MA")
        curr_universe["MA"] = (sector, mkt_cap, exchange)
        sector, mkt_cap, exchange = get_tickerdata("V`")
        curr_universe["V"] = (sector, mkt_cap, exchange)
        sector, mkt_cap, exchange = get_tickerdata("PYPL")
        curr_universe["PYPL"] = (sector, mkt_cap, exchange)
        # Проверка на достаточность данных в тикерах
        # Данных должно быть за 12 месяцев до текущей даты вселенной cur_universe_date
        checked_universe = check_enough_data(curr_universe, cur_universe_date)

        if cur_universe_date.year == 2018 and cur_universe_date.month == 6:
            checked_universe.pop('KDP')

        # ++++ Взять все исторические маркет капы
        universe_to_save = {}
        for ticker, value in checked_universe.items():
            hist_mkt_cap = find_mktcap(df_all, cur_universe_date, ticker, value[1])
            new_value = (value[0], hist_mkt_cap, value[2])
            universe_to_save[ticker] = new_value

        # Сохраним ткущую вселенную в БД
        save_universe(cur_universe_date, universe_to_save)

        debug(f"Universe for date [{cur_universe_date.strftime('%Y-%m-%d')}]: {universe_to_save}")


def check_enough_data(universe, universe_data, is_last=False):
    check_data_min = add_months(universe_data, -12)
    if is_last:
        td = timedelta(days=7)
        check_data_max = universe_data - td
    else:
        check_data_max = add_months(universe_data, 1)
    res_universe = universe.copy()
    for item in universe.items():
        min_ticker_date = find_min_date_by_ticker(item[0])
        max_ticker_date = find_max_date_by_ticker(item[0])
        # debug(f"{item[0]}: {str(min_ticker_date)}")
        if min_ticker_date is not None and max_ticker_date is not None:
            if min_ticker_date > check_data_min or max_ticker_date < check_data_max:
                res_universe.pop(item[0])
        else:
            res_universe.pop(item[0])
    return res_universe


def chck_data(universe):
    ticker_list = []
    for ticker in universe:
        min_ticker_date = find_min_date_by_ticker(ticker)
        max_ticker_date = find_max_date_by_ticker(ticker)
        # debug(f"{ticker}: {str(min_ticker_date)} - {str(max_ticker_date)}")
        if min_ticker_date is None or max_ticker_date is None:
            ticker_list.append(ticker)
    # debug(f"len={len(ticker_list)}")


def find_mktcap(df_all, universe_date, ticker, cur_mkt_cap):
    # debug(f"Find market cap for {ticker}")
    indx = df_all.index
    is_in = indx.isin([ticker], level='Ticker').any()
    if not is_in:
        # debug("Ticker not found")
        return cur_mkt_cap
    df_cap = df_all.loc[ticker, [CLOSE, SHARES_OUTSTANDING]]
    df_cap = df_cap.dropna()
    dates = df_cap.index
    min_date = dates[0]
    max_date = dates[-1]
    ud = pd.to_datetime(universe_date)
    mkt_cap = 0
    if ud in dates:
        dbyd = df_cap.loc[ud]
        close = dbyd[CLOSE]
        so = dbyd[SHARES_OUTSTANDING]
        mkt_cap = close * so
        # debug(f"{ticker} : Market Cap={mkt_cap}")
    elif ud < min_date:
        dbyd = df_cap.loc[min_date]
        close = dbyd[CLOSE]
        so = dbyd[SHARES_OUTSTANDING]
        mkt_cap = close * so
        # debug(f"{ticker} : Market Cap={mkt_cap}")
    elif min_date <= ud <= max_date:
        dbyd = df_cap.loc[ud:]
        ud = dbyd.index[0]
        dbyd = df_cap.loc[ud]
        close = dbyd[CLOSE]
        so = dbyd[SHARES_OUTSTANDING]
        mkt_cap = close * so
        # debug(f"{ticker} : Market Cap={mkt_cap}")
    elif ud > max_date:
        mkt_cap = cur_mkt_cap
    return mkt_cap


def save_universe(universe_date, universe):
    if not is_table_exist(HIST_UNIVERSE_TABLE_NAME):
        create_hist_universe_table(HIST_UNIVERSE_TABLE_NAME)
    append_universe_by_date(universe, universe_date)


if __name__ == '__main__':
    print(f"Starting create_nasdaq_hist_universe, this may take a 20 min")
    create_nasdaq_hist_universe()
