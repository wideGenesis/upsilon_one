import pandas as pd
from project_shared import *
from datetime import date, timedelta


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


def get_start_table_date(table_name=QUOTE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        try:
            query_string = f'SELECT dateTime FROM {table_name} ORDER by dateTime ASC LIMIT 1'
            result = connection.execute(query_string)
            return result.cursor.fetchone()[0]
        except:
            return None


def get_last_table_date(table_name=QUOTE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        try:
            query_string = f'SELECT dateTime FROM {table_name} ORDER by dateTime DESC LIMIT 1'
            result = connection.execute(query_string)
            return result.cursor.fetchone()[0]
        except:
            return None


def create_quotes_table(table_name=QUOTE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if not is_table_exist(table_name):
            transaction = connection.begin()
            create_query = f'CREATE TABLE {table_name} ' \
                           f'(ticker VARCHAR(6) NOT NULL, ' \
                           f'dateTime DATE, ' \
                           f'open  DOUBLE, ' \
                           f'high DOUBLE NOT NULL, ' \
                           f'low DOUBLE NOT NULL, ' \
                           f'close DOUBLE NOT NULL, ' \
                           f'adj_close DOUBLE NOT NULL, ' \
                           f'volume INTEGER NOT NULL, ' \
                           f'dividend DOUBLE NOT NULL, ' \
                           f'PRIMARY KEY(ticker, dateTime)' \
                           f')'
            connection.execute(create_query)
            transaction.commit()


def insert_quotes(ticker, quotes, is_update=True, table_name=QUOTE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            for qdate in quotes:
                o, h, l, c, ac, v, d = quotes[qdate]
                test = False
                if is_update:
                    try:
                        query_string = f'SELECT * FROM {table_name} ' \
                                       f'WHERE ticker = \'{ticker}\' AND dateTime = \'{str(qdate)}\' LIMIT 1'
                        result = connection.execute(query_string)
                        if result.rowcount > 0:
                            test = True
                            # debug("Duplicate date! Not insert!")
                        else:
                            test = False
                    except:
                        test = False
                if not test:
                    insert_query = f'INSERT INTO {table_name} ' \
                                   f'(ticker, dateTime, open, high, low, close, adj_close, volume, dividend) ' \
                                   f'VALUES (\'{ticker}\', \'{str(qdate)}\', ' \
                                   f'\'{str(o)}\', \'{str(h)}\', \'{str(l)}\', \'{str(c)}\', \'{str(ac)}\', ' \
                                   f'\'{str(v)}\', \'{str(d)}\')'
                    connection.execute(insert_query)
            transaction.commit()
        except:
            transaction.rollback()


def get_closes_universe_df(q_table_name=QUOTE_TABLE_NAME, u_table_name=UNIVERSE_TABLE_NAME, cap_filter=0, etf_list=None,
                           start_date=None, end_date=date.today(), engine=engine):
    with engine.connect() as connection:
        closes = None
        dat = {}
        if etf_list is not None:
            for ticker in etf_list:
                query_string = f'SELECT q.dateTime, q.close FROM {q_table_name} q ' \
                               f' WHERE q.ticker=\'{ticker}\''
                if start_date is not None:
                    query_string += f' AND q.dateTime >= \'{str(start_date)}\' '
                if end_date is not None:
                    query_string += f' AND q.dateTime <= \'{str(end_date)}\' '
                query_string += f' ORDER BY q.dateTime ASC'
                q_result = connection.execute(query_string)
                if q_result.rowcount > 0:
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
        tickers = get_universe(u_table_name, engine)
        for ticker in tickers:
            query_string = f'SELECT q.dateTime, q.close FROM {q_table_name} q, {u_table_name} u' \
                           f' WHERE q.ticker=\'{ticker}\' AND q.ticker=u.ticker AND u.mkt_cap > \'{cap_filter}\'' \
                           f' AND u.mkt_cap IS NOT NULL'
            if start_date is not None:
                query_string += f' AND q.dateTime >= \'{str(start_date)}\' '
            if end_date is not None:
                query_string += f' AND q.dateTime <= \'{str(end_date)}\' '
            q_result = connection.execute(query_string)
            if q_result.rowcount > 0:
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


def get_closes_by_ticker_list(ticker_list, start_date=None, end_date=date.today(),
                              q_table_name=QUOTE_TABLE_NAME, u_table_name=UNIVERSE_TABLE_NAME,
                              engine=engine):
    with engine.connect() as connection:
        closes = None
        dat = {}
        if start_date is None:
            td = timedelta(365)
            start_date = end_date - td

        for ticker in ticker_list:
            query_string = f'SELECT q.dateTime, q.close FROM {q_table_name} q, {u_table_name} u' \
                           f' WHERE q.ticker=\'{ticker}\' AND q.ticker=u.ticker '
            if start_date is not None:
                query_string += f' AND q.dateTime >= \'{str(start_date)}\' '
            if end_date is not None:
                query_string += f' AND q.dateTime <= \'{str(end_date)}\' '
            query_string += f' ORDER BY q.dateTime ASC'

            q_result = connection.execute(query_string)
            if q_result.rowcount > 0:
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


def get_ohlc_dict_by_port_id(port_id, start_date=None, end_date=date.today(),
                                 q_table_name=QUOTE_TABLE_NAME, u_table_name=UNIVERSE_TABLE_NAME,
                                 engine=engine):
    with engine.connect() as connection:
        weight_table = PORTFOLIO_ALLOCATION_TABLE_NAME
        ohlc = {}
        if start_date is None:
            td = timedelta(365)
            start_date = end_date - td
        query_string = f'SELECT q.ticker, q.dateTime, q.open, q.high, q.low, q.close, w.weight, q.adj_close ' \
                       f'FROM {q_table_name} q, {u_table_name} u, {weight_table} w' \
                       f' WHERE q.ticker=u.ticker ' \
                       f' AND q.ticker=w.ticker AND u.ticker=w.ticker ' \
                       f' AND w.port_id=\'{port_id}\''
        if start_date is not None:
            query_string += f' AND q.dateTime >= \'{str(start_date)}\' '
        if end_date is not None:
            query_string += f' AND q.dateTime <= \'{str(end_date)}\' '
        query_string += f' ORDER BY q.dateTime ASC'

        q_result = connection.execute(query_string)
        if q_result.rowcount > 0:
            rows = q_result.fetchall()
            for row in rows:
                ticker, dat, o, h, l, c, weight = row
                if ticker in ohlc:
                    ohlc[ticker].append((dat, o, h, l, c, weight))
                else:
                    ohlc[ticker] = [(dat, o, h, l, c, weight)]
    return ohlc


def get_closes_by_ticker_list_ti(ticker_list, time_interval=365,
                                 q_table_name=QUOTE_TABLE_NAME, u_table_name=UNIVERSE_TABLE_NAME,
                                 engine=engine):
    with engine.connect() as connection:
        closes = None
        dat = {}
        end_date = date.today()
        td = timedelta(time_interval)
        start_date = end_date - td

        for ticker in ticker_list:
            query_string = f'SELECT q.dateTime, q.close FROM {q_table_name} q, {u_table_name} u' \
                           f' WHERE q.ticker=\'{ticker}\' AND q.ticker=u.ticker '
            if start_date is not None:
                query_string += f' AND q.dateTime >= \'{str(start_date)}\' '
            if end_date is not None:
                query_string += f' AND q.dateTime <= \'{str(end_date)}\' '
            query_string += f' ORDER BY q.dateTime ASC'

            q_result = connection.execute(query_string)
            if q_result.rowcount > 0:
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
def create_universe_table(table_name=UNIVERSE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if not is_table_exist(table_name):
            transaction = connection.begin()
            create_query = f'CREATE TABLE {table_name} ' \
                           f'(ticker VARCHAR(6) NOT NULL, ' \
                           f'mkt_cap BIGINT, ' \
                           f'sector VARCHAR(100), ' \
                           f'exchange VARCHAR(20), ' \
                           f'PRIMARY KEY(ticker)' \
                           f')'
            connection.execute(create_query)
            transaction.commit()


def update_universe_table(new_universe, table_name=UNIVERSE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            transaction = connection.begin()
            try:
                del_query = f'DELETE FROM {table_name}'
                connection.execute(del_query)
                for ticker in new_universe:
                    insert_query = f'INSERT INTO {table_name} (ticker) VALUES (\'{ticker}\')'
                    connection.execute(insert_query)
                transaction.commit()
            except:
                transaction.rollback()
        else:
            debug(f'Can\'t find table: {table_name}!')


def eod_update_universe_table(new_universe, table_name=UNIVERSE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            transaction = connection.begin()
            try:
                del_query = f'DELETE FROM {table_name}'
                connection.execute(del_query)
                for ticker in new_universe:
                    sector, mkt_cap, exchange = new_universe[ticker]
                    insert_query = f'INSERT INTO {table_name} (ticker, mkt_cap, sector, exchange) ' \
                                   f'VALUES (\'{ticker}\', \'{mkt_cap}\', \'{sector}\', \'{exchange}\')'
                    connection.execute(insert_query)
                transaction.commit()
            except Exception as e:
                debug(e)
                transaction.rollback()
        else:
            debug(f'Can\'t find table: {table_name}!')


def delete_from_universe(ticker, table_name=UNIVERSE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            transaction = connection.begin()
            try:
                del_query = f'DELETE FROM \'{table_name}\' WHERE ticker=\'{ticker}\''
                connection.execute(del_query)
                transaction.commit()
            except:
                transaction.rollback()
        else:
            debug(f'Can\'t find table: {table_name}!')


def set_universe_mkt_cap(ticker_data, table_name=UNIVERSE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            transaction = connection.begin()
            try:
                for ticker in ticker_data:
                    sector, mkt_cap = ticker_data[ticker]
                    if ticker_lookup(ticker, table_name):
                        upd_query = f'UPDATE {table_name} SET ' \
                                    f'mkt_cap=\'{mkt_cap}\', sector=\'{sector}\' ' \
                                    f'WHERE ticker=\'{ticker}\''
                        connection.execute(upd_query)
                    else:
                        insert_query = f'INSERT INTO {table_name} (ticker, mkt_cap, sector) ' \
                                       f'VALUES (\'{ticker}\', \'{mkt_cap}\', \'{sector}\')'
                        connection.execute(insert_query)
                transaction.commit()
            except:
                transaction.rollback()
        else:
            debug(f'Can\'t find table: {table_name}!')


def eod_set_universe_mkt_cap(ticker_data, table_name=UNIVERSE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            transaction = connection.begin()
            try:
                for ticker in ticker_data:
                    mkt_cap = ticker_data[ticker]
                    if ticker_lookup(ticker, table_name):
                        upd_query = f'UPDATE {table_name} SET ' \
                                    f'mkt_cap=\'{mkt_cap}\' ' \
                                    f'WHERE ticker=\'{ticker}\''
                        connection.execute(upd_query)
                    else:
                        insert_query = f'INSERT INTO {table_name} (ticker, mkt_cap, sector) ' \
                                       f'VALUES (\'{ticker}\', \'{mkt_cap}\', \'\')'
                        connection.execute(insert_query)
                transaction.commit()
            except:
                transaction.rollback()
        else:
            debug(f'Can\'t find table: {table_name}!')


def insert_universe_data(new_universe, table_name=UNIVERSE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            transaction = connection.begin()
            try:
                for ticker in new_universe:
                    insert_query = f'INSERT INTO {table_name} (ticker) VALUES (\'{ticker}\')'
                    connection.execute(insert_query)
                transaction.commit()
            except:
                transaction.rollback()
        else:
            debug(f'Can\'t find table: {table_name}!')


def eod_insert_universe_data(new_universe, table_name=UNIVERSE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            transaction = connection.begin()
            try:
                for ticker in new_universe:
                    if len(new_universe[ticker]) < 3:
                        debug(f'ticker:{ticker} : new_universe[ticker]={new_universe[ticker]}')
                    sector, mkt_cap, exchange = new_universe[ticker]
                    insert_query = f'INSERT INTO {table_name} (ticker, mkt_cap, sector, exchange) ' \
                                   f'VALUES (\'{ticker}\', \'{mkt_cap}\', \'{sector}\', \'{exchange}\')'
                    connection.execute(insert_query)
                transaction.commit()
            except Exception as e:
                debug(e)
                transaction.rollback()
        else:
            debug(f'Can\'t find table: {table_name}!')


def get_universe(table_name=UNIVERSE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
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
            debug(f'Can\'t find table: {table_name}!')


def get_all_universe(table_name=UNIVERSE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            res = {}
            del_query = "SELECT ticker, sector, mkt_cap FROM " + table_name
            result = connection.execute(del_query)
            if result.rowcount > 0:
                for t in result.fetchall():
                    res[t[0]] = (t[1], t[2])
                return res
            else:
                return None
        else:
            debug(f'Can\'t find table: {table_name}!')
