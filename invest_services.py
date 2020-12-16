#!/usr/bin/env python3

from project_shared import *
from quotes.parsers_env import firefox_init, chrome_init, agents
from quotes.parsers import get_flows, advance_decline, get_finviz_treemaps,\
    get_coins360_treemaps, get_economics, get_sma50, get_tw_charts, vix_curve, vix_cont, qt_curve, spx_yield
from quotes.get_universe import *
from quotes.quote_loader import *
from quotes.portfolios.rp_portfolio import *
import schedule
from time import sleep


# ============================== Main  =============================
def main():
    # update_universe_prices()
    closes_df = get_closes_universe_df(cap_filter=100000000000)

    select = Selector(closes=closes_df)
    tickers = select.rs_sharpe()
    c_df = get_closes_by_ticker_list(tickers)

    rp = RiskParityAllocator(closes=c_df, cov_method='mcd', herc=False, risk_measure_='conditional_drawdown_risk')
    rp.calc_returns()
    rp.allocator()

    # # если start_date и end_date не указаны специально, то данные будут браться за период от сегодня минус 365 дней
    """
    equal_weighting 
    variance
    standard_deviation
    expected_shortfall
    conditional_drawdown_risk
    """
    exit()

    chrome = chrome_init()
    firefox = firefox_init()
    get_and_save_holdings(driver=chrome)

    exit()

    get_flows(driver=chrome)
    advance_decline(ag=agents())
    qt_curve()
    spx_yield()
    vix_cont()
    get_sma50(ag=agents())
    get_economics(ag=agents())
    get_finviz_treemaps(driver=firefox)
    get_coins360_treemaps(driver=firefox)
    get_tw_charts(driver=chrome)
    vix_curve(driver=chrome)

    schedule.every(720).minutes.do(lambda: get_flows(driver=chrome))
    schedule.every(120).minutes.do(lambda: advance_decline(ag=agents()))
    schedule.every(480).minutes.do(lambda: qt_curve())
    schedule.every(480).minutes.do(lambda: spx_yield())
    schedule.every(480).minutes.do(lambda: vix_cont())
    schedule.every(125).minutes.do(lambda: get_sma50(ag=agents()))
    schedule.every().monday.do(lambda: get_economics(ag=agents()))
    schedule.every(30).minutes.do(lambda: get_finviz_treemaps(driver=firefox))
    schedule.every(30).minutes.do(lambda: get_coins360_treemaps(driver=firefox))
    schedule.every(30).minutes.do(lambda: get_tw_charts(driver=chrome))
    schedule.every(120).minutes.do(lambda: vix_curve(driver=chrome))

    while True:
        schedule.run_pending()
        sleep(5)


if __name__ == '__main__':
    print(f"Starting scrapers {os.path.realpath(__file__)}, this may take a while")
    main()