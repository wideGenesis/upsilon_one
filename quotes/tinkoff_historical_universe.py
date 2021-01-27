import json
from datetime import timedelta, date, datetime
from project_shared import *
from quotes.sql_queries import *
import pandas as pd


def create_tinkoff_historical_universe():
    current_tinkoff_universe = get_universe(table_name=TINKOFF_UNIVERSE_TABLE_NAME)
    final_date = datetime.date(2019, 12, 31)
    cur_universe_date = date.today()
    prev_universe_date = date.today()
    td = timedelta(1)
    if cur_universe_date.day > 1:
        cur_universe_date = date(cur_universe_date.year, cur_universe_date.month, 1) - td
        universe_to_save = get_all_universe_by_date(cur_universe_date)
        global_universe = universe_to_save.copy()
        for ticker in global_universe:
            if ticker not in current_tinkoff_universe:
                universe_to_save.pop(ticker)
        # Сохраним ткущую вселенную в БД
        save_universe(cur_universe_date, universe_to_save)
        debug(f"TU [{cur_universe_date.strftime('%Y-%m-%d')}]:[{len(universe_to_save)}] {universe_to_save}")

    # ++++ Основной цикл создания исторических вселенных
    while cur_universe_date >= final_date:
        prev_universe_date = cur_universe_date
        cur_universe_date = date(cur_universe_date.year, cur_universe_date.month, 1) - td
        universe_to_save = get_all_universe_by_date(cur_universe_date)
        global_universe = universe_to_save.copy()
        for ticker in global_universe:
            if ticker not in current_tinkoff_universe:
                universe_to_save.pop(ticker)
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
    create_tinkoff_historical_universe()
