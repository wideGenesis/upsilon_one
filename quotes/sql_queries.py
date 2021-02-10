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
            try:
                create_query = f'CREATE TABLE {table_name} ' \
                               f'(ticker VARCHAR(6) NOT NULL, ' \
                               f'dateTime DATE, ' \
                               f'open  DOUBLE, ' \
                               f'high DOUBLE NOT NULL, ' \
                               f'low DOUBLE NOT NULL, ' \
                               f'close DOUBLE NOT NULL, ' \
                               f'adj_close DOUBLE NOT NULL, ' \
                               f'volume BIGINT NOT NULL, ' \
                               f'dividend DOUBLE NOT NULL, ' \
                               f'PRIMARY KEY(ticker, dateTime)' \
                               f')'
                connection.execute(create_query)
            except Exception as e:
                debug(e, ERROR)
                transaction.rollback()
            transaction.commit()


def insert_quotes(ticker, quotes, is_update=True, table_name=QUOTE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            values_amount = 0
            insert_query = f'INSERT INTO {table_name} ' \
                           f'(ticker, dateTime, open, high, low, close, adj_close, volume, dividend) ' \
                           f'VALUES '
            for count, qdate in enumerate(quotes, start=1):
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
                    insert_query += f'(\'{ticker}\', \'{str(qdate)}\', ' \
                                   f'\'{str(o)}\', \'{str(h)}\', \'{str(l)}\', \'{str(c)}\', \'{str(ac)}\', ' \
                                   f'\'{str(v)}\', \'{str(d)}\')'
                    if count == len(quotes):
                        insert_query += ";"
                    else:
                        insert_query += ", "
                    values_amount += 1
            if values_amount > 0:
                connection.execute(insert_query)
                transaction.commit()
        except Exception as e:
            debug(e, ERROR)
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
                    query_string += f' AND q.dateTime < \'{str(end_date)}\' '
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
                else:
                    debug("WARNING data is empty", WARNING)
                    debug(f"{query_string}", WARNING)
            closes = pd.DataFrame(dat)
            return closes
        tickers = get_universe(cap_filter, u_table_name, engine)
        for ticker, _ in tickers.items():
            query_string = f'SELECT q.dateTime, q.close FROM {q_table_name} q, {u_table_name} u' \
                           f' WHERE q.ticker=\'{ticker}\' AND q.ticker=u.ticker '
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
            else:
                debug("WARNING data is empty", WARNING)
                debug(f"{query_string}", WARNING)
        closes = pd.DataFrame(dat)
    return closes, tickers


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
            # query_string = f'SELECT q.dateTime, q.close FROM {q_table_name} q, {u_table_name} u' \
            #                f' WHERE q.ticker=\'{ticker}\' AND q.ticker=u.ticker '
            query_string = f'SELECT q.dateTime, q.close FROM {q_table_name} q ' \
                           f' WHERE q.ticker=\'{ticker}\' '
            if start_date is not None:
                query_string += f' AND q.dateTime >= \'{str(start_date)}\' '
            if end_date is not None:
                query_string += f' AND q.dateTime < \'{str(end_date)}\' '
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
            else:
                debug(f"Closes by ticker list is EMPTY!", WARNING)
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
            query_string += f' AND q.dateTime < \'{str(end_date)}\' '
        query_string += f' ORDER BY q.dateTime ASC'

        q_result = connection.execute(query_string)
        if q_result.rowcount > 0:
            rows = q_result.fetchall()
            for row in rows:
                ticker, dat, o, h, l, c, weight, ac = row
                if ticker in ohlc:
                    ohlc[ticker].append((dat, o, h, l, c, weight, ac))
                else:
                    ohlc[ticker] = [(dat, o, h, l, c, weight, ac)]
    return ohlc


def get_ohlc_dict_by_ticker(ticker, start_date=None, end_date=date.today(),
                            q_table_name=QUOTE_TABLE_NAME, u_table_name=UNIVERSE_TABLE_NAME,
                            engine=engine):
    with engine.connect() as connection:
        ohlc = {}
        query_string = f'SELECT q.dateTime, q.open, q.high, q.low, q.close, q.adj_close ' \
                       f'FROM {q_table_name} q ' \
                       f'WHERE q.ticker=\'{ticker}\' '
        if start_date is not None:
            query_string += f' AND q.dateTime >= \'{str(start_date)}\' '
        if end_date is not None:
            query_string += f' AND q.dateTime < \'{str(end_date)}\' '
        query_string += f' ORDER BY q.dateTime ASC'

        q_result = connection.execute(query_string)
        if q_result.rowcount > 0:
            rows = q_result.fetchall()
            for row in rows:
                dat, o, h, l, c, ac = row
                ohlc[dat] = [(o, h, l, c, ac)]
    return ohlc


def get_ohlc_dict_by_port_id_h(port_id, start_date=None, end_date=date.today(),
                                 q_table_name=QUOTE_TABLE_NAME, u_table_name=UNIVERSE_TABLE_NAME,
                                 engine=engine):
    with engine.connect() as connection:
        weight_table = PORTFOLIO_ALLOCATION_TABLE_NAME
        ohlc = {}
        if start_date is None:
            td = timedelta(365)
            start_date = end_date - td
        query_string = f'SELECT q.ticker, q.dateTime, q.open, q.high, q.low, q.close, w.weight, q.adj_close ' \
                       f'FROM {q_table_name} q, {weight_table} w' \
                       f' WHERE q.ticker=w.ticker ' \
                       f' AND w.port_id=\'{port_id}\''
        if start_date is not None:
            query_string += f' AND q.dateTime >= \'{str(start_date)}\' '
        if end_date is not None:
            query_string += f' AND q.dateTime < \'{str(end_date)}\' '
        query_string += f' ORDER BY q.dateTime ASC'

        q_result = connection.execute(query_string)
        if q_result.rowcount > 0:
            rows = q_result.fetchall()
            for row in rows:
                ticker, dat, o, h, l, c, weight, ac = row
                if ticker in ohlc:
                    ohlc[ticker].append((dat, o, h, l, c, weight, ac))
                else:
                    ohlc[ticker] = [(dat, o, h, l, c, weight, ac)]
    return ohlc


def get_ohlc_dict_by_port_id_w(port_id, start_date=None, end_date=date.today(),
                               q_table_name=QUOTE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        res = {}
        td = timedelta(days=1)
        if start_date is None:
            ytd = timedelta(365)
            start_date = end_date - ytd
        curr_date = start_date
        count = 0
        while curr_date < end_date:
            allo_date = curr_date
            if curr_date.day > 1:
                allo_date = datetime.date(curr_date.year, curr_date.month, 1)
            allo_date -= td
            allo = get_port_allocation_by_date(port_id=port_id, allo_date=allo_date)
            debug(f'Allo by date [{str(allo_date)}]:{allo}')

            e_date = add_months(curr_date, 1)
            e_date = datetime.date(e_date.year, e_date.month, 1)
            if e_date > end_date:
                e_date = end_date
            ohlc = {}
            for ticker, weight in allo.items():
                query_string = f'SELECT q.dateTime, q.open, q.high, q.low, q.close, q.adj_close ' \
                               f' FROM {q_table_name} q ' \
                               f' WHERE q.ticker=\'{ticker}\' ' \
                               f' AND q.dateTime >= \'{str(curr_date)}\' ' \
                               f' AND q.dateTime < \'{str(e_date)}\' ' \
                               f' ORDER BY q.dateTime ASC'
                q_result = connection.execute(query_string)
                if q_result.rowcount > 0:
                    rows = q_result.fetchall()
                    for row in rows:
                        dat, o, h, l, c, ac = row
                        if ticker in ohlc:
                            ohlc[ticker].append((dat, o, h, l, c, weight, ac))
                        else:
                            ohlc[ticker] = [(dat, o, h, l, c, weight, ac)]
            res[count] = ohlc
            count += 1
            curr_date = e_date
    return res


def get_all_tickers_fom_quotes(q_table_name=QUOTE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        res = []
        if is_table_exist(q_table_name):
            sel_query = f'SELECT ticker FROM {q_table_name} GROUP BY ticker'
            result = connection.execute(sel_query)
            if result.rowcount > 0:
                query_result = result.fetchall()
                for ticker in query_result:
                    res.append(ticker[0])
            else:
                debug(f"WARNING. Can't find data in {q_table_name}", WARNING)
        else:
            debug(f'Can\'t find table: {q_table_name}!', WARNING)
    return res


def get_port_allocation_by_date(port_id, allo_date, table_name=HIST_PORT_ALLOCATION_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            res = {}
            get_query = f'SELECT ticker, weight ' \
                        f'FROM {table_name} ' \
                        f'WHERE port_id=\'{port_id}\' AND adate=\'{str(allo_date)}\''
            get_result = connection.execute(get_query)
            if get_result.rowcount > 0:
                debug(f"SQL:{get_query}")
                rows = get_result.fetchall()
                for row in rows:
                    ticker, weight = row
                    res[ticker] = weight
            else:
                get_query = f'SELECT ticker, weight ' \
                            f'FROM {table_name} ' \
                            f'WHERE port_id=\'{port_id}\' ' \
                            f'AND adate=(SELECT min(a.adate) FROM {table_name} a WHERE a.port_id=\'{port_id}\')'
                get_result = connection.execute(get_query)
                if get_result.rowcount > 0:
                    debug(f"SQL:{get_query}")
                    rows = get_result.fetchall()
                    for row in rows:
                        ticker, weight = row
                        res[ticker] = weight
            return res


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


def get_close_ticker_by_date(ticker, tdate=date.today(), q_table_name=QUOTE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        pclose = None
        if ticker_lookup(ticker):
            query_string = f'SELECT close FROM {q_table_name} ' \
                           f'WHERE ticker=\'{ticker}\' AND dateTime<=\'{str(tdate)}\' ' \
                           f'ORDER BY dateTime DESC ' \
                           f'LIMIT 1'
            q_result = connection.execute(query_string)
            if q_result.rowcount > 0:
                pclose = q_result.fetchone()[0]
        else:
            debug(f'Can\'t find ticker: {ticker}!', ERROR)
    return pclose


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


def get_universe(cap_filter=0, table_name=UNIVERSE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            absolute_filter = None
            percent_filter = None
            res = {}
            if isinstance(cap_filter, str):
                percent_filter = int(cap_filter[:-1])
            elif isinstance(cap_filter, int):
                absolute_filter = cap_filter
            sel_query = f'SELECT ticker, mkt_cap FROM  {table_name} ' \
                        f'WHERE mkt_cap IS NOT NULL '
            if absolute_filter is not None:
                sel_query += f'AND mkt_cap > \'{absolute_filter}\' '
            sel_query += f'ORDER BY mkt_cap DESC'
            result = connection.execute(sel_query)
            if result.rowcount > 0:
                query_result = result.fetchall()
                for count, item in enumerate(query_result):
                    res[item[0]] = item[1]
                    if percent_filter is not None and count >= round((len(query_result)*percent_filter)/100):
                        break
                return res
            else:
                return None
        else:
            debug(f'Can\'t find table: {table_name}!')


def get_universe_for_update(table_name=UNIVERSE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            res = []
            sel_query = f'SELECT ticker FROM  {table_name} '
            result = connection.execute(sel_query)
            if result.rowcount > 0:
                query_result = result.fetchall()
                for item in query_result:
                    res.append(item[0])
                return res
            else:
                return None
        else:
            debug(f'Can\'t find table: {table_name}!')


def get_universe_capweighted(table_name=UNIVERSE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            res = list()
            del_query = f'SELECT ticker FROM {table_name} ' \
                        f'ORDER BY mkt_cap DESC'
            result = connection.execute(del_query)
            if result.rowcount > 0:
                query_result = result.fetchall()
                for count, ticker in enumerate(query_result):
                    res.append(ticker[0])
                    if count >= round(len(query_result)/2):
                        break
                return res
            else:
                return None
        else:
            debug(f'Can\'t find table: {table_name}!')


def get_all_uniq_tickers(engine=engine):
    current_universe = UNIVERSE_TABLE_NAME
    hist_universe = HIST_UNIVERSE_TABLE_NAME
    tinkoff_universe = TINKOFF_UNIVERSE_TABLE_NAME
    hist_tinkoff_universe = TINKOFF_HIST_UNIVERSE_TABLE_NAME
    quote = QUOTE_TABLE_NAME
    table_list = [current_universe, hist_universe, tinkoff_universe, hist_tinkoff_universe, quote]
    uniq_tickers = []
    with engine.connect() as connection:
        for table in table_list:
            if is_table_exist(table):
                sel_query = f'SELECT ticker FROM {table} GROUP BY ticker'
                result = connection.execute(sel_query)
                if result.rowcount > 0:
                    query_result = result.fetchall()
                    for ticker in query_result:
                        uniq_tickers.append(ticker[0])
                else:
                    debug(f"WARNING. Can't find data in {table}", WARNING)
            else:
                debug(f'Can\'t find table: {table}!', WARNING)
    return uniq_tickers


def get_all_universe(table_name=UNIVERSE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            res = {}
            del_query = "SELECT ticker, sector, mkt_cap, exchange FROM " + table_name
            result = connection.execute(del_query)
            if result.rowcount > 0:
                for t in result.fetchall():
                    res[t[0]] = (t[1], t[2], t[3])
                return res
            else:
                return None
        else:
            debug(f'Can\'t find table: {table_name}!')


def find_min_date(tisker_list, table_name=QUOTE_TABLE_NAME):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            min_dates = {}
            for ticker in tisker_list:
                if ticker_lookup(ticker):
                    sql_query = f'SELECT min(q.dateTime) FROM {table_name} q ' \
                                f'WHERE q.ticker=\'{ticker}\''
                    result = connection.execute(sql_query)
                    if result.rowcount > 0:
                        min_dates[ticker] = result.cursor.fetchone()[0]
                    else:
                        return None, ticker
                else:
                    return None, None
            md = max(min_dates.values())
            ticker = list(min_dates.keys())[list(min_dates.values()).index(md)]
            return md, ticker
        else:
            debug(f'Can\'t find table: {table_name}!')


def find_min_date_by_ticker(ticker, table_name=QUOTE_TABLE_NAME):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            if ticker_lookup(ticker):
                sql_query = f'SELECT min(q.dateTime) FROM {table_name} q ' \
                            f'WHERE q.ticker=\'{ticker}\''
                result = connection.execute(sql_query)
                if result.rowcount > 0:
                    md = result.cursor.fetchone()[0]
                    return md
                else:
                    return None
        else:
            debug(f'Can\'t find table: {table_name}!')


def find_max_date_by_ticker(ticker, table_name=QUOTE_TABLE_NAME):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            if ticker_lookup(ticker):
                sql_query = f'SELECT max(q.dateTime) FROM {table_name} q ' \
                            f'WHERE q.ticker=\'{ticker}\''
                result = connection.execute(sql_query)
                if result.rowcount > 0:
                    md = result.cursor.fetchone()[0]
                    return md
                else:
                    return None
        else:
            debug(f'Can\'t find table: {table_name}!')


# ******************** HISTORICAL UNIVERSE ********************
def create_hist_universe_table(table_name=HIST_UNIVERSE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if not is_table_exist(table_name):
            transaction = connection.begin()
            create_query = f'CREATE TABLE {table_name} ' \
                           f'(udate DATE NOT NULL, ' \
                           f'ticker VARCHAR(6) NOT NULL, ' \
                           f'mkt_cap BIGINT, ' \
                           f'sector VARCHAR(100), ' \
                           f'exchange VARCHAR(20), ' \
                           f'PRIMARY KEY(udate, ticker)' \
                           f')'
            connection.execute(create_query)
            transaction.commit()


def append_universe_by_date(universe, universe_date, table_name=HIST_UNIVERSE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(table_name):
            transaction = connection.begin()
            try:
                for ticker in universe:
                    sector, mkt_cap, exchange = universe[ticker]
                    insert_query = f'INSERT INTO {table_name} (udate, ticker, mkt_cap, sector, exchange) ' \
                                   f'VALUES (\'{str(universe_date)}\', ' \
                                   f'\'{ticker}\', \'{mkt_cap}\', \'{sector}\', \'{exchange}\')'
                    connection.execute(insert_query)
                transaction.commit()
            except Exception as e:
                debug(e, "ERROR")
                transaction.rollback()
        else:
            debug(f'Can\'t find table: {table_name}!')


def get_all_universe_by_date(universe_date, cap_filter=0, u_table_name=HIST_UNIVERSE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(u_table_name):
            res = {}
            absolute_filter = None
            percent_filter = None
            if isinstance(cap_filter, str):
                percent_filter = int(cap_filter[:-1])
            elif isinstance(cap_filter, int):
                absolute_filter = cap_filter
            del_query = f'SELECT ticker, sector, mkt_cap, exchange FROM  {u_table_name} ' \
                        f'WHERE udate=\'{str(universe_date)}\'  ' \
                        f'AND mkt_cap IS NOT NULL '
            if absolute_filter is not None:
                del_query += f'AND mkt_cap > \'{absolute_filter}\' '
            del_query += f'ORDER BY mkt_cap DESC'
            result = connection.execute(del_query)
            if result.rowcount > 0:
                query_result = result.fetchall()
                for count, item in enumerate(query_result):
                    res[item[0]] = (item[1], item[2], item[3])
                    if percent_filter is not None and count >= round((len(query_result)*percent_filter)/100):
                        break
                return res
            else:
                return None
        else:
            debug(f'Can\'t find table: {u_table_name}!')


def get_universe_by_date(universe_date, cap_filter=0, u_table_name=HIST_UNIVERSE_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if is_table_exist(u_table_name):
            res = {}
            absolute_filter = None
            percent_filter = None
            if isinstance(cap_filter, str):
                percent_filter = int(cap_filter[:-1])
            elif isinstance(cap_filter, int):
                absolute_filter = cap_filter
            sel_query = f'SELECT ticker, mkt_cap FROM  {u_table_name} ' \
                        f'WHERE udate=\'{str(universe_date)}\'  ' \
                        f'AND mkt_cap IS NOT NULL '
            if absolute_filter is not None:
                sel_query += f'AND mkt_cap > \'{absolute_filter}\' '
            sel_query += f'ORDER BY mkt_cap DESC'
            result = connection.execute(sel_query)
            if result.rowcount > 0:
                query_result = result.fetchall()
                for count, item in enumerate(query_result):
                    res[item[0]] = item[1]
                    if percent_filter is not None and count >= round((len(query_result)*percent_filter)/100):
                        break
                return res
            else:
                debug(f"Universe by: universe_date={str(universe_date)} : cap_filter={cap_filter} is Empty!!", WARNING)
                return None
        else:
            debug(f'Can\'t find table: {u_table_name}!')


def get_closes_universe_by_date_df(universe_date, q_table_name=QUOTE_TABLE_NAME, u_table_name=HIST_UNIVERSE_TABLE_NAME,
                                   cap_filter=0, etf_list=None, start_date=None, end_date=date.today(), engine=engine):
    with engine.connect() as connection:
        closes = None
        dat = {}
        universe = get_universe_by_date(universe_date, cap_filter, u_table_name, engine)
        # debug(f"Universe size: {len(universe)}")
        for ticker, mkt_cap in universe.items():
            query_string = f'SELECT q.dateTime, q.close FROM {q_table_name} q' \
                           f' WHERE q.ticker=\'{ticker}\''
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
            else:
                debug(f"Closes by date {str(universe_date)} is empty!!! ", WARNING)
        closes = pd.DataFrame(dat)
    return closes, universe

