import json
from datetime import timedelta, date, datetime
from project_shared import *
from quotes.sql_queries import *
from quotes.quote_loader import *
from quotes.eodhistoricaldata import *
import simfin as sf
from simfin.names import *
import pandas as pd

FMP_API_KEY = f'5d0aeca6a9e10d5c77140a33607d3872'


def get_last_nasdaq_events():
    debug("#Start get last nasdaq events")
    jsn = ""
    session = requests.Session()
    url = f'https://financialmodelingprep.com/api/v3/historical/nasdaq_constituent'
    params = {'apikey': FMP_API_KEY}
    request_result = session.get(url, params=params)
    if request_result.status_code == requests.codes.ok:
        jsn = request_result.text
    else:
        debug(f"Can't get NASDAQ historical events")
    return jsn


def create_last_hist_universe():
    jsn = get_last_nasdaq_events()
    parsed_json = json.loads(jsn)

