import json
from datetime import timedelta, date, datetime
from project_shared import *
from quotes.sql_queries import *
from time import sleep
from quotes.eodhistoricaldata import *


def create_nasdaq_hist_universe():
    # ++++ Подгрузим исторические события - когда добавлялись тикеры, а когда удалялись
    # переформатируем насвой лад - нужно что бы дата была ключем
    with open('nasdaq_100_histirical_events.json') as json_file:
        hist_events = json.load(json_file)
    result_events = {}
    for item in hist_events:
        upd = {}
        event_date = datetime.datetime.strptime(item['date'], "%Y-%m-%d").date()
        if item['removedTicker'] is not None and item['removedTicker'] != "":
            upd = {item['removedTicker']: 'Remove'}
        if item['addedSecurity'] is not None and item['addedSecurity'] != "":
            upd = {item['symbol']: 'Add'}
        if event_date in result_events:
            result_events[event_date].update(upd)
        else:
            result_events[event_date] = upd

    for key, value in result_events.items():
        debug(f"Date[{key.strftime('%Y-%m-%d')}]: {value}")

    # ++++ Заберем текущие конституенты
    curr_universe = get_index_constituent('NDX')

    # ++++ Основной цикл создания исторических вселенных
    final_date = list(result_events.keys())[-1]
    debug(f"Final Date[{final_date.strftime('%Y-%m-%d')}]")
    cur_universe_date = date.today()
    prev_universe_date = date.today()
    td = timedelta(1)
    if cur_universe_date.day > 1:
        cur_universe_date = date(cur_universe_date.year, cur_universe_date.month, 1) - td
        debug(f'Current universe date: {cur_universe_date.strftime("%Y-%m-%d")}')
        for ev_date, event in result_events.items():
            if cur_universe_date <= ev_date < prev_universe_date:
                for ticker, cmd in event.items():
                    if cmd == 'Remove':
                        sector, mkt_cap, exchange = get_tickerdata(ticker)
                        if (((sector not in EXCLUDE_SECTORS and sector is not None)
                             or ticker in NOT_EXCLUDE_TICKERS)
                                and ticker not in EXCLUDE_TICKERS and exchange in VALID_EXCHANGE):
                            debug(f"Add ticker: {ticker}")
                            curr_universe[ticker] = (sector, mkt_cap, exchange)
                    if cmd == "Add":
                        if ticker in curr_universe:
                            debug(f"Remove ticker: {ticker}")
                            curr_universe.pop(ticker)
                result_events.pop(ev_date)

    debug(f"Current universe: {curr_universe}")

    while cur_universe_date >= final_date:
        prev_universe_date = cur_universe_date
        cur_universe_date = date(cur_universe_date.year, cur_universe_date.month, 1) - td
        debug(f'Current universe date: {cur_universe_date.strftime("%Y-%m-%d")}')
        for ev_date, event in result_events.items():
            if cur_universe_date <= ev_date < prev_universe_date:
                for ticker, cmd in event.items():
                    if cmd == 'Remove':
                        sector, mkt_cap, exchange = get_tickerdata(ticker)
                        if (((sector not in EXCLUDE_SECTORS and sector is not None)
                             or ticker in NOT_EXCLUDE_TICKERS)
                                and ticker not in EXCLUDE_TICKERS and exchange in VALID_EXCHANGE):
                            debug(f"Add ticker: {ticker}")
                            curr_universe[ticker] = (sector, mkt_cap, exchange)
                    if cmd == "Add":
                        if ticker in curr_universe:
                            debug(f"Remove ticker: {ticker}")
                            curr_universe.pop(ticker)
        debug(f"Current universe: {curr_universe}")


if __name__ == '__main__':
    print(f"Starting scrapers {os.path.realpath(__file__)}, this may take a while")
    create_nasdaq_hist_universe()

