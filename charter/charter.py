import yaml
import logging
import finance2 as fin
import sql_queries as sql
from datetime import date, timedelta
from sqlalchemy import create_engine
from alchemysession import AlchemySessionContainer

conf = yaml.safe_load(open('../config/settings.yaml'))

# ============================== SQL Connect ======================

SQL_DB_NAME = conf['SQL']['DB_NAME']
SQL_USER = conf['SQL']['DB_USER']
SQL_PASSWORD = conf['SQL']['DB_PASSWORD']
SQL_URI = 'mysql+pymysql://{}:{}@localhost/{}'.format(SQL_USER, SQL_PASSWORD, SQL_DB_NAME)

engine = create_engine(SQL_URI, pool_recycle=3600)
container = AlchemySessionContainer(engine=engine)
alchemy_session = container.new_session('default')

QUOTE_TABLE_NAME = "quotes"


# ============================== Logging Setup ======================
# logging.basicConfig(
#     filemode='w',
#     filename=os.path.abspath('logs/quote_loader.log'),
#     format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
#     level=logging.DEBUG)
# logging.getLogger('telethon').setLevel(level=logging.DEBUG)


def get_year_data_by_ticker(ticker, start_date=None, end_date=date.today()):
    if sql.is_table_exist(QUOTE_TABLE_NAME, engine):
        quotes = None
        if start_date is None:
            td = timedelta(365)
            start_date = end_date - td
        if sql.ticker_lookup(ticker, QUOTE_TABLE_NAME, engine):
            quotes = sql.get_quotes_by_ticker(ticker=ticker, table_name=QUOTE_TABLE_NAME, start_date=start_date,
                                              end_date=end_date, engine=engine)
        else:
            print("Ticker:" + ticker + " not found!!!")
            return None
    else:
        print("Quotes table:" + QUOTE_TABLE_NAME + " not found!")
        return None
    return quotes


def get_ytd_data_by_ticker(ticker, start_date=None, end_date=date.today()):
    if sql.is_table_exist(QUOTE_TABLE_NAME, engine):
        quotes = None
        if start_date is None:
            start_date = date(end_date.year, 1, 1)
        if sql.ticker_lookup(ticker, QUOTE_TABLE_NAME, engine):
            quotes = sql.get_quotes_by_ticker(ticker=ticker, table_name=QUOTE_TABLE_NAME, start_date=start_date,
                                              end_date=end_date, engine=engine)
        else:
            print("Ticker:" + ticker + " not found!!!")
            return None
    else:
        print("Quotes table:" + QUOTE_TABLE_NAME + " not found!")
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
        print("WARNING: Can't create chart!")


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
        print("WARNING: Can't create chart!")


def main():
    print("__Start main__")
    if sql.is_table_exist(QUOTE_TABLE_NAME, engine):
        ticker = "QQQ"
        compare_ticker = "MTUM"
        create_candle_chart_image(ticker, compare_ticker, chart_type="YTD")
        create_excess_histogram(ticker, compare_ticker, chart_type="YTD")


if __name__ == '__main__':
    print("*********** Start Charter ***********")
    main()
