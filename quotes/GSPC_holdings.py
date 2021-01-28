import json
from datetime import timedelta, date, datetime
from project_shared import *
from quotes.sql_queries import *
from quotes.quote_loader import *
from quotes.eodhistoricaldata import *
import simfin as sf
from simfin.names import *
import pandas as pd


def get_GSPC_alive_holdings():
    debug("#Start get INDEX Constituents")
    td = timedelta(days=30)
    check_data_min = datetime.datetime.strptime(DEFAULT_START_QUOTES_DATE, "%Y-%m-%d").date()
    check_data_min -= td
    interest_sectors = ['Consumer Cyclical', 'Utilities', 'Consumer Defensive']
    session = requests.Session()
    holdings = []
    url = f'https://eodhistoricaldata.com/api/fundamentals/GSPC.INDX'
    params = {'api_token': EOD_API_KEY, 'filter': 'Components'}
    request_result = session.get(url, params=params)
    if request_result.status_code == requests.codes.ok:
        parsed_json = json.loads(request_result.text)
        for company in parsed_json:
            ticker = parsed_json[company].get('Code', None)
            sector = parsed_json[company].get('Sector', None)
            min_ticker_date = get_min_historical_pricesdata(ticker, check_data_min, date.today())
            min_ticker_date = datetime.datetime.strptime(min_ticker_date, "%Y-%m-%d").date()
            if min_ticker_date <= check_data_min and sector in interest_sectors:
                holdings.append(ticker)
    debug(f'GSPC Holdings: {holdings}')


def get_min_historical_pricesdata(ticker, from_date, end_date):
    # debug("#Start get Historical Prices")
    session = requests.Session()
    prices = {}
    url = f'https://eodhistoricaldata.com/api/eod/{ticker}.US'
    params = {'api_token': EOD_API_KEY,
              'from': from_date.strftime("%Y-%m-%d"),
              'to': end_date.strftime("%Y-%m-%d"),
              'period': 'd',
              'fmt': 'json'}
    try:
        request_result = session.get(url, params=params)
    except Exception as e:
        # print(e, 'Waiting 10 sec')
        sleep(15)
        request_result = session.get(url, params=params)
    if request_result.status_code == requests.codes.ok:
        parsed_json = json.loads(request_result.text)
        for bar in parsed_json:
            prices[bar['date']] = (bar['open'], bar['high'], bar['low'], bar['close'], bar['adjusted_close'],
                                   bar['volume'], 0)

    return min(prices.keys())


if __name__ == '__main__':
    print(f"Starting get_GSPC_alive_holdings")
    get_GSPC_alive_holdings()
