from finviz.screener import Screener
import pandas as pd


def percent_to_float(x):
    return float(x.strip('%'))


def cap_norm(x):
    try:

        if x[-1] == 'M':
            x = float(x.strip('M'))
            x = x * 1000000
        elif x[-1] == 'B':
            x = float(x.strip('B'))
            x = x * 1000000000
        else:
            return x
    except:
        return x
    return x


def get_picks(guru_picks=True):
    custom = ['1', '2', '3', '6', '43', '44', '46', '49', '59', '65']
    if guru_picks:
        filters = ['idx_sp500', 'ta_perf_26wup', 'ta_sma50_pa']
        filename = 'guru_stocks.csv'
    else:
        filters = ['cap_microover', 'ind_stocksonly', 'ipodate_more1', 'avgvol_o50',
                   'sh_price_u10', 'ta_perf_13wup', 'ta_sma50_pa']
        filename = 'odds_stocks.csv'

    get_stocks = Screener(filters=filters, table='Performance', order='price', custom=custom)
    get_stocks.to_csv(f'/home/gene/projects/upsilon_one/logs/{filename}')


def picks_ranking(guru_picks=True, path='/home/gene/projects/upsilon_one/logs/', filename='odds_stocks'):
    guru = pd.read_csv(f'{path}{filename}.csv', index_col='Ticker',
                       converters={'Perf Month': percent_to_float, 'Perf Quart': percent_to_float,
                                   'Perf Year': percent_to_float, 'Market Cap': cap_norm})
    if guru_picks:
        mk = 0.25
        qk = 0.35
        yk = 0.4
        cap = guru['Market Cap']

    else:
        mk = 0.20
        qk = 0.70
        yk = 0.10
        cap = 1

    guru['rank'] = (mk * guru['Perf Month'] + qk * guru['Perf Quart'] + yk * guru['Perf Year']) / guru['RSI'] * cap
    guru['daily_stop'] = round(guru['ATR'] / guru['Price'] * 100 * 2.71828, ndigits=2)
    guru.sort_values(by=['rank'], inplace=True, ascending=False)
    guru = guru[0:50]
    guru.drop(columns={'No.', 'Market Cap', 'Perf Month', 'Perf Quart', 'Perf Year', 'ATR', 'RSI', 'Price', 'rank'},
              inplace=True)
    guru.to_csv(f'{path}{filename}.csv')


# get_picks(guru_picks=True)
# picks_ranking(guru_picks=True, filename='guru_stocks.csv')

get_picks(guru_picks=False)
picks_ranking(guru_picks=False, filename='odds_stocks')
