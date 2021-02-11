#!/usr/bin/env python3

import os
import sys
import yaml
import logging
import inspect
import datetime
import calendar
from sqlalchemy import create_engine
from alchemysession import AlchemySessionContainer
from PIL import Image, ImageDraw, ImageFont

PYTHON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(PYTHON_PATH)
os.environ["PYTHONUNBUFFERED"] = "1"

PROJECT_HOME_DIR, i_filename = os.path.split(__file__)
# print(f'##### {PROJECT_HOME_DIR}:{i_filename}')
conf_dir = f'{PROJECT_HOME_DIR}/config/'
conf = yaml.safe_load(open(f'{PROJECT_HOME_DIR}/config/settings.yaml'))

if os.path.exists(conf_dir+'local.conf'):
    print("Run local!!")

LOGS_PATH = PROJECT_HOME_DIR + '/logs/'

LOGS = conf['PATHS']['LOGS']
WEBDRIVER = conf['PATHS']['WEBDRIVER']
IMAGES_OUT_PATH = conf['PATHS']['IMAGES_OUT_PATH']
RESULTS_PATH = conf['PATHS']['RESULTS_PATH']
ETF_HOLDINGS_URL = conf['PATHS']['ETF_HOLDINGS_URL']

EOD_API_KEY = conf['EODHISTOCICALDATA']['API_KEY']
# ============================== Quote Loader ======================

DEFAULT_START_QUOTES_DATE = SQL_USER = conf['SQL']['DEFAULT_START_QUOTES_DATE']
UNIVERSE_TABLE_NAME = conf['SQL_TABLE_NAMES']['UNIVERSE_TABLE_NAME']
HIST_UNIVERSE_TABLE_NAME = conf['SQL_TABLE_NAMES']['HIST_UNIVERSE_TABLE_NAME']
TINKOFF_UNIVERSE_TABLE_NAME = conf['SQL_TABLE_NAMES']['TINKOFF_UNIVERSE_TABLE_NAME']
TINKOFF_HIST_UNIVERSE_TABLE_NAME = conf['SQL_TABLE_NAMES']['TINKOFF_HIST_UNIVERSE_TABLE_NAME']
QUOTE_TABLE_NAME = conf['SQL_TABLE_NAMES']['QUOTE_TABLE_NAME']
PORTFOLIO_ALLOCATION_TABLE_NAME = conf['SQL_TABLE_NAMES']['PORTFOLIO_ALLOCATION_TABLE_NAME']
HIST_PORT_ALLOCATION_TABLE_NAME = conf['SQL_TABLE_NAMES']['HIST_PORT_ALLOCATION_TABLE_NAME']
PORTFOLIO_RETURNS_TABLE_NAME = conf['SQL_TABLE_NAMES']['PORTFOLIO_RETURNS_TABLE_NAME']
PORTFOLIO_BARS_TABLE_NAME = conf['SQL_TABLE_NAMES']['PORTFOLIO_BARS_TABLE_NAME']
ETF_FOR_SCRAPE = conf['ETF_FOR_SCRAPE']
ETFs = conf['ETFs']
EXCLUDE_SECTORS = conf['EXCLUDE_SECTORS']
EXCLUDE_TICKERS = conf['EXCLUDE_TICKERS']
NOT_EXCLUDE_TICKERS = conf['NOT_EXCLUDE_TICKERS']
VALID_EXCHANGE = conf['VALID_EXCHANGE']
DELISTED_TICKERS = conf['DELISTED_TICKERS']
RECENTLY_DELISTED = conf['RECENTLY_DELISTED']
SIMFIN_PATH = "" + PROJECT_HOME_DIR + "/" + conf['PATHS']['SIMFIN_PATH']

# ============================== Portfolios ======================

PARKING = conf['PORTFOLIOS']['PARKING']
ALL_WEATHER = conf['PORTFOLIOS']['ALL_WEATHER']
BALANCED = conf['PORTFOLIOS']['BALANCED']
AGGRESSIVE = conf['PORTFOLIOS']['AGGRESSIVE']
LEVERAGED = conf['PORTFOLIOS']['LEVERAGED']
TEST_ADM = conf['PORTFOLIOS']['TEST_ADM']
SAC_PARKING = conf['PORTFOLIOS']['SAC_PARKING']
SAC_BALANCED = conf['PORTFOLIOS']['SAC_BALANCED']
SAC_GROWTH = conf['PORTFOLIOS']['SAC_GROWTH']

# ============================== Charter ======================
CHARTER_IMAGES_PATH = "" + PROJECT_HOME_DIR + "/" + conf['PATHS']['CHARTER_IMAGES_PATH']
STATS_PATH = "" + PROJECT_HOME_DIR + "/" + conf['PATHS']['STATS_PATH']
TESTER_RESULT_PATH = "" + PROJECT_HOME_DIR + "/" + conf['PATHS']['TESTER_RESULT_PATH']
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

# *************** Settings for pie chart
P_IMAGE_WIDTH = conf['CHARTER_PIE']['IMAGE_WIDTH']
P_IMAGE_HEIGHT = conf['CHARTER_PIE']['IMAGE_HEIGHT']
P_BACKGROUND_COLOR = conf['CHARTER_PIE']['PIE_BACKGROUND_COLOR']
P_TITLE_FONT_COLOR = conf['CHARTER_PIE']['TITLE_FONT_COLOR']
P_OUTER_BACKGROUND_COLOR = conf['CHARTER_PIE']['OUTER_BACKGROUND_COLOR']
P_AXIS_FONT_COLOR = conf['CHARTER_PIE']['AXIS_FONT_COLOR']

# ============================== SQL Connect ======================
if os.path.exists(conf_dir+'local.conf'):
    SQL_DB_NAME = conf['SQL_LOCAL']['DB_NAME']
    SQL_USER = conf['SQL_LOCAL']['DB_USER']
    SQL_PASSWORD = conf['SQL_LOCAL']['DB_PASSWORD']
else:
    SQL_DB_NAME = conf['SQL']['DB_NAME']
    SQL_USER = conf['SQL']['DB_USER']
    SQL_PASSWORD = conf['SQL']['DB_PASSWORD']

SQL_URI = 'mysql+pymysql://{}:{}@localhost/{}'.format(SQL_USER, SQL_PASSWORD, SQL_DB_NAME)

engine = create_engine(SQL_URI, pool_recycle=3600)
container = AlchemySessionContainer(engine=engine)
alchemy_session = container.new_session('default')

# ============================== BOT SETTINGS ======================
PAYMENT_TOKEN = conf['TELEGRAM']['PAYMENT_TOKEN']
PAYMENT_SUCCESS_LISTEN = conf['TELEGRAM']['PAYMENT_SUCCESS_LISTEN']
PAYMENT_SUCCESS_LISTEN_PORT = conf['TELEGRAM']['PAYMENT_SUCCESS_LISTEN_PORT']

YAHOO_PATH = conf['PATHS']['YAHOO_PATH']
TARIFF_IMAGES = conf['TELEGRAM']['TARIFF_IMAGES']
BTC = conf['CREDENTIALS']['BTC']
ETH = conf['CREDENTIALS']['ETH']
API_KEY = conf['TELEGRAM']['API_KEY']
API_HASH = conf['TELEGRAM']['API_HASH']
if os.path.exists(conf_dir+'local.conf'):
    UPSILON = conf['TELEGRAM']['UPSILON_LOCAL']
else:
    UPSILON = conf['TELEGRAM']['UPSILON']
OWNER = conf['TELEGRAM']['OWNER']  # TODO Сделать пару владельцев для коммуникации
SERVICE_CHAT = conf['TELEGRAM']['SERVICE_CHAT']

# ============================== Logging Setup ======================
# logging.basicConfig(
#     filemode='w',
#     filename=os.path.abspath('logs/invest_services.log'),
#     format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
#     level=logging.WARNING)
# logging.getLogger('scrapers').setLevel(level=logging.WARNING)

RECURSION_DEPTH = 5

WARNING = conf['DEBUG_TYPE']['WARNING']
ERROR = conf['DEBUG_TYPE']['ERROR']

DEBUG_LOG_FILE = None


def is_debug_init():
    global DEBUG_LOG_FILE
    if DEBUG_LOG_FILE is None:
        return False
    else:
        return True

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


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


def debug_init(file_name="debug.log"):
    # print(f'%% Inint log file: {file_name}')
    global DEBUG_LOG_FILE
    fname = f'{LOGS_PATH}{file_name}'
    bufsize = 1
    DEBUG_LOG_FILE = open(fname, "a", buffering=bufsize)


def debug_deinit():
    global DEBUG_LOG_FILE
    if DEBUG_LOG_FILE is not None:
        DEBUG_LOG_FILE.close()
        DEBUG_LOG_FILE = None


def debug(print_string="", debug_type="NORMAL"):
    caller_frame_record = inspect.stack()[1]
    frame = caller_frame_record[0]
    info = inspect.getframeinfo(frame)
    path, filename = os.path.split(info.filename)
    dt = datetime.datetime.now()
    global DEBUG_LOG_FILE
    if DEBUG_LOG_FILE is not None:
        DEBUG_LOG_FILE.write(f'[{dt.strftime("%H:%M:%S")}]{filename}:{info.lineno}:{print_string}\n')
    else:
        if debug_type == "NORMAL":
            print(f'[{dt.strftime("%H:%M:%S")}]{filename}:{info.lineno}:{print_string}')
        elif debug_type == "WARNING":
            print(f'{bcolors.WARNING}[{dt.strftime("%H:%M:%S")}]{filename}:{info.lineno}:{print_string}{bcolors.ENDC}')
        elif debug_type == "ERROR":
            print(f'{bcolors.FAIL}[{dt.strftime("%H:%M:%S")}]{filename}:{info.lineno}:{print_string}{bcolors.ENDC}')


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def add_watermark(before, after, font_size=16, wtermark_color=(217, 217, 217, 20)):
    img_to_edit = IMAGES_OUT_PATH + before
    image = Image.open(img_to_edit).convert("RGBA")
    txt_img = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_img)
    font = ImageFont.truetype("arial.ttf", font_size)
    text = "(c) @UpsilonBot"
    font_width, font_height = font.getsize(text)
    x = image.width/2 - font_width/2
    y = image.height/2 - font_height/2
    draw.text((x, y), text, font=font, fill=wtermark_color)
    save_path = IMAGES_OUT_PATH + after
    composite = Image.alpha_composite(image, txt_img)
    composite.save(save_path)
