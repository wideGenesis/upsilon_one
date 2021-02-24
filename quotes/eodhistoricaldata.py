import json
import requests
import datetime
from project_shared import *
from quotes.sql_queries import *
from time import sleep


def get_all_etf_holdings():
    debug("ETF_FOR_SCRAPE:" + str(ETF_FOR_SCRAPE))
    ticker_data = {}
    request_count = 0
    t_len = len(ETF_FOR_SCRAPE)
    if not is_debug_init():
        print_progress_bar(0, t_len, prefix='Progress:', suffix='Complete', length=50)
    for numb, etf in enumerate(ETF_FOR_SCRAPE, start=1):
        with requests.Session() as session:
            url = f'https://eodhistoricaldata.com/api/fundamentals/{etf}.US'
            params = {'api_token': EOD_API_KEY, 'filter': 'ETF_Data::Holdings'}
            if request_count > 0 and request_count % 200 == 0:
                sleep(3)
            try:
                request_result = session.get(url, params=params)
            except Exception as e:
                # print(e, 'Waiting 10 sec')
                sleep(10)
                request_result = session.get(url, params=params)
            request_count += 1
            if request_result.status_code == requests.codes.ok:
                parsed_json = json.loads(request_result.text)
                for count, company in enumerate(parsed_json, start=1):
                    ticker = parsed_json[company].get('Code', None)
                    if ticker is not None:
                        if ticker not in ticker_data:
                            sector, mkt_cap, exchange = get_data_by_ticker(ticker, session)
                            request_count += 1
                            # debug(f'{ticker}:{etf}')
                            if (((sector not in EXCLUDE_SECTORS and sector is not None)
                                or ticker in NOT_EXCLUDE_TICKERS)
                                    and ticker not in EXCLUDE_TICKERS and exchange in VALID_EXCHANGE):
                                # debug(f'INSERT {ticker}:{etf}', "WARNING")
                                ticker_data[ticker] = (sector, mkt_cap, exchange)
                    else:
                        # debug(f'Cant get Code for company:ETF:{etf}:{company}')
                        ticker = lookup_ticker_by_name(company_name=company, sess=session)
                        request_count += 1
                        if ticker is not None and ticker not in ticker_data:
                            sector, mkt_cap, exchange = get_data_by_ticker(ticker, session)
                            request_count += 1
                            # debug(f'{ticker}:{exchange}')
                            if (((sector not in EXCLUDE_SECTORS and sector is not None)
                                or ticker in NOT_EXCLUDE_TICKERS)
                                    and ticker not in EXCLUDE_TICKERS and exchange in VALID_EXCHANGE):
                                ticker_data[ticker] = (sector, mkt_cap, exchange)
                    if count == ETF_FOR_SCRAPE[etf]:
                        break
        if not is_debug_init():
            print_progress_bar(numb, t_len, prefix='Progress:', suffix=f'Complete:{etf}:{len(ticker_data)}    ',
                               length=50)
        else:
            debug(f'Complete:{etf}:{len(ticker_data)}')
    debug("Complete get_all_etf_holdings")
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
            ticker = parsed_json[company].get('Code', None)
            if ticker is not None:
                sector, mkt_cap, exchange = get_data_by_ticker(ticker, session)
                if (((sector not in EXCLUDE_SECTORS and sector is not None)
                     or ticker in NOT_EXCLUDE_TICKERS)
                        and ticker not in EXCLUDE_TICKERS and exchange in VALID_EXCHANGE):
                    holdings[ticker] = (sector, mkt_cap)
            else:
                ticker = lookup_ticker_by_name(company_name=company, sess=session)
                if ticker is not None and ticker not in holdings:
                    sector, mkt_cap, exchange = get_data_by_ticker(ticker, session)
                    if (((sector not in EXCLUDE_SECTORS and sector is not None)
                         or ticker in NOT_EXCLUDE_TICKERS)
                            and ticker not in EXCLUDE_TICKERS and exchange in VALID_EXCHANGE):
                        holdings[ticker] = (sector, mkt_cap, exchange)
    debug(str(holdings))
    return holdings


def get_index_constituent(index):
    debug("#Start get INDEX Constituents")
    session = requests.Session()
    holdings = {}
    url = f'https://eodhistoricaldata.com/api/fundamentals/{index}.INDX'
    params = {'api_token': EOD_API_KEY, 'filter': 'Components'}
    request_result = session.get(url, params=params)
    if request_result.status_code == requests.codes.ok:
        parsed_json = json.loads(request_result.text)
        for company in parsed_json:
            ticker = parsed_json[company].get('Code', None)
            if ticker is not None:
                sector, mkt_cap, exchange = get_data_by_ticker(ticker, session)
                if (((sector not in EXCLUDE_SECTORS and sector is not None)
                     or ticker in NOT_EXCLUDE_TICKERS)
                        and ticker not in EXCLUDE_TICKERS and exchange in VALID_EXCHANGE):
                    holdings[ticker] = (sector, mkt_cap, exchange)
            else:
                ticker = lookup_ticker_by_name(company_name=company, sess=session)
                if ticker is not None and ticker not in holdings:
                    sector, mkt_cap, exchange = get_data_by_ticker(ticker, session)
                    if (((sector not in EXCLUDE_SECTORS and sector is not None)
                         or ticker in NOT_EXCLUDE_TICKERS)
                            and ticker not in EXCLUDE_TICKERS and exchange in VALID_EXCHANGE):
                        holdings[ticker] = (sector, mkt_cap, exchange)
    debug(str(holdings))
    return holdings


def get_market_cap(ticker):
    # debug("#Start get MarketCapitalization")
    session = requests.Session()
    mkt_cap = 0
    url = f'https://eodhistoricaldata.com/api/fundamentals/{ticker}.US'
    params = {'api_token': EOD_API_KEY, 'filter': 'Highlights::MarketCapitalization'}
    request_result = session.get(url, params=params)
    if request_result.status_code == requests.codes.ok:
        parsed_json = json.loads(request_result.text)
        if isinstance(parsed_json, int):
            mkt_cap = int(parsed_json)
        else:
            debug(f'Ticker:{ticker}:Cant get mkt cap:{parsed_json}')
    return mkt_cap


def get_mkt_cap(ticker, sess):
    # debug("#Start get MarketCapitalization")
    session = sess
    mkt_cap = 0
    url = f'https://eodhistoricaldata.com/api/fundamentals/{ticker}.US'
    params = {'api_token': EOD_API_KEY, 'filter': 'Highlights::MarketCapitalization'}
    request_result = session.get(url, params=params)
    if request_result.status_code == requests.codes.ok:
        parsed_json = json.loads(request_result.text)
        if isinstance(parsed_json, int):
            mkt_cap = int(parsed_json)
        # else:
        #     debug(f'Ticker:{ticker}:Cant get mkt cap:{parsed_json}')
    return mkt_cap


def get_sector(ticker, sess):
    # debug("#Start get MarketCapitalization")
    session = sess
    sector = ""
    url = f'https://eodhistoricaldata.com/api/fundamentals/{ticker}.US'
    params = {'api_token': EOD_API_KEY, 'filter': 'General'}
    request_result = session.get(url, params=params)
    if request_result.status_code == requests.codes.ok:
        parsed_json = json.loads(request_result.text)
        sector = parsed_json.get('Sector', "")
    return sector


def get_data_by_ticker(ticker, sess):
    session = sess
    sector = ""
    mkt_cap = 0
    exchange = ""
    url = f'https://eodhistoricaldata.com/api/fundamentals/{ticker}.US'
    params = {'api_token': EOD_API_KEY}
    request_result = session.get(url, params=params)
    if request_result.status_code == requests.codes.ok:
        parsed_json = json.loads(request_result.text)
        if parsed_json.get('General', None) is not None:
            sector = parsed_json['General'].get('Sector', None)
            exchange = parsed_json['General'].get('Exchange', None)
            if parsed_json.get('Highlights', None) is not None:
                mkt_cap = parsed_json['Highlights'].get('MarketCapitalization', 0)
    return sector, mkt_cap, exchange


def get_tickerdata(ticker):
    session = requests.Session()
    sector = ""
    mkt_cap = 0
    exchange = ""
    url = f'https://eodhistoricaldata.com/api/fundamentals/{ticker}.US'
    params = {'api_token': EOD_API_KEY}
    request_result = session.get(url, params=params)
    if request_result.status_code == requests.codes.ok:
        parsed_json = json.loads(request_result.text)
        if parsed_json.get('General', None) is not None:
            sector = parsed_json['General'].get('Sector', None)
            exchange = parsed_json['General'].get('Exchange', None)
            if parsed_json.get('Highlights', None) is not None:
                mkt_cap = parsed_json['Highlights'].get('MarketCapitalization', 0)
    return sector, mkt_cap, exchange


def search_ticker_by_name(company_name, exchange="US"):
    ticker = None
    if company_name is None:
        return None
    session = requests.Session()
    url = f'https://eodhistoricaldata.com/api/search/{company_name}'
    params = {'api_token': EOD_API_KEY}
    request_result = session.get(url, params=params)
    if request_result.status_code == requests.codes.ok:
        parsed_json = json.loads(request_result.text)
        if parsed_json is None:
            return None
        if exchange == 'Any':
            ticker = parsed_json[0].get('Code', None)
            return ticker
        else:
            for item in parsed_json:
                if exchange == item.get('Exchange', None):
                    ticker = item.get('Code', None)
                    debug(f'$$$ Searched ticker:{ticker}')
                    return ticker


def lookup_ticker_by_name(company_name, exchange="US", sess=None):
    ticker = None
    if company_name is None:
        return None
    session = sess
    url = f'https://eodhistoricaldata.com/api/search/{company_name}'
    params = {'api_token': EOD_API_KEY}
    request_result = session.get(url, params=params)
    if request_result.status_code == requests.codes.ok:
        parsed_json = json.loads(request_result.text)
        if parsed_json is None:
            return None
        if exchange == 'Any':
            ticker = parsed_json[0].get('Code', None)
            return ticker
        else:
            for item in parsed_json:
                if exchange == item.get('Exchange', None):
                    ticker = item.get('Code', None)
                    return ticker


def get_historical_prices(ticker, from_date, end_date, is_update=False):
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

    url = f'https://eodhistoricaldata.com/api/splits/{ticker}.US'
    params = {'api_token': EOD_API_KEY,
              'from': from_date.strftime("%Y-%m-%d"),
              'to': end_date.strftime("%Y-%m-%d"),
              'fmt': 'json'}
    try:
        request_result = session.get(url, params=params)
    except Exception as e:
        # print(e, 'Waiting 10 sec')
        sleep(15)
        request_result = session.get(url, params=params)
    if request_result.status_code == requests.codes.ok:
        parsed_json = json.loads(request_result.text)
        for split in parsed_json:
            debug(f'Split[{ticker}]:' + split['date'] + ":::" + split['split'])

    insert_quotes(ticker, prices, is_update)


def get_historical_adjprices(ticker, from_date, end_date, is_update=False):
    # debug("#Start get Historical Prices")
    session = requests.Session()
    prices = {}
    url = ''
    if ticker == 'VIX':
        url = f'https://eodhistoricaldata.com/api/technical/{ticker}.INDX'
    else:
        url = f'https://eodhistoricaldata.com/api/technical/{ticker}.US'
    params = {'api_token': EOD_API_KEY,
              'from': from_date.strftime("%Y-%m-%d"),
              'to': end_date.strftime("%Y-%m-%d"),
              'order':  'd',
              'fmt': 'json',
              'function': 'splitadjusted'}
    try:
        request_result = session.get(url, params=params)
    except Exception as e:
        # print(e, 'Waiting 10 sec')
        count = 0
        while request_result.status_code != requests.codes.ok:
            sleep(5)
            request_result = session.get(url, params=params)
            count += 1
            if count == 10:
                debug(f"Cant get_historical_adjprices by ticker {ticker}", WARNING)
    if request_result.status_code == requests.codes.ok:
        parsed_json = json.loads(request_result.text)
        for bar in parsed_json:
            prices[bar['date']] = (bar['open'], bar['high'], bar['low'], bar['close'], bar['close'],
                                   bar['volume'], 0)
        # if len(prices) == 0:
        #     debug(f'Prices ticker: [{ticker}] is EMPTY!', WARNING)
    insert_quotes(ticker, prices, is_update)


def get_company_rank(ticker, exchange="US", sess=None):
    debug(f"### {ticker} ###")
    res1 = None
    res2 = None
    res3 = None
    if ticker is None:
        return res1, res2, res3, ""
    session = requests.Session()
    url = f'https://eodhistoricaldata.com/api/fundamentals/{ticker}.US'
    params = {'api_token': EOD_API_KEY}
    request_result = session.get(url, params=params)
    debug(f"request_result.status_code={request_result.status_code}")
    if request_result.status_code == requests.codes.ok:
        parsed_json = json.loads(request_result.text)
        # debug(f'parsed_json:{parsed_json}')
        if parsed_json is None:
            return res1, res2, res3, ""
        else:
            if parsed_json["General"]["IsDelisted"] == 'true':
                return res1, res2, res3, ""
            td = datetime.date.today()
            ipo_date = parsed_json["General"]["IPODate"]
            if datetime.datetime.strptime(ipo_date, "%Y-%m-%d").date() > add_months(td, -12):
                return res1, res2, res3, ipo_date

            EPSEstimateNextQuarter = parsed_json["Highlights"]["EPSEstimateNextQuarter"]
            EPSEstimateCurrentQuarter = parsed_json["Highlights"]["EPSEstimateCurrentQuarter"]
            if EPSEstimateNextQuarter == 0 and EPSEstimateCurrentQuarter == 0:
                return res1, res2, res3, ""

            # RevenuePerShareTTM = parsed_json["Highlights"]["RevenuePerShareTTM"]
            # DilutedEpsTTM = parsed_json["Highlights"]["DilutedEpsTTM"]
            delta = timedelta(days=1)
            td = datetime.date.today()
            eh = parsed_json["Earnings"]["History"]
            fqdate = next((dat for dat in eh if datetime.datetime.strptime(dat, "%Y-%m-%d").date() < td), None)
            if fqdate is None:
                debug(f"Can't find quarter date", ERROR)
                return res1, res2, res3, ""
            tmpdate = datetime.datetime.strptime(fqdate, "%Y-%m-%d").date()
            while tmpdate < td:
                tmpdate = add_months(tmpdate, 4)
                tmpdate = datetime.date(tmpdate.year, tmpdate.month, 1) - delta
            current_quarter = tmpdate
            debug(f'current_quarter: {current_quarter}')

            yearago = add_months(current_quarter, -11)
            yearago = datetime.date(yearago.year, yearago.month, 1) - delta
            yearago = yearago.strftime("%Y-%m-%d")

            next_quarter = add_months(current_quarter, 4)
            next_quarter = datetime.date(next_quarter.year, next_quarter.month, 1) - delta
            nqyearago = add_months(next_quarter, -11)
            nqyearago = datetime.date(nqyearago.year, nqyearago.month, 1) - delta
            nqyearago = nqyearago.strftime("%Y-%m-%d")
            debug(f'yearago={yearago}')
            # totalRevenueLastYear = parsed_json["Financials"]["Income_Statement"]["quarterly"][yearago]["totalRevenue"]
            epsActualYearago = parsed_json["Earnings"]["History"][yearago]["epsActual"]
            epsActualYearagoNextQuarterYearago = parsed_json["Earnings"]["History"][nqyearago]["epsActual"]
            QuarterlyRevenueGrowthYOY = parsed_json["Highlights"]["QuarterlyRevenueGrowthYOY"]

            if EPSEstimateNextQuarter is not None and  epsActualYearagoNextQuarterYearago is not None:
                res1 = (EPSEstimateNextQuarter - epsActualYearagoNextQuarterYearago) >= 0
            if EPSEstimateCurrentQuarter is not None and epsActualYearago is not None:
                res2 = (EPSEstimateCurrentQuarter - epsActualYearago) >= 0
            if QuarterlyRevenueGrowthYOY is not None:
                res3 = QuarterlyRevenueGrowthYOY >= 0
            debug(f'\nEPSEstimateNextQuarter: {EPSEstimateNextQuarter} \n'
                  f'EPSEstimateCurrentQuarter: {EPSEstimateCurrentQuarter}\n'
                  f'QuarterlyRevenueGrowthYOY:{QuarterlyRevenueGrowthYOY}\n'
                  # f'DilutedEpsTTM:{DilutedEpsTTM}\n'
                  # f'totalRevenue[{yearago}]:{totalRevenueLastYear}\n'
                  f'epsActualYearago[{yearago}]:{epsActualYearago}\n'
                  f'epsActualYearagoNextQuarterYearago[{nqyearago}]:{epsActualYearagoNextQuarterYearago}\n'
                  f'res1:{res1}\n'
                  f'res2:{res2}\n'
                  f'res3:{res3}')
            return res1, res2, res3, ""


def main():
    debug("__Start main__")
    # mkt_cap = get_market_cap('AAPL')
    # debug(str(mkt_cap))
    holdings = get_etf_holdings('ARKF')
    debug(holdings)
    # from_date = datetime.date(2019, 1, 1)
    # get_historical_prices('MCD', from_date, datetime.date.today())


if __name__ == '__main__':
    print("*********** Start Charter ***********")
    main()
