from project_shared import *
import simfin as sf
from simfin.names import *
import pandas as pd


def find_mktcap(universe_date, ticker, cur_mkt_cap):
    sf.set_api_key('free')
    sf.set_data_dir(SIMFIN_PATH)
    df_all = sf.load_shareprices(variant='daily', market='us')
    df_cap = df_all.loc[ticker, [CLOSE, SHARES_OUTSTANDING]]
    df_cap = df_cap.dropna()
    dates = df_cap.index
    min_date = dates[0]
    max_date = dates[-1]
    ud = pd.to_datetime(universe_date)
    mkt_cap = 0
    if ud in dates:
        dbyd = df_cap.loc[ud]
        close = dbyd[CLOSE]
        so = dbyd[SHARES_OUTSTANDING]
        mkt_cap = close * so
        debug(f"{ticker} : Market Cap={mkt_cap}")
    elif ud < min_date:
        dbyd = df_cap.loc[min_date]
        close = dbyd[CLOSE]
        so = dbyd[SHARES_OUTSTANDING]
        mkt_cap = close * so
        debug(f"{ticker} : Market Cap={mkt_cap}")
    elif min_date < ud < max_date:
        dbyd = df_cap.loc[ud:]
        ud = dbyd.index[0]
        debug(dbyd)
        dbyd = df_cap.loc[ud]
        close = dbyd[CLOSE]
        so = dbyd[SHARES_OUTSTANDING]
        mkt_cap = close * so
        debug(f"{ticker} : Market Cap={mkt_cap}")
    elif ud > max_date:
        mkt_cap = cur_mkt_cap
    return mkt_cap


if __name__ == '__main__':
    print(f"Starting scrapers {os.path.realpath(__file__)}, this may take a while")

    sf.set_api_key('free')

    # Set the local directory where data-files are stored.
    # The dir will be created if it does not already exist.
    sf.set_data_dir('~/simfin_data/')

    # Daily Share-Prices.
    df_cap = sf.load_shareprices(variant='daily', market='us')

    # Print the first rows of the data.
    print(df_cap.head())

    # Print all Revenue and Net Income for Microsoft (ticker MSFT).
    tmp = df_cap.loc['TCOM', [CLOSE, SHARES_OUTSTANDING]]

    print(df_cap.loc['MSFT', [CLOSE, SHARES_OUTSTANDING]])

