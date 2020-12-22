#!/usr/bin/env python3

from project_shared import *
from quotes.parsers_env import chrome_init, agents
from quotes.parsers import get_flows, advance_decline, get_finviz_treemaps,\
    get_coins360_treemaps, get_economics, get_sma50, get_tw_charts, vix_curve, vix_cont, qt_curve, spx_yield
from quotes.get_universe import *
from quotes.quote_loader import *
from quotes.portfolios.portfolios_calc import *
from quotes.portfolios.portfolios_save import *
import schedule
from time import sleep
from charter.charter import *


# ============================== Main  =============================
def main():

    # Это забирание вселенной по-старому
    # get_and_save_holdings(driver=chrome_init())
    # update_universe_prices()

    # Это уже формирование вселенной по-новому, через апи
    # eod_get_and_save_holdings()
    # eod_update_universe_prices()

    parking_weights = parking_portfolio()
    allweather_weights = allweather_portfolio()
    balanced_weights = balanced_portfolio()
    aggressive_weights = aggressive_portfolio()
    leveraged_weights = leveraged_portfolio()
    create_portfolio_pie_image(weights=parking_weights,
                               title="Parking portfolio",
                               filename="parking_portfolio_pie")
    create_portfolio_pie_image(weights=allweather_weights,
                               title="Allweather portfolio",
                               filename="allweather_portfolio_pie")
    create_portfolio_pie_image(weights=balanced_weights,
                               title="Balanced portfolio",
                               filename="balanced_portfolio_pie")
    create_portfolio_pie_image(weights=aggressive_weights,
                               title="Aggressive portfolio",
                               filename="aggressive_portfolio_pie")
    create_portfolio_pie_image(weights=leveraged_weights,
                               title="Leveraged portfolio",
                               filename="leveraged_portfolio_pie")
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
