from project_shared import *
from quotes.sql_queries import *
from quotes.yahoo_downloader import *
from datetime import timedelta, date, datetime
import pandas as pd

delta = 0.15


def validate_data():
    ticker = 'ADP'
    tickers = get_all_tickers_fom_quotes()
    today = date.today()
    start_date = datetime.strptime(DEFAULT_START_QUOTES_DATE, "%Y-%m-%d").date()
    db_ohlc = get_ohlc_dict_by_ticker(ticker=ticker, start_date=start_date, end_date=today)
    yhoo_ohlc = download_quotes_by_ticker(ticker, start_date, today)
    for dat, bar in yhoo_ohlc.items():
        if dat.date() not in db_ohlc:
            debug(f"[{ticker}][{str(dat)}] Не найдено в DB!!!", WARNING)
            continue
        dbo, dbh, dbl, dbc, dbac = db_ohlc[dat.date()][0]
        yo, yh, yl, yc, yac, _, _ = bar
        do = dbo - yo
        dh = dbh - yh
        dl = dbl - yl
        dc = dbc - yc
        dac = dbac - yac
        if abs(do) > delta or abs(dh) > delta or abs(dl) > delta or abs(dc) > delta or abs(dac) > delta:
            debug(f"Price difference", WARNING)
            debug(f"YH: O:{yo}  H:{yh}  L:{yl}  C:{yc}  AC:{yac}")
            debug(f"DB: O:{dbo}  H:{dbh}  L:{dbl}  C:{dbc}  AC:{dbac}")


if __name__ == '__main__':
    debug("### Start validate date ###")
    validate_data()
