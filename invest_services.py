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
from charter.finance2 import *
import undetected_chromedriver as uc
from quotes.historical_universe import *
from quotes.stock_quotes_news import StockStat
# from messages.message import *
# from quantstats.quantstats_backtest import *


# ============================== Main  =============================
def main():
    x = get_inspector_data({'QQQ': 1})
    # , 'LGIH': 3, 'PZZA': 4, 'MTH': 6, 'MBUU': 13,
    #                         'YEXT': 26, 'PRLB': 3, 'MTRN': 5, 'ASGN': 5, 'SMTC': 4, 'SRDX': 8, 'VRTV': 20, 'ATRA': 28,
    #                         'PS': 13, 'MUSA': 3, 'LLY': 6, 'LGND': 4, 'IIVI': 13, 'HALO': 12, 'CDNS': 2, 'CBPO': 1,
    #                         'CLX': 1, 'FIZZ': 3, 'SMG': 1, 'AVAV': 3, 'LRN': 14, 'SJM': 1, 'KR': 4, 'CAG': 2})
        # {'QQQ': 201, 'SPY': 23, 'XLV': 21, 'XLY': 28, 'GLD': 28, 'UUP': 1291, 'SHY': 371})
    # {'QQQ': 0, 'MSFT': 0, 'AMZN': 0, 'TSLA': 0,
    #  'QLD': 0, 'AGG': 0, 'AAPL': 0, 'VLUE': 0}
    # {'AAPL': 0, 'MSFT': 0, 'AMZN': 0, 'TSLA': 0, 'FB': 0, 'GOOG': 0, 'IBM': 0,
    #  'JPM': 0, 'UNH': 0, 'GS': 0, 'HD': 0, 'AMGN': 0, 'INTC': 0, 'T': 0,
    #  'MU': 0, 'GM': 0}
    # {'QQQ': 201, 'SPY': 23, 'XLV': 21, 'XLY': 28, 'GLD': 28, 'UUP': 1291, 'SHY': 371}
    # {'QQQ': 0, 'XLP': 0, 'GME': 0, 'AYX': 0}
    exit()

    # x, y = get_ranking_data2("DOCN")
    # debug(x)
    # debug(y)
    # exit()

    # while True:
    #     ticker = input("\n\n\nInput ticker:")
    #     if ticker == "quit":
    #         break
    #     x = get_ranking_data3(ticker)
    #     debug(x)
    # exit()


    # end_date = date.today()
    # td = timedelta(365)
    # start_date = end_date - td
    # create_candle_portfolio_img(port_id='aggressive',
    #                             compare_ticker='QQQ',
    #                             # chart_type='Line',
    #                             start_date=start_date,
    #                             end_date=end_date,
    #                             chart_path=LOGS_PATH)
    # exit()
    # create_pdf()
    # exit()

    get_tw_charts(driver=chrome_init())
    exit()

    # before = f'C:\\Projects\\ups_one\\yolo.png'
    # after = f'C:\\Projects\\ups_one\\results\\strategy_stats\\yolo3.png'
    # add_watermark(before, after, 64, wtermark_color=(217, 217, 217, 40))
    # exit()
    #
    # pdf = get_portfolio_returns_df("aggressive")
    # debug(f'DF:{pdf}')
    # exit()
    # pdata = {"XLY": 2.5,
    #          "XLV": 2.5,
    #          "IEF": 10.0,
    #          "DBC": 7.5,
    #          "TLT": 30,
    #          "GLD": 7.5,
    #          "QQQ": 40.0}
    # manual_create_portfolio_donut(portfolio_data=pdata, title="All Seasons S", filename="all_seasons_s_pie")
    # pdata1 = {"SPY": 5.0,
    #          "XLY": 10.0,
    #          "XLV": 10.0,
    #          "IEF": 7.5,
    #          "DBC": 2.5,
    #          "TLT": 20.0,
    #          "GLD": 5.0,
    #          "QQQ": 40.0}
    # manual_create_portfolio_donut(portfolio_data=pdata1, title="All Seasons M", filename="all_seasons_m_pie")
    # pdata2 = {"SPY": 5.0,
    #          "XLY": 10.0,
    #          "XLV": 10.0,
    #          "IEF": 5.0,
    #          "TLT": 20.0,
    #          "QQQ": 50.0}
    # manual_create_portfolio_donut(portfolio_data=pdata2, title="All Seasons L", filename="all_seasons_l_pie")
    # exit()
    #
    # sentusrdict, failusrdict, pollresult = get_mailing_lists(53)
    # debug(f'sentusrdict:{sentusrdict}')
    # debug(f'failusrdict:{failusrdict}')
    # debug(f'pollresult:{pollresult}')
    # exit()
    #
    # img_out_path = PROJECT_HOME_DIR + '/' + IMAGES_OUT_PATH
    # get_tw_charts(driver=chrome_init(), img_out_path_=img_out_path)
    # get_moex(driver=chrome_init(), img_out_path_=img_out_path)
    #
    # exit()
    # x = get_ranking_data2("GILD")
    # y = x[1]
    # print('%%%%%%%%', y)
    # exit(0)
    # print(x)
    # ss = StockStat(stock='AMGN')
    # out = ss.company_rank_v2()
    # print(out)
    # exit(0)
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
    # global_universe = create_max_universe_list()
    # ohlc_data_updater(global_universe, True)

    # 3) Обновление данных за конкретный период времени. Сделано на тот случай если вдруг,
    # по неизвестной причине в данных есть дырки, что бы можно было не перезабирать все данные,
    # а обновить только за конкретный период. Надеюсь этот вараинт не пригодится,
    # но для гибкости забора данных пусть будет.
    # global_universe = create_max_universe_list()
    # ohlc_data_updater(global_universe, True, datetime.date(2021, 1, 1), datetime.date(2021, 2, 1))



    # exit()
    # # Создать текущую вселенную.
    # eod_get_and_save_holdings()
    #
    # exit()


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
