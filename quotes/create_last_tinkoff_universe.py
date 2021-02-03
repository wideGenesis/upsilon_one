import json
import requests
import datetime
from project_shared import *
from quotes.quote_loader import *
from quotes.sql_queries import *
from quotes.get_tinkoff_universe import *
from quotes.eodhistoricaldata import *


def create_last_hist_tinkoff_universe():
    all_tinkoff_tickers = get_and_save_tinkoff_universe()
    current_tinkoff_universe = get_universe(table_name=TINKOFF_UNIVERSE_TABLE_NAME)
    cur_universe_date = date.today()
    prev_universe_date = date.today()
    td = timedelta(1)
    cur_universe_date = date(cur_universe_date.year, cur_universe_date.month, 1) - td
    universe_to_save = get_all_universe_by_date(cur_universe_date)
    global_universe = universe_to_save.copy()
    for ticker in global_universe:
        if ticker not in current_tinkoff_universe:
            universe_to_save.pop(ticker)

    need_update_prices = []
    if "WMT" not in universe_to_save and "WMT" in all_tinkoff_tickers:
        sector, mkt_cap, exchange = get_tickerdata("WMT")
        universe_to_save["WMT"] = (sector, mkt_cap, exchange)
        need_update_prices.append("WMT")
    if "NEE" not in universe_to_save and "NEE" in all_tinkoff_tickers:
        sector, mkt_cap, exchange = get_tickerdata("NEE")
        universe_to_save["NEE"] = (sector, mkt_cap, exchange)
        need_update_prices.append("NEE")
    if "XEL" not in universe_to_save and "XEL" in all_tinkoff_tickers:
        sector, mkt_cap, exchange = get_tickerdata("XEL")
        universe_to_save["XEL"] = (sector, mkt_cap, exchange)
        need_update_prices.append("XEL")

    # Заберем данные по вновь добавленным тикерам
    eod_update_universe_prices(need_update_prices)

    # Сохраним ткущую вселенную в БД
    save_universe(cur_universe_date, universe_to_save)
    debug(f"TU [{cur_universe_date.strftime('%Y-%m-%d')}]:[{len(universe_to_save)}] {universe_to_save}")


def save_universe(universe_date, universe):
    if not is_table_exist(TINKOFF_HIST_UNIVERSE_TABLE_NAME):
        create_hist_universe_table(TINKOFF_HIST_UNIVERSE_TABLE_NAME)
    append_universe_by_date(universe=universe,
                            universe_date=universe_date,
                            table_name=TINKOFF_HIST_UNIVERSE_TABLE_NAME)


if __name__ == '__main__':
    print(f"Starting create_nasdaq_hist_universe, this may take a 20 min")
    create_last_hist_tinkoff_universe()
