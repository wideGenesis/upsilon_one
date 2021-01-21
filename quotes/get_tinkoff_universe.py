import json
import requests
import datetime
from project_shared import *
from quotes.sql_queries import *

TOKEN = 't.TuzfyQk5bMfqGQdKuOPUDo9QPuRuUJEjQuc6uKEqrYBfHAK1X_8gIHgpWf_ZlohqTjzPb8IYGrgpGrJjz66eQw'


def get_and_save_tinkoff_universe():
    with requests.Session() as session:
        url = f'https://api-invest.tinkoff.ru/openapi/market/stocks'
        headers = {'accept': 'application/json', 'Authorization': f'Bearer {TOKEN}'}
        request_result = session.get(url, headers=headers)
        if request_result.status_code == requests.codes.ok:
            res = {}
            parsed_json = json.loads(request_result.text)
            universe = get_all_universe()
            count = 0
            for inst in parsed_json['payload']['instruments']:
                if inst['currency'] == 'USD' and inst['ticker'] in universe:
                    res[inst['ticker']] = (universe[inst['ticker']][0], universe[inst['ticker']][1])
                    count += 1
            debug(f'Result: {res}')
            debug(f'Count: {count}')
        else:
            debug(f'Can\'t get json: {request_result.status_code}', "WARNING")
            debug(f'Can\'t get json: {request_result.text}', "WARNING")
        if len(res) > 0:
            # ++++++++ положим все в базу ++++++++
            if is_table_exist(TINKOFF_UNIVERSE_TABLE_NAME):
                eod_update_universe_table(res, TINKOFF_UNIVERSE_TABLE_NAME)
            else:
                create_universe_table(TINKOFF_UNIVERSE_TABLE_NAME)
                eod_insert_universe_data(res, TINKOFF_UNIVERSE_TABLE_NAME)


def main():
    debug("__Start main__")
    get_and_save_tinkoff_universe()


if __name__ == '__main__':
    debug("*********** Start get_and_save_tinkoff_universe ***********")
    main()
