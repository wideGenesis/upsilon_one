import json
import requests
import datetime
from project_shared import *
from quotes.sql_queries import *

TOKEN = 't.TuzfyQk5bMfqGQdKuOPUDo9QPuRuUJEjQuc6uKEqrYBfHAK1X_8gIHgpWf_ZlohqTjzPb8IYGrgpGrJjz66eQw'


def get_and_save_universe():
    with requests.Session() as session:
        url = f'https://api-invest.tinkoff.ru/openapi/market/stocks'
        headers = {'accept': 'application/json', 'Authorization': f'Bearer {TOKEN}'}
        request_result = session.get(url, headers=headers)
        if request_result.status_code == requests.codes.ok:
            parsed_json = json.loads(request_result.text)
            universe = get_universe()
            count = 0
            for inst in parsed_json['payload']['instruments']:
                if inst['currency'] == 'USD' and inst['ticker'] in universe:
                    count += 1
                    debug(f'Ticker: ' + inst['ticker'])
            debug(f'Count: {count}')
        else:
            debug(f'Can\'t get json: {request_result.status_code}', "WARNING")
            debug(f'Can\'t get json: {request_result.text}', "WARNING")


def main():
    debug("__Start main__")
    get_and_save_universe()


if __name__ == '__main__':
    print("*********** Start Charter ***********")
    main()
