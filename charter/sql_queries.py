def is_table_exist(table_name, engine=None) -> bool:
    with engine.connect() as connection:
        try:
            query_string = "SELECT 1 FROM " + table_name + " LIMIT 1"
            result = connection.execute(query_string)
            return True if result else False
        except:
            return False


def ticker_lookup(ticker, table_name, engine=None) -> bool:
    with engine.connect() as connection:
        try:
            query_string = "SELECT * FROM " + table_name + " WHERE ticker = '" + ticker + "' LIMIT 1"
            result = connection.execute(query_string)
            return True if result.rowcount > 0 else False
        except:
            return False


def get_quotes_by_ticker(ticker, table_name="quotes", start_date=None, end_date=None, engine=None):
    with engine.connect() as connection:
        connection.begin()
        try:
            query_string = "SELECT dateTime, open, high, low, close "
            query_string += "FROM " + table_name + " WHERE ticker "
            query_string += "= '" + ticker + "' "
            if start_date is not None:
                query_string += " AND dateTime >= '" + str(start_date) + "' "
            if end_date is not None:
                query_string += " AND dateTime <= '" + str(end_date) + "' "
            query_string += "ORDER BY dateTime ASC"
            result = connection.execute(query_string)
            if result.rowcount > 0:
                print("result.rowcount=" + str(result.rowcount))
                return result.cursor.fetchall()
            else:
                return None
        except:
            return None