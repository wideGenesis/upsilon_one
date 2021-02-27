#!/usr/bin/env python3

from project_shared import *
from quotes.parsers_env import chrome_init, agents, chrome_opt, firefox_init
from quotes.parsers import *
from quotes.get_universe import *
from quotes.quote_loader import *
from quotes.portfolios.portfolios_calc import *
from quotes.portfolios.portfolios_save import *
import schedule
from time import sleep
from charter.charter import *
import undetected_chromedriver as uc
from quotes.historical_universe import *


# ============================== Main  =============================
def main():
    x = get_ranking_data("AAPL")
    print(x)
    exit(0)
    # 1) Первичный аплоад данных. Делаем один раз и больше данные не  трогаем.
    #    Ео если вдруг пришлось дропнуть таблицу quotes то лучше начать именно с первичного забора данных
    # Создадим максимально необходимый список тикеров. Он учитывет все конституенты Насдака + исторические
    # вхождения и выбытия из Насдака.
    # Также в нем все сонституенты из списка в настройках - ETF_FOR_SCRAPE.
    # А также все ETFы из списка в настройках - ETFs
    # global_universe = create_max_universe_list()

    # Закачаем OHLC по всему этому списку начиная с даты указанной в настройках в DEFAULT_START_QUOTES_DATE
    # ohlc_data_updater(global_universe)

    # Создать текущую вселенную.
    # eod_get_and_save_holdings()

    # 2) Обновление данных!
    # На вход можно подать любой набор тикеров.
    # Для того что бы не было ошибок с попыткой положить в базу дублированные данные,
    # нужно второй аргумент функции выставить в TRUE !!! ЭТО ВАЖНО!
    # Иначе обновление данных по тикерам где данные дублируются не произойдет.
    # Функция возмет по каждому тикеру максимальную дату, которая найдется в базе
    # и будет пытаться обновить с этой даты по сегодня
    global_universe = create_max_universe_list()
    ohlc_data_updater(global_universe, True)

    # 3) Обновление данных за конкретный период времени. Сделано на тот случай если вдруг,
    # по неизвестной причине в данных есть дырки, что бы можно было не перезабирать все данные,
    # а обновить только за конкретный период. Надеюсь этот вараинт не пригодится,
    # но для гибкости забора данных пусть будет.
    # global_universe = create_max_universe_list()
    # ohlc_data_updater(global_universe, True, datetime.date(2021, 1, 1), datetime.date(2021, 2, 1))



    exit()
    # Создать текущую вселенную.
    eod_get_and_save_holdings()

    exit()


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

    # start_test_date - первая дата на которую будет вычеслена первая аллокация, далее эта дата смещается на месяц
    # data_interval -- за какой период времени на RP будут подаваться данные -3 значит за 3 месяца
    # start_test_date = datetime.date(2007, 1, 1)
    # data_interval = -3
    # port_id = 'parking'
    # port_id = 'allweather'
    # port_id = 'balanced'
    # port_id = 'aggressive'
    # port_id = 'leveraged'
    # portfolio_tester(port_id=port_id, data_interval=data_interval, start_test_date=start_test_date)


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
    # print(f"Starting scrapers {os.path.realpath(__file__)}, this may take a while")
    main()
