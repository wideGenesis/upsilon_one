import argparse
from project_shared import *
from quotes.portfolios.portfolios_calc import *
from quotes.portfolios.portfolios_save import *
from charter.charter import *
from quotes.get_universe import *
from quotes.quote_loader import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set log filename')
    parser.add_argument("--fname", default="cron_scheduler.log", help="This is the 'a' variable")
    args = parser.parse_args()
    log_file_name = args.fname

    debug_init(file_name=log_file_name)

    # ****************************************** СТАРЫЕ ПОРТФЕЛИ ******************************************

    debug(f"### Start eod_get_and_save_holdings ###")
    eod_get_and_save_holdings()

    universe = ['VIX']
    eod_update_universe_prices(universe)
    update_universe_prices1()

    debug(f"### Start calc portfolio allocation ###")
    portfolio_args = {}
    allocator_end_date = date.today()
    if allocator_end_date.day != 1:
        allocator_end_date = datetime.date(allocator_end_date.year, allocator_end_date.month, 1)
    alloctor_start_date = add_months(allocator_end_date, -3)
    selector_end_date = date.today()
    if selector_end_date.day != 1:
        selector_end_date = datetime.date(selector_end_date.year, selector_end_date.month, 1)
    selector_start_date = add_months(allocator_end_date, -12)
    vix_close = get_close_ticker_by_date('VIX', allocator_end_date)
    td = timedelta(days=1)

    debug(f"Start calc parking portfolio")
    # ======================================== P A R K I N G ========================================
    portfolio_args['port_id'] = 'parking'
    portfolio_args['etf_only'] = False
    portfolio_args['stocks_only'] = False
    portfolio_args['cor_perc'] = 0.9
    portfolio_args['sat_perc'] = 0.1
    # ********************* Parking cor *********************
    portfolio_args['cor_alloctor_start_date'] = alloctor_start_date
    portfolio_args['cor_allocator_end_date'] = allocator_end_date
    portfolio_args['cor_selector_start_date'] = selector_start_date
    portfolio_args['cor_selector_end_date'] = selector_end_date
    portfolio_args['cor_etf_list'] = PARKING
    portfolio_args['cor_assets_to_hold'] = 4
    portfolio_args['cor_cov_method'] = 'semi'
    portfolio_args['cor_herc'] = False
    portfolio_args['cor_linkage_'] = 'ward'
    portfolio_args['cor_risk_measure_'] = 'variance'
    portfolio_args['cor_graphs_show'] = False
    portfolio_args['cor_selector_type'] = 13
    portfolio_args['cor_selector_adjustment'] = False
    portfolio_args['cor_selector_p1'] = 21
    portfolio_args['cor_selector_p2'] = 126
    portfolio_args['cor_selector_c_p1'] = 1
    portfolio_args['cor_selector_c_p2'] = 3
    # ********************* Parking sat *********************
    portfolio_args['sat_alloctor_start_date'] = alloctor_start_date
    portfolio_args['sat_allocator_end_date'] = allocator_end_date
    portfolio_args['sat_selector_start_date'] = selector_start_date
    portfolio_args['sat_selector_end_date'] = selector_end_date
    portfolio_args['sat_etf_list'] = None
    portfolio_args['sat_cap_filter'] = 100000000000
    portfolio_args['sat_assets_to_hold'] = 4
    portfolio_args['sat_cov_method'] = 'de2'
    portfolio_args['sat_shrinkage_type'] = 'lw'
    portfolio_args['sat_denoise_method'] = 'const_resid_eigen'
    portfolio_args['sat_detone'] = True
    portfolio_args['sat_herc'] = False
    portfolio_args['sat_linkage_'] = 'ward'
    portfolio_args['sat_risk_measure_'] = 'variance'
    portfolio_args['sat_graphs_show'] = False
    portfolio_args['sat_selector_type'] = 21
    portfolio_args['sat_selector_adjustment'] = False
    portfolio_args['sat_selector_p1'] = 21
    portfolio_args['sat_selector_p2'] = 63
    portfolio_args['sat_selector_c_p1'] = 1
    portfolio_args['sat_selector_c_p2'] = 3
    portfolio_args['sat_cap_weight'] = 0
    portfolio_args['cap_limit_1'] = 0.13

    parking_weights = calc_portfolio(portfolio_args)
    create_portfolio_pie_image(weights=parking_weights,
                               title="Parking portfolio",
                               filename="parking_portfolio_pie")
    debug(f'[{portfolio_args["port_id"]}]: {parking_weights}')
    save_portfolio_weights(name='parking', portfolio_weights=parking_weights, allocation_date=(allocator_end_date-td))

    debug(f"Start calc allweather portfolio")
    # ======================================== A L L W E A T H E R ========================================
    portfolio_args['port_id'] = 'allweather'
    portfolio_args['etf_only'] = False
    portfolio_args['stocks_only'] = False
    portfolio_args['cor_perc'] = 0.8
    portfolio_args['sat_perc'] = 0.2
    # ********************* Allweather cor *********************
    portfolio_args['cor_alloctor_start_date'] = alloctor_start_date
    portfolio_args['cor_allocator_end_date'] = allocator_end_date
    portfolio_args['cor_selector_start_date'] = selector_start_date
    portfolio_args['cor_selector_end_date'] = selector_end_date
    portfolio_args['cor_etf_list'] = ALL_WEATHER
    portfolio_args['cor_assets_to_hold'] = 4
    portfolio_args['sat_cov_method'] = 'de2'
    portfolio_args['sat_shrinkage_type'] = 'lw'
    portfolio_args['sat_denoise_method'] = 'const_resid_eigen'
    portfolio_args['sat_detone'] = True
    portfolio_args['cor_herc'] = False
    portfolio_args['cor_linkage_'] = 'ward'
    portfolio_args['cor_risk_measure_'] = 'variance'
    portfolio_args['cor_graphs_show'] = False
    portfolio_args['cor_selector_type'] = 13
    portfolio_args['cor_selector_adjustment'] = False
    portfolio_args['cor_selector_p1'] = 21
    portfolio_args['cor_selector_p2'] = 126
    portfolio_args['cor_selector_c_p1'] = 1
    portfolio_args['cor_selector_c_p2'] = 3
    # ********************* Allweather sat *********************
    portfolio_args['sat_alloctor_start_date'] = alloctor_start_date
    portfolio_args['sat_allocator_end_date'] = allocator_end_date
    portfolio_args['sat_selector_start_date'] = selector_start_date
    portfolio_args['sat_selector_end_date'] = selector_end_date
    portfolio_args['sat_etf_list'] = None
    portfolio_args['sat_cap_filter'] = 150000000000
    portfolio_args['sat_assets_to_hold'] = 6
    portfolio_args['sat_cov_method'] = 'semi'
    portfolio_args['sat_herc'] = False
    portfolio_args['sat_linkage_'] = 'ward'
    portfolio_args['sat_risk_measure_'] = 'variance'
    portfolio_args['sat_graphs_show'] = False
    portfolio_args['sat_selector_type'] = 21
    portfolio_args['sat_selector_adjustment'] = False
    portfolio_args['sat_selector_p1'] = 21
    portfolio_args['sat_selector_p2'] = 63
    portfolio_args['sat_selector_c_p1'] = 1
    portfolio_args['sat_selector_c_p2'] = 3
    portfolio_args['sat_cap_weight'] = 0
    portfolio_args['cap_limit_1'] = 0.13

    allweather_weights = calc_portfolio(portfolio_args)
    create_portfolio_pie_image(weights=allweather_weights,
                               title="Allweather portfolio",
                               filename="allweather_portfolio_pie")
    debug(f'[{portfolio_args["port_id"]}]: {allweather_weights}')
    save_portfolio_weights(name='allweather',
                           portfolio_weights=allweather_weights,
                           allocation_date=(allocator_end_date-td))

    debug(f"Start calc balanced portfolio")
    # ======================================== B A L A N C E D ========================================
    portfolio_args['port_id'] = 'balanced'
    portfolio_args['etf_only'] = False
    portfolio_args['stocks_only'] = False
    portfolio_args['cor_perc'] = 0.7
    portfolio_args['sat_perc'] = 0.3
    # ********************* Balanced cor *********************
    portfolio_args['cor_alloctor_start_date'] = alloctor_start_date
    portfolio_args['cor_allocator_end_date'] = allocator_end_date
    portfolio_args['cor_selector_start_date'] = selector_start_date
    portfolio_args['cor_selector_end_date'] = selector_end_date
    portfolio_args['cor_etf_list'] = BALANCED
    portfolio_args['cor_assets_to_hold'] = 3
    portfolio_args['cor_cov_method'] = 'semi'
    portfolio_args['cor_herc'] = False
    portfolio_args['cor_linkage_'] = 'ward'
    portfolio_args['cor_risk_measure_'] = 'variance'
    portfolio_args['cor_graphs_show'] = False
    portfolio_args['cor_selector_type'] = 13
    portfolio_args['cor_selector_adjustment'] = False
    portfolio_args['cor_selector_p1'] = 21
    portfolio_args['cor_selector_p2'] = 126
    portfolio_args['cor_selector_c_p1'] = 1
    portfolio_args['cor_selector_c_p2'] = 3
    # ********************* Balanced sat *********************
    portfolio_args['sat_alloctor_start_date'] = alloctor_start_date
    portfolio_args['sat_allocator_end_date'] = allocator_end_date
    portfolio_args['sat_selector_start_date'] = selector_start_date
    portfolio_args['sat_selector_end_date'] = selector_end_date
    portfolio_args['sat_etf_list'] = None
    portfolio_args['sat_cap_filter'] = 100000000000
    portfolio_args['sat_assets_to_hold'] = 7
    portfolio_args['sat_cov_method'] = 'de2'
    portfolio_args['sat_shrinkage_type'] = 'lw'
    portfolio_args['sat_denoise_method'] = 'const_resid_eigen'
    portfolio_args['sat_detone'] = True
    portfolio_args['sat_herc'] = False
    portfolio_args['sat_linkage_'] = 'ward'
    portfolio_args['sat_risk_measure_'] = 'variance'
    portfolio_args['sat_graphs_show'] = False
    portfolio_args['sat_selector_type'] = 21
    portfolio_args['sat_selector_adjustment'] = False
    portfolio_args['sat_selector_p1'] = 21
    portfolio_args['sat_selector_p2'] = 63
    portfolio_args['sat_selector_c_p1'] = 1
    portfolio_args['sat_selector_c_p2'] = 3
    portfolio_args['sat_cap_weight'] = 0
    portfolio_args['cap_limit_1'] = 0.13

    balanced_weights = calc_portfolio(portfolio_args)
    create_portfolio_pie_image(weights=balanced_weights,
                               title="Balanced portfolio",
                               filename="balanced_portfolio_pie")
    debug(f'[{portfolio_args["port_id"]}]: {balanced_weights}')
    save_portfolio_weights(name='balanced', portfolio_weights=balanced_weights, allocation_date=(allocator_end_date-td))

    debug(f"Start calc aggressive portfolio")
    # ======================================== A G G R E S S I V E ========================================
    portfolio_args['port_id'] = 'aggressive'
    portfolio_args['etf_only'] = False
    portfolio_args['stocks_only'] = False
    portfolio_args['cor_perc'] = 0.7
    portfolio_args['sat_perc'] = 0.3
    # ********************* Aggressive cor *********************
    portfolio_args['cor_alloctor_start_date'] = alloctor_start_date
    portfolio_args['cor_allocator_end_date'] = allocator_end_date
    portfolio_args['cor_selector_start_date'] = selector_start_date
    portfolio_args['cor_selector_end_date'] = selector_end_date
    portfolio_args['cor_etf_list'] = AGGRESSIVE
    portfolio_args['cor_assets_to_hold'] = 3
    portfolio_args['cor_cov_method'] = 'semi'
    portfolio_args['cor_herc'] = False
    portfolio_args['cor_linkage_'] = 'ward'
    portfolio_args['cor_risk_measure_'] = 'variance'
    portfolio_args['cor_graphs_show'] = False
    portfolio_args['cor_selector_type'] = 13
    portfolio_args['cor_selector_adjustment'] = False
    portfolio_args['cor_selector_p1'] = 21
    portfolio_args['cor_selector_p2'] = 126
    portfolio_args['cor_selector_c_p1'] = 1
    portfolio_args['cor_selector_c_p2'] = 3
    # ********************* Aggressive sat *********************
    portfolio_args['sat_alloctor_start_date'] = alloctor_start_date
    portfolio_args['sat_allocator_end_date'] = allocator_end_date
    portfolio_args['sat_selector_start_date'] = selector_start_date
    portfolio_args['sat_selector_end_date'] = selector_end_date
    portfolio_args['sat_etf_list'] = None
    portfolio_args['sat_cap_filter'] = 5000000000
    portfolio_args['sat_assets_to_hold'] = 7
    portfolio_args['sat_cov_method'] = 'de2'
    portfolio_args['sat_shrinkage_type'] = 'lw'
    portfolio_args['sat_denoise_method'] = 'const_resid_eigen'
    portfolio_args['sat_detone'] = True
    portfolio_args['sat_herc'] = False
    portfolio_args['sat_linkage_'] = 'ward'
    portfolio_args['sat_risk_measure_'] = 'variance'
    portfolio_args['sat_graphs_show'] = False
    portfolio_args['sat_selector_type'] = 21
    portfolio_args['sat_selector_adjustment'] = False
    portfolio_args['sat_selector_p1'] = 63
    portfolio_args['sat_selector_p2'] = 63
    portfolio_args['sat_selector_c_p1'] = 1
    portfolio_args['sat_selector_c_p2'] = 3
    portfolio_args['sat_cap_weight'] = 0
    portfolio_args['cap_limit_1'] = 0.13

    aggressive_weights = calc_portfolio(portfolio_args)
    create_portfolio_pie_image(weights=aggressive_weights,
                               title="Aggressive portfolio",
                               filename="aggressive_portfolio_pie")
    debug(f'[{portfolio_args["port_id"]}]: {aggressive_weights}')
    save_portfolio_weights(name='aggressive',
                           portfolio_weights=aggressive_weights,
                           allocation_date=(allocator_end_date-td))

    debug(f"Start calc leveraged portfolio")
    # ======================================== L E V E R A G E D ========================================
    portfolio_args['port_id'] = 'leveraged'
    portfolio_args['is_aliased'] = False
    portfolio_args['etf_only'] = False
    portfolio_args['stocks_only'] = False
    portfolio_args['cor_perc'] = 0.65
    portfolio_args['sat_perc'] = 0.35
    # ********************* Leveraged cor *********************
    portfolio_args['cor_alloctor_start_date'] = alloctor_start_date
    portfolio_args['cor_allocator_end_date'] = allocator_end_date
    portfolio_args['cor_selector_start_date'] = selector_start_date
    portfolio_args['cor_selector_end_date'] = selector_end_date
    portfolio_args['cor_etf_list'] = LEVERAGED
    portfolio_args['cor_assets_to_hold'] = 3
    portfolio_args['cor_cov_method'] = 'semi'
    portfolio_args['cor_herc'] = False
    portfolio_args['cor_linkage_'] = 'ward'
    portfolio_args['cor_risk_measure_'] = 'variance'
    portfolio_args['cor_graphs_show'] = False
    portfolio_args['cor_selector_type'] = 13
    portfolio_args['cor_selector_adjustment'] = False
    portfolio_args['cor_selector_p1'] = 21
    portfolio_args['cor_selector_p2'] = 126
    portfolio_args['cor_selector_c_p1'] = 1
    portfolio_args['cor_selector_c_p2'] = 3
    # ********************* Leveraged sat *********************
    portfolio_args['sat_alloctor_start_date'] = alloctor_start_date
    portfolio_args['sat_allocator_end_date'] = allocator_end_date
    portfolio_args['sat_selector_start_date'] = selector_start_date
    portfolio_args['sat_selector_end_date'] = selector_end_date
    portfolio_args['sat_etf_list'] = None
    portfolio_args['sat_cap_filter'] = 20000000000
    portfolio_args['sat_assets_to_hold'] = 9
    portfolio_args['sat_cov_method'] = 'de2'
    portfolio_args['sat_shrinkage_type'] = 'lw'
    portfolio_args['sat_denoise_method'] = 'const_resid_eigen'
    portfolio_args['sat_detone'] = True
    portfolio_args['sat_herc'] = False
    portfolio_args['sat_linkage_'] = 'ward'
    portfolio_args['sat_risk_measure_'] = 'variance'
    portfolio_args['sat_graphs_show'] = False
    portfolio_args['sat_selector_type'] = 21
    portfolio_args['sat_selector_adjustment'] = False
    portfolio_args['sat_selector_p1'] = 21
    portfolio_args['sat_selector_p2'] = 63
    portfolio_args['sat_selector_c_p1'] = 1
    portfolio_args['sat_selector_c_p2'] = 3
    portfolio_args['sat_cap_weight'] = 0
    portfolio_args['cap_limit_1'] = 0.13

    leveraged_weights = calc_portfolio(portfolio_args)
    create_portfolio_pie_image(weights=leveraged_weights,
                               title="Leveraged portfolio",
                               filename="leveraged_portfolio_pie")
    debug(f'[{portfolio_args["port_id"]}]: {leveraged_weights}')
    save_portfolio_weights(name='leveraged',
                           portfolio_weights=leveraged_weights,
                           allocation_date=(allocator_end_date-td))

    # ****************************************** ПОРТФЕЛИ ТОЛЬКО НА АКЦИЯХ ******************************************

    # ++++++++++++++++++++++++++++++++++++++++++++ Сначала рассчитаем вселенную
    # ++++ Заберем текущие конституенты индекса NDX
    # Это и будет текущей вселенной
    debug("Get NDX constituents")
    curr_universe = get_index_constituent('NDX')

    # ++++ Обновляем цены по всем тикерам из curr_universe
    debug("Get NDX constituents prices")
    eod_update_universe_prices(curr_universe)

    # ++++ Далее идут основные расчеты  ++++++++++++++
    # расчитаем вселенную для текущего месяца
    cur_universe_date = date.today()
    td = timedelta(1)
    cur_universe_date = date(cur_universe_date.year, cur_universe_date.month, 1) - td
    debug(f'Current universe date: {cur_universe_date.strftime("%Y-%m-%d")}')

    need_update_prices = []
    if "MA" not in curr_universe:
        sector, mkt_cap, exchange = get_tickerdata("MA")
        curr_universe["MA"] = (sector, mkt_cap, exchange)
        need_update_prices.append("MA")
    if "V" not in curr_universe:
        sector, mkt_cap, exchange = get_tickerdata("V")
        curr_universe["V"] = (sector, mkt_cap, exchange)
        need_update_prices.append("V")
    if "PYPL" not in curr_universe:
        sector, mkt_cap, exchange = get_tickerdata("PYPL")
        curr_universe["PYPL"] = (sector, mkt_cap, exchange)
        need_update_prices.append("PYPL")
    if "WMT" not in curr_universe:
        sector, mkt_cap, exchange = get_tickerdata("WMT")
        curr_universe["WMT"] = (sector, mkt_cap, exchange)
        need_update_prices.append("WMT")
    if "NEE" not in curr_universe:
        sector, mkt_cap, exchange = get_tickerdata("NEE")
        curr_universe["NEE"] = (sector, mkt_cap, exchange)
        need_update_prices.append("NEE")
    if "XEL" not in curr_universe:
        sector, mkt_cap, exchange = get_tickerdata("XEL")
        curr_universe["XEL"] = (sector, mkt_cap, exchange)
        need_update_prices.append("XEL")

    # Заберем данные по вновь добавленным тикерам
    eod_update_universe_prices(need_update_prices)

    # Проверка на достаточность данных в тикерах
    # Данных должно быть за 12 месяцев до текущей даты вселенной cur_universe_date
    check_data_min = add_months(cur_universe_date, -12)
    td = timedelta(days=7)
    check_data_max = cur_universe_date - td
    universe_to_save = curr_universe.copy()
    for item in curr_universe.items():
        min_ticker_date = find_min_date_by_ticker(item[0])
        max_ticker_date = find_max_date_by_ticker(item[0])
        if min_ticker_date is not None and max_ticker_date is not None:
            if min_ticker_date > check_data_min or max_ticker_date < check_data_max:
                universe_to_save.pop(item[0])
        else:
            universe_to_save.pop(item[0])

    # Сохраним ткущую вселенную в БД
    if not is_table_exist(HIST_UNIVERSE_TABLE_NAME):
        create_hist_universe_table(HIST_UNIVERSE_TABLE_NAME)
    append_universe_by_date(universe_to_save, cur_universe_date)

    debug(f"Universe for date [{cur_universe_date.strftime('%Y-%m-%d')}]: {universe_to_save}")

    # ++++++++++++++++++++++++++++++++++++++++++++ Теперь рассчитаем портфели

    debug("%%%%%%%%%%%%%%%Complete calc portfolios \n\n\n")
    debug_deinit()
