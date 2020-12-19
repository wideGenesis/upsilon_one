#!/usr/bin/env python3

from project_shared import *
from quotes.parsers_env import chrome_init, agents
from quotes.parsers import get_flows, advance_decline, get_finviz_treemaps,\
    get_coins360_treemaps, get_economics, get_sma50, get_tw_charts, vix_curve, vix_cont, qt_curve, spx_yield
from quotes.get_universe import *
from quotes.quote_loader import *
from quotes.portfolios.portfolios_calc import *
import schedule
from time import sleep


# ============================== Main  =============================
def main():

    # get_and_save_holdings(driver=chrome_init())
    # update_universe_prices()
    parking_portfolio()
    allweather_portfolio()
    exit()

    get_flows(driver=chrome_init())
    advance_decline(ag=agents())
    qt_curve()
    spx_yield()
    vix_cont()
    get_sma50(ag=agents())
    get_economics(ag=agents())
    get_tw_charts(driver=chrome_init())

    vix_curve(driver=chrome_init())
    get_finviz_treemaps(driver=chrome_init())
    get_coins360_treemaps(driver=chrome_init())

    schedule.every(720).minutes.do(lambda: get_flows(driver=chrome_init()))
    schedule.every(120).minutes.do(lambda: advance_decline(ag=agents()))
    schedule.every(480).minutes.do(lambda: qt_curve())
    schedule.every(480).minutes.do(lambda: spx_yield())
    schedule.every(480).minutes.do(lambda: vix_cont())
    schedule.every(125).minutes.do(lambda: get_sma50(ag=agents()))
    schedule.every().monday.do(lambda: get_economics(ag=agents()))
    schedule.every(30).minutes.do(lambda: get_tw_charts(driver=chrome_init()))
    schedule.every(120).minutes.do(lambda: vix_curve(driver=chrome_init()))
    schedule.every(30).minutes.do(lambda: get_finviz_treemaps(driver=chrome_init()))
    schedule.every(30).minutes.do(lambda: get_coins360_treemaps(driver=chrome_init()))

    while True:
        schedule.run_pending()
        sleep(5)


if __name__ == '__main__':
    print(f"Starting scrapers {os.path.realpath(__file__)}, this may take a while")
    main()