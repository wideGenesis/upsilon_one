import pandas as pd
from time import sleep
from project_shared import *
from datetime import date, timedelta
import sqlalchemy


def is_table_exist(table_name, engine=engine) -> bool:
    with engine.connect() as connection:
        try:
            query_string = f'SELECT 1 FROM {table_name} LIMIT 1'
            result = connection.execute(query_string)
            return True if result else False
        except:
            return False


# ============================================ PORTFOLIOS ============================================
# ============ Weights ============
def create_portfolio_allocation_table(table_name=PORTFOLIO_ALLOCATION_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if not is_table_exist(table_name):
            transaction = connection.begin()
            create_query = f'CREATE TABLE {table_name} ' \
                           f'(port_id VARCHAR(100) NOT NULL, ' \
                           f'ticker VARCHAR(6), ' \
                           f'weight DOUBLE, ' \
                           f'PRIMARY KEY(port_id, ticker, weight)' \
                           f')'
            connection.execute(create_query)
            transaction.commit()


def update_portfolio_allocation(port_id, weights, table_name=PORTFOLIO_ALLOCATION_TABLE_NAME, engine=engine,
                                recursion_count=0):
    if recursion_count == RECURSION_DEPTH:
        return -1
    with engine.connect() as connection:
        if is_table_exist(table_name):
            transaction = connection.begin()
            try:
                del_query = f'DELETE FROM {table_name} WHERE port_id=\'{port_id}\''
                connection.execute(del_query)
            except sqlalchemy.exc.OperationalError as oe:
                if oe.orig.args[0] == 1213:
                    debug(f'Exception: {oe}', "WARNING")
                    sleep(0.9)
                    errCode = update_portfolio_allocation(port_id=port_id, weights=weights,
                                                          recursion_count=recursion_count + 1)
                    return errCode
                else:
                    debug(f'Exception: {oe}', "WARNING")
                    return -1

            for ticker in weights:
                try:
                    ins_query = f'INSERT INTO {table_name} (port_id, ticker, weight) ' \
                                f'VALUES (\'{port_id}\', \'{ticker}\', \'{weights[ticker]}\')'
                    connection.execute(ins_query)
                except sqlalchemy.exc.OperationalError as oe:
                    if oe.orig.args[0] == 1213:
                        debug(f'Exception: {oe}', "WARNING")
                        sleep(0.9)
                        errCode = update_portfolio_allocation(port_id=port_id, weights=weights,
                                                              recursion_count=recursion_count + 1)
                        return errCode
                    else:
                        debug(f'Exception: {oe}', "WARNING")
                        return -1
            transaction.commit()
            return 0


def get_portfolio_allocation(port_id, table_name=PORTFOLIO_ALLOCATION_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            get_query = f'SELECT ticker, weight FROM {table_name} WHERE port_id=\'{port_id}\''
            get_result = connection.execute(get_query)
            return get_result.fetchall() if get_result.rowcount > 0 else None


# ============ Returns ============
def create_portfolio_returns_table(table_name=PORTFOLIO_RETURNS_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if not is_table_exist(table_name):
            transaction = connection.begin()
            create_query = f'CREATE TABLE {table_name} ' \
                           f'(port_id VARCHAR(100) NOT NULL, ' \
                           f'rdate DATE NOT NULL, ' \
                           f'ret DOUBLE, ' \
                           f'PRIMARY KEY(port_id, rdate)' \
                           f')'
            connection.execute(create_query)
            transaction.commit()


def append_portfolio_returns(port_id, ret, ret_date=date.today(),
                             table_name=PORTFOLIO_RETURNS_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            transaction = connection.begin()
            ins_query = f'INSERT INTO {table_name} (port_id, rdate, ret) ' \
                        f'VALUES (\'{port_id}\', \'{ret_date}\', \'{ret}\')'
            connection.execute(ins_query)
            transaction.commit()


def insert_portfolio_returns(port_id, returns, table_name=PORTFOLIO_RETURNS_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            transaction = connection.begin()
            for rdate in returns:
                exist_query = f'SELECT * FROM {table_name} WHERE port_id=\'{port_id}\' AND rdate=\'{str(rdate)}\''
                exist_result = connection.execute(exist_query)
                if exist_result.rowcount == 1:
                    update_query = f'UPDATE {table_name} ' \
                                   f'SET ret=\'{str(returns[rdate])}\' ' \
                                   f'WHERE port_id=\'{port_id}\' AND rdate=\'{str(rdate)}\''
                    connection.execute(update_query)
                else:
                    ins_query = f'INSERT INTO {table_name} (port_id, rdate, ret) ' \
                                f'VALUES (\'{port_id}\', \'{str(rdate)}\', \'{str(returns[rdate])}\')'
                    connection.execute(ins_query)
            transaction.commit()


def get_portfolio_returns(port_id, start_date=None, end_date=date.today(),
                          table_name=PORTFOLIO_RETURNS_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            query_string = f'SELECT rdate, ret FROM {table_name} ' \
                           f' WHERE port_id=\'{port_id}\' '
            if start_date is not None:
                query_string += f' AND rdate >= \'{str(start_date)}\' '
            if end_date is not None:
                query_string += f' AND rdate <= \'{str(end_date)}\' '
            query_string += f' ORDER BY rdate ASC'
            q_result = connection.execute(query_string)
            return q_result.fetchall() if q_result.rowcount > 0 else None


def get_portfolio_returns_df(port_id, start_date=None, end_date=date.today(),
                             table_name=PORTFOLIO_RETURNS_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        portfolio_returns = None
        if is_table_exist(table_name):
            query_string = f'SELECT rdate, ret FROM {table_name} ' \
                           f' WHERE port_id=\'{port_id}\' '
            if start_date is not None:
                query_string += f' AND rdate >= \'{str(start_date)}\' '
            if end_date is not None:
                query_string += f' AND rdate <= \'{str(end_date)}\' '
            query_string += f' ORDER BY rdate ASC'
            q_result = connection.execute(query_string)
            if q_result.rowcount > 0:
                rows = q_result.fetchall()
                c0 = []
                c1 = []
                for row in rows:
                    rdate = pd.to_datetime(row[0], errors="coerce")
                    c0.append(rdate)
                    c1.append(row[1])
                portfolio_returns = pd.Series(c1, index=c0)
            portfolio_returns.index.name = 'Date'
            return portfolio_returns


def get_portfolio_returns_ti(port_id, time_interval=None, interval_type="Y",
                             table_name=PORTFOLIO_RETURNS_TABLE_NAME, engine=engine):
    start_date = None
    end_date = date.today()
    if time_interval is not None and time_interval > 0:
        td = timedelta(time_interval)
        start_date = end_date - td
    elif interval_type is not None:
        if interval_type == "Y":
            td = timedelta(365)
            start_date = end_date - td
        elif interval_type == "YTD":
            start_date = date(end_date.year, 1, 1)

    with engine.connect() as connection:
        if is_table_exist(table_name):
            query_string = f'SELECT rdate, ret FROM {table_name} ' \
                           f' WHERE port_id=\'{port_id}\' '
            if start_date is not None:
                query_string += f' AND rdate >= \'{str(start_date)}\' '
            if end_date is not None:
                query_string += f' AND rdate <= \'{str(end_date)}\' '
            query_string += f' ORDER BY rdate ASC'
            q_result = connection.execute(query_string)
            return q_result.fetchall() if q_result.rowcount > 0 else None


# ============ Bars ============
def create_portfolio_bars_table(table_name=PORTFOLIO_BARS_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if not is_table_exist(table_name):
            transaction = connection.begin()
            create_query = f'CREATE TABLE {table_name} ' \
                           f'(port_id VARCHAR(100) NOT NULL, ' \
                           f'bdate DATE, ' \
                           f'open  DOUBLE, ' \
                           f'high DOUBLE NOT NULL, ' \
                           f'low DOUBLE NOT NULL, ' \
                           f'close DOUBLE NOT NULL, ' \
                           f'adjclose DOUBLE NOT NULL, ' \
                           f'PRIMARY KEY(port_id, bdate)' \
                           f')'
            connection.execute(create_query)
            transaction.commit()


def insert_portfolio_bars(port_id, bar_list, table_name=PORTFOLIO_BARS_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            transaction = connection.begin()
            for bar in bar_list:
                bar_date, o, h, l, c, ac = bar
                exist_query = f'SELECT * FROM {table_name} WHERE port_id=\'{port_id}\' AND bdate=\'{str(bar_date)}\''
                exist_result = connection.execute(exist_query)
                if exist_result.rowcount == 1:
                    update_query = f'UPDATE {table_name} ' \
                                   f'SET open=\'{str(o)}\', high=\'{str(h)}\', low=\'{str(l)}\', close=\'{str(c)}\', ' \
                                   f'adjclose=\'{str(ac)}\'' \
                                   f'WHERE port_id=\'{port_id}\' AND bdate=\'{str(bar_date)}\''
                    connection.execute(update_query)
                else:
                    ins_query = f'INSERT INTO {table_name} (port_id, bdate, open, high, low, close, adjclose) ' \
                                f'VALUES (\'{port_id}\', \'{str(bar_date)}\', ' \
                                f'\'{str(o)}\', \'{str(h)}\', \'{str(l)}\', \'{str(c)}\', \'{str(ac)}\')'
                    connection.execute(ins_query)
            transaction.commit()


def append_portfolio_bar(port_id, bopen, bhigh, blow, bclose, bar_date=date.today(),
                         table_name=PORTFOLIO_BARS_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            transaction = connection.begin()
            ins_query = f'INSERT INTO {table_name} (port_id, bdate, open, high, low, close) ' \
                        f'VALUES (\'{port_id}\', \'{bar_date}\', \'{bopen}\', \'{bhigh}\', \'{blow}\', \'{bclose}\')'
            connection.execute(ins_query)
            transaction.commit()


def get_portfolio_bars(port_id, start_date=None, end_date=date.today(),
                       table_name=PORTFOLIO_BARS_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            query_string = f'SELECT bdate, open, high, low, close FROM {table_name} ' \
                           f' WHERE port_id=\'{port_id}\' '
            if start_date is not None:
                query_string += f' AND bdate >= \'{str(start_date)}\' '
            if end_date is not None:
                query_string += f' AND bdate <= \'{str(end_date)}\' '
            query_string += f' ORDER BY bdate ASC'
            q_result = connection.execute(query_string)
            return q_result.fetchall() if q_result.rowcount > 0 else None


def get_portfolio_bars_ti(port_id, time_interval=None, interval_type="Y",
                          table_name=PORTFOLIO_BARS_TABLE_NAME, engine=engine):
    start_date = None
    end_date = date.today()
    if time_interval is not None and time_interval > 0:
        td = timedelta(time_interval)
        start_date = end_date - td
    elif interval_type is not None:
        if interval_type == "Y":
            td = timedelta(365)
            start_date = end_date - td
        elif interval_type == "YTD":
            start_date = date(end_date.year, 1, 1)

    with engine.connect() as connection:
        if is_table_exist(table_name):
            query_string = f'SELECT bdate, open, high, low, close FROM {table_name} ' \
                           f' WHERE port_id=\'{port_id}\' '
            if start_date is not None:
                query_string += f' AND bdate >= \'{str(start_date)}\' '
            if end_date is not None:
                query_string += f' AND bdate <= \'{str(end_date)}\' '
            query_string += f' ORDER BY bdate ASC'
            q_result = connection.execute(query_string)
            return q_result.fetchall() if q_result.rowcount > 0 else None


# ============================================ Historical allocations ============================================
def create_hist_port_allocation_table(table_name=HIST_PORT_ALLOCATION_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if not is_table_exist(table_name):
            transaction = connection.begin()
            create_query = f'CREATE TABLE {table_name} ' \
                           f'(port_id VARCHAR(100) NOT NULL, ' \
                           f'adate DATE, ' \
                           f'ticker VARCHAR(6), ' \
                           f'weight DOUBLE, ' \
                           f'PRIMARY KEY(port_id, adate, ticker, weight)' \
                           f')'
            connection.execute(create_query)
            transaction.commit()


def update_hist_port_allocation(port_id, weights, allo_date=date.today(), overwrite=False,
                                table_name=HIST_PORT_ALLOCATION_TABLE_NAME, engine=engine,
                                recursion_count=0):
    if recursion_count == RECURSION_DEPTH:
        return -1
    with engine.connect() as connection:
        if is_table_exist(table_name):
            transaction = connection.begin()
            if overwrite:
                try:
                    del_query = f'DELETE FROM {table_name} WHERE port_id=\'{port_id}\' AND adate=\'{str(allo_date)}\''
                    connection.execute(del_query)
                except sqlalchemy.exc.OperationalError as oe:
                    if oe.orig.args[0] == 1213:
                        debug(f'Exception: {oe}', "WARNING")
                        sleep(0.9)
                        errCode = update_hist_port_allocation(port_id=port_id, weights=weights, allo_date=allo_date,
                                                              recursion_count=recursion_count + 1)
                        return errCode
                    else:
                        debug(f'Exception: {oe}', "WARNING")
                        return -1

                for ticker in weights:
                    try:
                        ins_query = f'INSERT INTO {table_name} (port_id, adate, ticker, weight) ' \
                                    f'VALUES (\'{port_id}\', \'{str(allo_date)}\', \'{ticker}\', \'{weights[ticker]}\')'
                        connection.execute(ins_query)
                    except sqlalchemy.exc.OperationalError as oe:
                        if oe.orig.args[0] == 1213:
                            debug(f'Exception: {oe}', "WARNING")
                            sleep(0.9)
                            errCode = update_hist_port_allocation(port_id=port_id, weights=weights, allo_date=allo_date,
                                                                  recursion_count=recursion_count + 1)
                            return errCode
                        else:
                            debug(f'Exception: {oe}', "WARNING")
                            return -1
                transaction.commit()
                return 0
            else:  #не перезаписываем по умолчанию
                sel_query = f'SELECT * from {table_name} ' \
                            f'WHERE port_id=\'{port_id}\' AND adate=\'{str(allo_date)}\''

                q_result = connection.execute(sel_query)
                if q_result.rowcount == 0:
                    for ticker in weights:
                        try:
                            ins_query = f'INSERT INTO {table_name} (port_id, adate, ticker, weight) ' \
                                        f'VALUES (\'{port_id}\', \'{str(allo_date)}\', \'{ticker}\', \'{weights[ticker]}\')'
                            connection.execute(ins_query)
                        except sqlalchemy.exc.OperationalError as oe:
                            if oe.orig.args[0] == 1213:
                                debug(f'Exception: {oe}', "WARNING")
                                sleep(0.9)
                                errCode = update_hist_port_allocation(port_id=port_id, weights=weights,
                                                                      allo_date=allo_date,
                                                                      recursion_count=recursion_count + 1)
                                return errCode
                            else:
                                debug(f'Exception: {oe}', "WARNING")
                                return -1
                transaction.commit()
                return 0


def get_hist_port_allocation(port_id, allo_date, table_name=HIST_PORT_ALLOCATION_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            get_query = f'SELECT ticker, weight ' \
                        f'FROM {table_name} ' \
                        f'WHERE port_id=\'{port_id}\' AND adate=\'{str(allo_date)}\''
            get_result = connection.execute(get_query)
            return get_result.fetchall() if get_result.rowcount > 0 else None

