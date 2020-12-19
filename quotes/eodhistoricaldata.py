import json
import requests
import datetime
from project_shared import *
from quotes.sql_queries import *


def get_all_etf_holdings():
    debug("#Start get ETF holdings")
    session = requests.Session()
    ticker_data = {}
    for etf in ETF_FOR_SCRAPE:
        url = f'https://eodhistoricaldata.com/api/fundamentals/{etf}.US'
        params = {'api_token': EOD_API_KEY}
        request_result = session.get(url, params=params)
        if request_result.status_code == requests.codes.ok:
            parsed_json = json.loads(request_result.text)
            holdings = parsed_json['ETF_Data']['Holdings']
            for holding in holdings:
                ticker_data[holdings[holding]['Code']] = holdings[holding]['Sector']
                debug(f"Ticker:{holdings[holding]['Code']}  Sector: {holdings[holding]['Sector']}")
    return ticker_data


def get_etf_holdings(etf):
    debug("#Start get ETF holdings")
    session = requests.Session()
    holdings = {}
    url = f'https://eodhistoricaldata.com/api/fundamentals/{etf}.US'
    params = {'api_token': EOD_API_KEY, 'filter': 'ETF_Data::Holdings'}
    request_result = session.get(url, params=params)
    if request_result.status_code == requests.codes.ok:
        parsed_json = json.loads(request_result.text)
        for company in parsed_json:
            holdings[parsed_json[company]['Code']] = parsed_json[company]['Sector']
    return holdings


def get_market_cap(ticker):
    debug("#Start get MarketCapitalization")
    session = requests.Session()
    mkt_cap = 0
    url = f'https://eodhistoricaldata.com/api/fundamentals/{ticker}.US'
    params = {'api_token': EOD_API_KEY, 'filter': 'Highlights::MarketCapitalization'}
    request_result = session.get(url, params=params)
    if request_result.status_code == requests.codes.ok:
        parsed_json = json.loads(request_result.text)
        mkt_cap = int(parsed_json)
    return mkt_cap


def get_historical_prices(ticker, from_date, end_date):
    debug("#Start get Historical Prices")
    session = requests.Session()
    prices = {}
    url = f'https://eodhistoricaldata.com/api/eod/{ticker}.US'
    params = {'api_token': EOD_API_KEY,
              'from': from_date.strftime("%Y-%m-%d"),
              'to': end_date.strftime("%Y-%m-%d"),
              'period': 'd',
              'fmt': 'json'}
    request_result = session.get(url, params=params)
    if request_result.status_code == requests.codes.ok:
        parsed_json = json.loads(request_result.text)
        for bar in parsed_json:
            prices[bar['date']] = (bar['open'], bar['high'], bar['low'], bar['adjusted_close'], bar['volume'], 0)
    insert_quotes(ticker, prices, is_update=False)


def main():
    debug("__Start main__")
    mkt_cap = get_market_cap('AAPL')
    debug(str(mkt_cap))
    holdings = get_etf_holdings('VTI')
    debug(holdings)
    from_date = datetime.date(2019, 1, 1)
    get_historical_prices('MCD', from_date, datetime.date.today())


if __name__ == '__main__':
    print("*********** Start Charter ***********")
    main()
