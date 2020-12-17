#!/usr/bin/env python3

import os
import sys
import yaml
import logging
import inspect
import datetime
from sqlalchemy import create_engine
from alchemysession import AlchemySessionContainer

PYTHON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(PYTHON_PATH)
os.environ["PYTHONUNBUFFERED"] = "1"

i_path, i_filename = os.path.split(__file__)
print(f'##### {i_path}:{i_filename}')
conf = yaml.safe_load(open(f'{i_path}/config/settings.yaml'))

LOGS = conf['PATHS']['LOGS']
WEBDRIVER = conf['PATHS']['WEBDRIVER']
IMAGES_OUT_PATH = conf['PATHS']['IMAGES_OUT_PATH']
ETF_HOLDINGS_URL = conf['PATHS']['ETF_HOLDINGS_URL']

# ============================== Quote Loader ======================

DEFAULT_START_QUOTES_DATE = SQL_USER = conf['SQL']['DEFAULT_START_QUOTES_DATE']
UNIVERSE_TABLE_NAME = conf['SQL_TABLE_NAMES']['UNIVERSE_TABLE_NAME']
QUOTE_TABLE_NAME = conf['SQL_TABLE_NAMES']['QUOTE_TABLE_NAME']
PORTFOLIO_ALLOCATION_TABLE_NAME = conf['SQL_TABLE_NAMES']['PORTFOLIO_ALLOCATION_TABLE_NAME']
PORTFOLIO_RETURNS_TABLE_NAME = conf['SQL_TABLE_NAMES']['PORTFOLIO_RETURNS_TABLE_NAME']
PORTFOLIO_BARS_TABLE_NAME = conf['SQL_TABLE_NAMES']['PORTFOLIO_BARS_TABLE_NAME']
ETF_FOR_SCRAPE = conf['ETF_FOR_SCRAPE']
ETFs = conf['ETFs']
EXCLUDE_SECTORS = conf['EXCLUDE_SECTORS']
NOT_EXCLUDE_TICKERS = conf['NOT_EXCLUDE_TICKERS']

# ============================== Charter ======================
# *************** Settings for candlestick chart
IMAGE_WIDTH = conf['CHARTER_CANDLE_CHART']['IMAGE_WIDTH']
IMAGE_HEIGHT = conf['CHARTER_CANDLE_CHART']['IMAGE_HEIGHT']
TITLE_FONT_COLOR = conf['CHARTER_CANDLE_CHART']['TITLE_FONT_COLOR']
EXTRA_DAYS = conf['CHARTER_CANDLE_CHART']['EXTRA_DAYS']
AXIS_FONT_COLOR = conf['CHARTER_CANDLE_CHART']['AXIS_FONT_COLOR']
CHART_BACKGROUND_COLOR = conf['CHARTER_CANDLE_CHART']['CHART_BACKGROUND_COLOR']
OUTER_BACKGROUND_COLOR = conf['CHARTER_CANDLE_CHART']['OUTER_BACKGROUND_COLOR']
GRID_LINE_COLOR = conf['CHARTER_CANDLE_CHART']['GRID_LINE_COLOR']
WATERMARK_TEXT_COLOR = conf['CHARTER_CANDLE_CHART']['WATERMARK_TEXT_COLOR']
CANDLE_UP_COLOR = conf['CHARTER_CANDLE_CHART']['CANDLE_UP_COLOR']
CANDLE_DOWN_COLOR = conf['CHARTER_CANDLE_CHART']['CANDLE_DOWN_COLOR']
CANDLE_SHADOW_COLOR = conf['CHARTER_CANDLE_CHART']['CANDLE_SHADOW_COLOR']
COMPARISON_LINE_COLOR = conf['CHARTER_CANDLE_CHART']['COMPARISON_LINE_COLOR']

# *************** Settings for histogram chart
H_IMAGE_WIDTH = conf['CHARTER_HISTOGRAM']['IMAGE_WIDTH']
H_IMAGE_HEIGHT = conf['CHARTER_HISTOGRAM']['IMAGE_HEIGHT']
H_AXIS_FONT_COLOR = conf['CHARTER_HISTOGRAM']['AXIS_FONT_COLOR']
H_TITLE_FONT_COLOR = conf['CHARTER_HISTOGRAM']['TITLE_FONT_COLOR']
H_WATERMARK_TEXT_COLOR = conf['CHARTER_HISTOGRAM']['WATERMARK_TEXT_COLOR']
BAR_UP_COLOR = conf['CHARTER_HISTOGRAM']['BAR_UP_COLOR']
BAR_DOWN_COLOR = conf['CHARTER_HISTOGRAM']['BAR_DOWN_COLOR']
HIST_BACKGROUND_COLOR = conf['CHARTER_HISTOGRAM']['HIST_BACKGROUND_COLOR']

# ============================== SQL Connect ======================

SQL_DB_NAME = conf['SQL']['DB_NAME']
SQL_USER = conf['SQL']['DB_USER']
SQL_PASSWORD = conf['SQL']['DB_PASSWORD']
SQL_URI = 'mysql+pymysql://{}:{}@localhost/{}'.format(SQL_USER, SQL_PASSWORD, SQL_DB_NAME)

engine = create_engine(SQL_URI, pool_recycle=3600)
container = AlchemySessionContainer(engine=engine)
alchemy_session = container.new_session('default')


# ============================== Logging Setup ======================
# logging.basicConfig(
#     filemode='w',
#     filename=os.path.abspath('logs/invest_services.log'),
#     format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
#     level=logging.WARNING)
# logging.getLogger('scrapers').setLevel(level=logging.WARNING)


# Print iterations progress
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end=""):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        print_end    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()


def debug(print_string=""):
    caller_frame_record = inspect.stack()[1]
    frame = caller_frame_record[0]
    info = inspect.getframeinfo(frame)
    path, filename = os.path.split(info.filename)
    dt = datetime.datetime.now()
    print(f'\r[{dt.strftime("%H:%M:%S")}]{filename}:{info.lineno}:{print_string}')

