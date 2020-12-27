import pandas as pd
import cmath
import os
from quotes.sql_queries import *
from yahoofinancials import YahooFinancials
from datetime import datetime
import yfinance as yhoo


# Формат даты в сторку
def dt_to_str(date: datetime) -> str:
    return "%04d-%02d-%02d" % (date.year, date.month, date.day)


# Формат строки в дату
def str_to_dt(string: str) -> datetime:
    return datetime.strptime(string, '%Y-%m-%d')


# Формат листа со строками в лист с датами из файла
def str_list_to_date(file: pd.DataFrame):
    try:
        file["Date"] = pd.to_datetime(file["Date"], dayfirst=False)
    except ValueError:
        file["Date"] = pd.to_datetime(file["Date"], format='%d-%m-%Y')


# Округление числа и конвертация его во float
def number_to_float(n) -> float:
    if empty_check(n):
        return round(float(n), 2)
    else:
        return n


# Округление числа и конвертация его в int
def number_to_int(n) -> int:
    if empty_check(n):
        return int(round(float(n), 0))
    else:
        return n


# Не пустой ли объект?
def empty_check(n) -> bool:
    return n is not None and n != 0 and not cmath.isnan(n)


# Скачиваем тикеры из яху (цены и дивиденды)
def download_yahoo(ticker, base_dir, start_date, end_date):
    try:
        yf = YahooFinancials(ticker)
        data = yf.get_historical_price_data(dt_to_str(start_date), dt_to_str(end_date), 'daily')
    except Exception as err:
        print(f'Unable to read data for {ticker}: {err}')
        return pd.DataFrame({})

    if data.get(ticker) is None or data[ticker].get('prices') is None or \
            data[ticker].get('timeZone') is None or len(data[ticker]['prices']) == 0:
        print(f'Yahoo: no data for {ticker}')
        return pd.DataFrame({})

    prices = {}
    for rec in sorted(data[ticker]['prices'], key=lambda r: r['date']):
        date = datetime.strptime(rec['formatted_date'], '%Y-%m-%d')
        dic_with_prices(prices, ticker, date, rec['open'], rec['high'], rec['low'], rec['close'], rec['volume'])

    if 'dividends' in data[ticker]['eventsData']:
        for date, rec in sorted(data[ticker]['eventsData']['dividends'].items(), key=lambda r: r[0]):
            date = datetime.strptime(date, '%Y-%m-%d')
            dic_with_div(prices, ticker, date, rec['amount'])

    if 'splits' in data[ticker]['eventsData']:
        for date, rec in sorted(data[ticker]['eventsData']['splits'].items(), key=lambda r: r[0]):
            date = datetime.strptime(date, '%Y-%m-%d')
            print(f"{ticker} has split {rec['splitRatio']} for {date}")

    frame = pd.DataFrame.from_dict(prices, orient='index',
                                   columns=['Open', 'High', 'Low', 'Close', 'Volume', 'Dividend'])
    save_csv(base_dir, ticker, frame, 'yahoo')


# Словарь с ценами
def dic_with_prices(prices: dict, ticker: str, date: datetime, open, high, low, close, adjclose, volume, dividend=0):
    if date.weekday() > 5:
        # print(f'Найден выходной в {ticker} на {date}')
        return

    open = number_to_float(open)
    high = number_to_float(high)
    low = number_to_float(low)
    close = number_to_float(close)
    adjclose = number_to_float(adjclose)
    volume = number_to_int(volume)

    error_price = (not empty_check(open)) or (not empty_check(high)) or (not empty_check(low)) or (
        not empty_check(close) or (not empty_check(adjclose)) )
    error_vol = not empty_check(volume)

    if error_price:
        # print(f'В {ticker} на {date} имеются пустые данные')
        return
    # if error_vol:
        # print(f'В {ticker} на {date} нет объёма')

    prices[date] = [open, high, low, close, adjclose, volume, dividend]


# Добавляем дивиденды к словарю с ценами
def dic_with_div(prices: dict, ticker: str, date: datetime, amount: float):
    if date.weekday() > 5:
        # print(f'Найден выходной в {ticker} на {date}')
        return

    dividend = amount
    error_price = not empty_check(dividend)

    if error_price:
        # print(f'В {ticker} на {date} имеются пустые данные в дивидендах')
        return

    prices[date][len(prices[date]) - 1] = dividend


# Блок работы с файлами ------------------------------------------------------------------------------------------------
# Сохраняем csv файл
def save_csv(base_dir: str, file_name: str, data: pd.DataFrame, source: str = 'new_file'):
    path = os.path.join(base_dir)
    if not os.path.exists(path):
        os.makedirs(path)

    if source == 'yahoo':
        print(f'{file_name} отработал через яху')
        path = os.path.join(path, file_name + '.csv')
        path = path.replace('^', '')
    elif source == 'new_file':
        print(f'Сохраняем файл с тикером {file_name}')
        path = os.path.join(path, file_name + '.csv')
    else:
        print(f'Неопознанный источник данных для {file_name}')

    if source == 'yahoo':
        data.to_csv(path, index_label='Date')
    else:
        data.to_csv(path, index=False)


# Загружаем csv файл
def load_csv(ticker: str, data_dir) -> pd.DataFrame:
    path = os.path.join(data_dir, str(ticker) + '.csv')
    file = pd.read_csv(path, parse_dates=True, index_col=0)
    if 'Date' in file.columns:
        str_list_to_date(file)
    return file


# *************** Download to DataBase ***************
# Скачиваем данные из яху (цены и дивиденды)
def download_quotes_to_db(ticker, start_date, end_date, is_update):
    try:
        yf = YahooFinancials(ticker)
        data = yf.get_historical_price_data(dt_to_str(start_date), dt_to_str(end_date), 'daily')
    except Exception as err:
        # print(f'Unable to read data for {ticker}: {err}')
        return pd.DataFrame({})

    if data.get(ticker) is None or data[ticker].get('prices') is None or \
            data[ticker].get('timeZone') is None or len(data[ticker]['prices']) == 0:
        # print(f'Yahoo: no data for {ticker}')
        return pd.DataFrame({})

    prices = {}
    for rec in sorted(data[ticker]['prices'], key=lambda r: r['date']):
        date = datetime.strptime(rec['formatted_date'], '%Y-%m-%d')
        dic_with_prices(prices, ticker, date, rec['open'], rec['high'], rec['low'], rec['close'],
                        rec['adjclose'], rec['volume'])

    if 'dividends' in data[ticker]['eventsData']:
        for date, rec in sorted(data[ticker]['eventsData']['dividends'].items(), key=lambda r: r[0]):
            date = datetime.strptime(date, '%Y-%m-%d')
            dic_with_div(prices, ticker, date, rec['amount'])

    if 'splits' in data[ticker]['eventsData']:
        for date, rec in sorted(data[ticker]['eventsData']['splits'].items(), key=lambda r: r[0]):
            date = datetime.strptime(date, '%Y-%m-%d')
            # print(f"{ticker} has split {rec['splitRatio']} for {date}")

    # print("PRICES:" + str(prices))
    insert_quotes(ticker, prices, is_update)


def get_sector_and_market_cap(ticker):
    tic = yhoo.Ticker(ticker)
    sector = tic.info.get('sector', None)
    mkt_cap = tic.info.get('marketCap', 0)
    return mkt_cap, sector
