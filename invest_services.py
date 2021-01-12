#!/usr/bin/env python3

from project_shared import *
from quotes.parsers_env import chrome_init, agents, chrome_opt
from quotes.parsers import get_flows, advance_decline, get_finviz_treemaps,\
    get_coins360_treemaps, get_economics, get_sma50, get_tw_charts, vix_curve, vix_cont, qt_curve, spx_yield
from quotes.get_universe import *
from quotes.quote_loader import *
from quotes.portfolios.portfolios_calc import *
from quotes.portfolios.portfolios_save import *
import schedule
from time import sleep
from charter.charter import *
import undetected_chromedriver as uc

proxy = "110.232.86.52:53281"
chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--proxy-server=direct://")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument(f'user-agent={agent_rotation}')
chrome_options.add_argument("--enable-javascript")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--proxy-server={}'.format(proxy))
chrome_options.add_argument("user-data-dir=/home/upsilonsfather/.config/google-chrome")
# chrome_options.add_argument('--profile-directory=Default')
# ============================== Main  =============================
def main():

    get_flows(driver=uc.Chrome(options=chrome_options))
    exit()
    # Это забирание вселенной по-старому
    # get_and_save_holdings(driver=chrome_init())
    # update_universe_prices()

    # Это уже формирование вселенной по-новому, через апи
    # eod_get_and_save_holdings()
    update_universe_prices1()

    # parking_weights = parking_portfolio()
    # allweather_weights = allweather_portfolio()
    # balanced_weights = balanced_portfolio()
    # aggressive_weights = aggressive_portfolio()
    # leveraged_weights = leveraged_portfolio()
    # create_portfolio_pie_image(weights=parking_weights,
    #                            title="Parking portfolio",
    #                            filename="parking_portfolio_pie")
    # create_portfolio_pie_image(weights=allweather_weights,
    #                            title="Allweather portfolio",
    #                            filename="allweather_portfolio_pie")
    # create_portfolio_pie_image(weights=balanced_weights,
    #                            title="Balanced portfolio",
    #                            filename="balanced_portfolio_pie")
    # create_portfolio_pie_image(weights=aggressive_weights,
    #                            title="Aggressive portfolio",
    #                            filename="aggressive_portfolio_pie")
    # create_portfolio_pie_image(weights=leveraged_weights,
    #                            title="Leveraged portfolio",
    #                            filename="leveraged_portfolio_pie")
    # save_portfolio_weights(name='parking', portfolio_weights=parking_weights)
    # save_portfolio_weights(name='allweather', portfolio_weights=allweather_weights)
    # save_portfolio_weights(name='balanced', portfolio_weights=balanced_weights)
    # save_portfolio_weights(name='aggressive', portfolio_weights=aggressive_weights)
    # save_portfolio_weights(name='leveraged', portfolio_weights=leveraged_weights)
    #
    # td = timedelta(days=365)
    # ed = date.today()
    # sd = ed - td
    # ohlc = get_ohlc_dict_by_port_id('leveraged', start_date=sd, end_date=ed)
    # debug("OHLC:" + str(ohlc))
    #
    # portfolio_bars = returns_calc(ohlc=ohlc)
    # save_portfolio_bars(name="leveraged", portfolio_bars=portfolio_bars)
    # create_candle_portfolio_img(port_id="leveraged", compare_ticker="QQQ", start_date=sd, end_date=ed)
    #
    # exit()

    # start_test_date - первая дата на которую будет вычеслена первая аллокация, далее эта дата смещается на месяц
    # data_interval -- за какой период времени на RP будут подаваться данные -3 значит за 3 месяца
    # start_test_date = datetime.date(2007, 1, 1)
    # data_interval = -3
    # port_id = 'parking'
    port_id = 'allweather'
    # port_id = 'balanced'
    # port_id = 'aggressive'
    # port_id = 'leveraged'
    # portfolio_tester(port_id=port_id, data_interval=data_interval, start_test_date=start_test_date)

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

    # schedule.every(720).minutes.do(lambda: get_flows(driver=chrome_init()))
    # schedule.every(120).minutes.do(lambda: advance_decline(ag=agents()))
    # schedule.every(480).minutes.do(lambda: qt_curve())
    # schedule.every(480).minutes.do(lambda: spx_yield())
    # schedule.every(480).minutes.do(lambda: vix_cont())
    # schedule.every(125).minutes.do(lambda: get_sma50(ag=agents()))
    # schedule.every().monday.do(lambda: get_economics(ag=agents()))
    # schedule.every(30).minutes.do(lambda: get_tw_charts(driver=chrome_init()))
    # schedule.every(120).minutes.do(lambda: vix_curve(driver=chrome_init()))
    # schedule.every(30).minutes.do(lambda: get_finviz_treemaps(driver=chrome_init()))
    # schedule.every(30).minutes.do(lambda: get_coins360_treemaps(driver=chrome_init()))

    # while True:
    #     schedule.run_pending()
    #     sleep(5)


if __name__ == '__main__':
    print(f"Starting scrapers {os.path.realpath(__file__)}, this may take a while")
    main()
