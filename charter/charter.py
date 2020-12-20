import charter.finance2 as fin
import charter.sql_queries as sql
from datetime import date, timedelta
from project_shared import *


def get_year_data_by_ticker(ticker, start_date=None, end_date=date.today()):
    if sql.is_table_exist(QUOTE_TABLE_NAME):
        quotes = None
        if start_date is None:
            td = timedelta(365)
            start_date = end_date - td
        if sql.ticker_lookup(ticker):
            quotes = sql.get_quotes_by_ticker(ticker=ticker, start_date=start_date, end_date=end_date)
        else:
            debug(f'Ticker:{ticker} not found!!!')
            return None
    else:
        debug(f'Quotes table: {QUOTE_TABLE_NAME} not found!')
        return None
    return quotes


def get_ytd_data_by_ticker(ticker, start_date=None, end_date=date.today()):
    if sql.is_table_exist(QUOTE_TABLE_NAME):
        quotes = None
        if start_date is None:
            start_date = date(end_date.year, 1, 1)
        if sql.ticker_lookup(ticker):
            quotes = sql.get_quotes_by_ticker(ticker=ticker, start_date=start_date, end_date=end_date)
        else:
            debug(f'Ticker: {ticker} not found!!!')
            return None
    else:
        debug(f'Quotes table: {QUOTE_TABLE_NAME} not found!' )
        return None
    return quotes


def create_candle_chart_image(ticker, compare_ticker, chart_type="Y"):
    ticker_quotes = None
    compare_ticker_quotes = None
    if chart_type == "Y":
        ticker_quotes = get_year_data_by_ticker(ticker)
        compare_ticker_quotes = get_year_data_by_ticker(compare_ticker)
    if chart_type == "YTD":
        ticker_quotes = get_ytd_data_by_ticker(ticker)
        compare_ticker_quotes = get_ytd_data_by_ticker(compare_ticker)
    if ticker_quotes is not None and compare_ticker_quotes is not None:
        fin.create_chart(ticker, ticker_quotes, compare_ticker, compare_ticker_quotes)
    else:
        debug("WARNING: Can't create chart!")


def create_excess_histogram(ticker, compare_ticker, chart_type="Y"):
    ticker_quotes = None
    compare_ticker_quotes = None
    if chart_type == "Y":
        ticker_quotes = get_year_data_by_ticker(ticker)
        compare_ticker_quotes = get_year_data_by_ticker(compare_ticker)
    if chart_type == "YTD":
        ticker_quotes = get_ytd_data_by_ticker(ticker)
        compare_ticker_quotes = get_ytd_data_by_ticker(compare_ticker)
    if ticker_quotes is not None and compare_ticker_quotes is not None:
        fin.create_excess_histogram(ticker, ticker_quotes, compare_ticker, compare_ticker_quotes)
    else:
        debug("WARNING: Can't create chart!")


def create_portfolio_pie_image(weights, title, filename):
    fin.create_portfolio_donut(portfolio_data=weights, title=title, filename=filename)

def main():
    debug("__Start main__")
    if sql.is_table_exist(QUOTE_TABLE_NAME):
        ticker = "TSLA"
        compare_ticker = "FB"
        create_candle_chart_image(ticker, compare_ticker, chart_type="YTD")
        create_excess_histogram(ticker, compare_ticker, chart_type="YTD")
        fin.create_portfolio_donut()


if __name__ == '__main__':
    print("*********** Start Charter ***********")
    main()
