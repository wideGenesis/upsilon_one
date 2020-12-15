from project_shared import *


def is_table_exist(table_name, engine=engine) -> bool:
    with engine.connect() as connection:
        try:
            query_string = f'SELECT 1 FROM {table_name} LIMIT 1'
            result = connection.execute(query_string)
            return True if result else False
        except:
            return False


def ticker_lookup(ticker, table_name=QUOTE_TABLE_NAME, engine=engine) -> bool:
    with engine.connect() as connection:
        try:
            query_string = f'SELECT * FROM {table_name} WHERE ticker = \'{ticker}\' LIMIT 1'
            result = connection.execute(query_string)
            return True if result.rowcount > 0 else False
        except:
            return False


def get_quotes_by_ticker(ticker, start_date=None, end_date=None, table_name=QUOTE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        try:
            query_string = f'SELECT dateTime, open, high, low, close FROM {table_name} WHERE ticker=\'{ticker}\''
            if start_date is not None:
                query_string += f' AND dateTime >= \'{str(start_date)}\' '
            if end_date is not None:
                query_string += f' AND dateTime <= \'{str(end_date)}\' '
            query_string += f' ORDER BY dateTime ASC'
            result = connection.execute(query_string)
            if result.rowcount > 0:
                # print("result.rowcount=" + str(result.rowcount))
                return result.cursor.fetchall()
            else:
                return None
        except:
            return None
