#!/usr/bin/env python3

import os
import sys
import yaml
import logging
from quotes.parsers_env import firefox_init, chrome_init, agents
from quotes.parsers import get_flows, advance_decline, get_finviz_treemaps,\
    get_coins360_treemaps, get_economics, get_sma50, get_tw_charts, vix_curve, vix_cont, qt_curve, spx_yield
from quotes.get_universe import ConstituentsScraper #get_etf_holdings
import schedule
from time import sleep


PYTHON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(PYTHON_PATH)
os.environ["PYTHONUNBUFFERED"] = "1"

conf = yaml.safe_load(open('config/settings.yaml'))
LOGS = conf['PATHS']['LOGS']
WEBDRIVER = conf['PATHS']['WEBDRIVER']
IMAGES_OUT_PATH = conf['PATHS']['IMAGES_OUT_PATH']
ETF_HOLDINGS_URL = conf['PATHS']['ETF_HOLDINGS_URL']

# ============================== Logging Setup ======================
logging.basicConfig(
    filemode='w',
    filename=os.path.abspath('logs/invest_services.log'),
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING)
logging.getLogger('scrapers').setLevel(level=logging.WARNING)


# ============================== Main  =============================
def main():
    etfs = ['DIA', 'XLU']
    chrome = chrome_init(webdriver_path=WEBDRIVER, agent_rotation=agents(), headless=True)
    firefox = firefox_init(webdriver_path=WEBDRIVER, agent_rotation=agents())
    universe = ConstituentsScraper(holdings_url=ETF_HOLDINGS_URL, etfs_list=etfs)

    constituents = universe.get_etf_holdings(driver=chrome)
    print(constituents)
    # exit()

    get_flows(driver=chrome, img_out_path_=IMAGES_OUT_PATH)
    advance_decline(ag=agents())
    qt_curve()
    spx_yield()
    vix_cont()
    get_sma50(ag=agents())
    get_economics(ag=agents(), img_out_path_=IMAGES_OUT_PATH)
    get_finviz_treemaps(driver=firefox, img_out_path_=IMAGES_OUT_PATH)
    get_coins360_treemaps(driver=firefox, img_out_path_=IMAGES_OUT_PATH)
    get_tw_charts(driver=chrome, img_out_path_=IMAGES_OUT_PATH)
    vix_curve(driver=chrome, img_out_path_=IMAGES_OUT_PATH)

    schedule.every(720).minutes.do(lambda: get_flows(driver=chrome, img_out_path_=IMAGES_OUT_PATH))
    schedule.every(120).minutes.do(lambda: advance_decline(ag=agents()))
    schedule.every(480).minutes.do(lambda: qt_curve())
    schedule.every(480).minutes.do(lambda: spx_yield())
    schedule.every(480).minutes.do(lambda: vix_cont())
    schedule.every(125).minutes.do(lambda: get_sma50(ag=agents()))
    schedule.every().monday.do(lambda: get_economics(ag=agents(), img_out_path_=IMAGES_OUT_PATH))
    schedule.every(30).minutes.do(lambda: get_finviz_treemaps(driver=firefox, img_out_path_=IMAGES_OUT_PATH))
    schedule.every(30).minutes.do(lambda: get_coins360_treemaps(driver=firefox, img_out_path_=IMAGES_OUT_PATH))
    schedule.every(30).minutes.do(lambda: get_tw_charts(driver=chrome, img_out_path_=IMAGES_OUT_PATH))
    schedule.every(120).minutes.do(lambda: vix_curve(driver=chrome, img_out_path_=IMAGES_OUT_PATH))

    while True:
        schedule.run_pending()
        sleep(5)


if __name__ == '__main__':
    print(f"Starting scrapers {os.path.realpath(__file__)}, this may take a while")
    main()
