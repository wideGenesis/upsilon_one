import json
from datetime import timedelta, date, datetime
from project_shared import *
from quotes.sql_queries import *
from quotes.quote_loader import *
from quotes.eodhistoricaldata import *
import simfin as sf
from simfin.names import *
import pandas as pd

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
        debug(f"Can't get NASDAQ historical events")
    return jsn


def check_enough_data(universe, universe_data, is_last=False):
    check_data_min = add_months(universe_data, -12)
    td = timedelta(days=7)
    if is_last:
        check_data_max = universe_data - td
    else:
        check_data_max = add_months(universe_data, 1)
        check_data_max -= td
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


def save_universe(universe_date, universe):
    if not is_table_exist(HIST_UNIVERSE_TABLE_NAME):
        create_hist_universe_table(HIST_UNIVERSE_TABLE_NAME)
    append_universe_by_date(universe, universe_date)


def create_last_hist_universe(need_update_data=True):
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

    # ++++ Обновляем цены по всем тикерам из global_universe
    if need_update_data:
        ohlc_data_updater(global_universe, True)

    cur_universe_date = date.today()
    prev_universe_date = date.today()
    td = timedelta(1)
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
    need_update_prices = []
    if "MA" not in curr_universe:
        sector, mkt_cap, exchange = get_tickerdata("MA")
        curr_universe["MA"] = (sector, mkt_cap, exchange)
        need_update_prices.append("MA")
    if "V" not in curr_universe:
        sector, mkt_cap, exchange = get_tickerdata("V")
        curr_universe["V"] = (sector, mkt_cap, exchange)
        need_update_prices.append("V")
    if "PYPL" not in curr_universe:
        sector, mkt_cap, exchange = get_tickerdata("PYPL")
        curr_universe["PYPL"] = (sector, mkt_cap, exchange)
        need_update_prices.append("PYPL")
    if "WMT" not in curr_universe:
        sector, mkt_cap, exchange = get_tickerdata("WMT")
        curr_universe["WMT"] = (sector, mkt_cap, exchange)
        need_update_prices.append("WMT")
    if "NEE" not in curr_universe:
        sector, mkt_cap, exchange = get_tickerdata("NEE")
        curr_universe["NEE"] = (sector, mkt_cap, exchange)
        need_update_prices.append("NEE")
    if "XEL" not in curr_universe:
        sector, mkt_cap, exchange = get_tickerdata("XEL")
        curr_universe["XEL"] = (sector, mkt_cap, exchange)
        need_update_prices.append("XEL")

    # Заберем данные по вновь добавленным тикерам
    ohlc_data_updater(global_universe, True)

    # Проверка на достаточность данных в тикерах
    # Данных должно быть за 12 месяцев до текущей даты вселенной cur_universe_date
    checked_universe = check_enough_data(curr_universe, cur_universe_date, is_last=True)

    # Сохраним ткущую вселенную в БД
    save_universe(cur_universe_date, checked_universe)

    debug(f"Universe for date [{cur_universe_date.strftime('%Y-%m-%d')}]: {checked_universe}")


if __name__ == '__main__':
    print(f"Starting create_nasdaq_hist_universe, this may take a 20 min")
    create_last_hist_universe()
