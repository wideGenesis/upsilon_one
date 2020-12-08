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


def main():
    print("__Start main__")
    if sql.is_table_exist(QUOTE_TABLE_NAME, engine):
        ticker = "QQQ"
        td = timedelta(365)
        end_date = date.today()
        start_date = end_date - td
        if sql.ticker_lookup(ticker, QUOTE_TABLE_NAME, engine):
            if end_date is not None and start_date is not None:
                quotes = sql.get_quotes_by_ticker(ticker=ticker, table_name=QUOTE_TABLE_NAME, start_date=start_date,
                                                  end_date=end_date, engine=engine)
            else:
                quotes = sql.get_quotes_by_ticker(ticker=ticker, table_name=QUOTE_TABLE_NAME, engine=engine)
            compare_ticker = "MTUM"
            compare_quotes = None
            if sql.ticker_lookup(compare_ticker, QUOTE_TABLE_NAME, engine):
                if end_date is not None and start_date is not None:
                    compare_quotes = sql.get_quotes_by_ticker(ticker=compare_ticker, table_name=QUOTE_TABLE_NAME,
                                                              start_date=start_date, end_date=end_date, engine=engine)
                else:
                    compare_quotes = sql.get_quotes_by_ticker(ticker=ticker, table_name=QUOTE_TABLE_NAME, engine=engine)
            print(str(quotes))
            fin.create_chart(ticker, quotes, compare_ticker, compare_quotes)
            fin.create_excess_histogram(ticker, quotes, compare_ticker, compare_quotes)
        else:
            print("Ticker:" + ticker + " not found!!!")
    else:
        print("Quotes tbale:" + QUOTE_TABLE_NAME + " not found!")


if __name__ == '__main__':
    print("*********** Start Charter ***********")
    main()
