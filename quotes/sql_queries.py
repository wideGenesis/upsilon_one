from datetime import date
import pymysql
import pandas as pd


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


def get_start_table_date(table_name, engine=None) -> bool:
    with engine.connect() as connection:
        try:
            query_string = "SELECT dateTime FROM " + table_name + " ORDER by dateTime ASC LIMIT 1"
            result = connection.execute(query_string)
            return result.cursor.fetchone()[0]
        except:
            return None


def get_last_table_date(table_name, engine=None) -> bool:
    with engine.connect() as connection:
        try:
            query_string = "SELECT dateTime FROM " + table_name + " ORDER by dateTime DESC LIMIT 1"
            result = connection.execute(query_string)
            return result.cursor.fetchone()[0]
        except:
            return None


def create_quotes_table(table_name="quotes", engine=None):
    with engine.connect() as connection:
        is_exist = is_table_exist(table_name, engine)
        if not is_exist:
            connection.execute("CREATE TABLE "
                               + table_name +
                               " (ticker VARCHAR(6) NOT NULL, "
                               "dateTime DATE, "
                               "open  DOUBLE, "
                               "high DOUBLE NOT NULL, "
                               "low DOUBLE NOT NULL, "
                               "close DOUBLE NOT NULL, "
                               "volume INTEGER NOT NULL, "
                               "dividend DOUBLE NOT NULL, "
                               "PRIMARY KEY(ticker, dateTime)"
                               ")")
            connection.execute("commit")


def insert_quotes(ticker, quotes, table_name="quotes", is_update=True, engine=None):
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            for qdate in quotes:
                o, h, l, c, v, d = quotes[qdate]
                test = False
                if is_update:
                    try:
                        query_string = "SELECT * FROM " + table_name + " WHERE ticker = '" + ticker + "' AND dateTime = '" + str(qdate) + "' LIMIT 1"
                        result = connection.execute(query_string)
                        if result.rowcount > 0:
                            test = True
                            print("Duplicate date! Not insert!")
                        else:
                            test = False
                    except:
                        test = False
                if not test:
                    connection.execute("INSERT INTO "
                                       + table_name +
                                       " (ticker, dateTime, open, high, low, close, volume, dividend) "
                                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [ticker, str(qdate),
                                                                                   str(o), str(h), str(l), str(c),
                                                                                   str(v), str(d)])
            transaction.commit()
        except:
            transaction.rollback()


def get_closes_universe_df(q_table_name, u_table_name, engine):
    tickers = get_universe(u_table_name, engine)
    with engine.connect() as connection:
        closes = None
        dat = {}
        for ticker in tickers:
            query_string = f'SELECT dateTime, close from {q_table_name} where ticker=\'{ticker}\''
            q_result = connection.execute(query_string)
            rows = q_result.fetchall()
            c0 = []
            c1 = []
            for row in rows:
                c0.append(row[0])
                c1.append(row[1])
            series = pd.Series(c1, index=c0)
            dat[ticker] = series
        closes = pd.DataFrame(dat)
    return closes

# ******************** UNIVERSE ********************
def create_universe_table(table_name="universe", engine=None):
    with engine.connect() as connection:
        is_exist = is_table_exist(table_name, engine)
        if not is_exist:
            connection.execute("CREATE TABLE "
                               + table_name +
                               " (ticker VARCHAR(6) NOT NULL, "
                               "PRIMARY KEY(ticker)"
                               ")")
            connection.execute("commit")


def update_universe_table(new_universe, table_name="universe", engine=None):
    with engine.connect() as connection:
        is_exist = is_table_exist(table_name, engine)
        if is_exist:
            transaction = connection.begin()
            try:
                del_query = "DELETE FROM " + table_name
                connection.execute(del_query)
                for ticker in new_universe:
                    connection.execute("INSERT INTO " + table_name + " (ticker) VALUES (%s)", [ticker])
            except:
                transaction.rollback()
            transaction.commit()
        else:
            print(f'Can\'t find table: {table_name}!')


def insert_universe_data(new_universe, table_name="universe", engine=None):
    with engine.connect() as connection:
        is_exist = is_table_exist(table_name, engine)
        if is_exist:
            transaction = connection.begin()
            try:
                for ticker in new_universe:
                    connection.execute("INSERT INTO " + table_name + " (ticker) VALUES (%s)", [ticker])
            except:
                transaction.rollback()
            transaction.commit()
        else:
            print(f'Can\'t find table: {table_name}!')


def get_universe(table_name="universe", engine=None):
    with engine.connect() as connection:
        is_exist = is_table_exist(table_name, engine)
        if is_exist:
            res = list()
            del_query = "SELECT ticker FROM " + table_name
            result = connection.execute(del_query)
            if result.rowcount > 0:
                for t in result.fetchall():
                    res.append(t[0])
                return res
            else:
                return None
        else:
            print(f'Can\'t find table: {table_name}!')
