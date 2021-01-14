from project_shared import *
from quotes.portfolios.portfolios_calc import *
from quotes.portfolios.portfolios_save import *
from charter.charter import *
from quotes.get_universe import *


if __name__ == '__main__':
    debug_init(file_name="cron_scheduler.log")

    debug(f"### Start eod_get_and_save_holdings ###")
    eod_get_and_save_holdings()

    debug(f"### Start calc portfolio allocation ###")
    portfolio_args = {}
    allocator_end_date = date.today()
    alloctor_start_date = add_months(allocator_end_date, -3)
    selector_end_date = date.today()
    selector_start_date = add_months(allocator_end_date, -12)

    debug(f"Start calc parking portfolio")
    # ======================================== P A R K I N G ========================================
    portfolio_args['port_id'] = 'parking'
    portfolio_args['etf_only'] = False
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

    parking_weights = calc_portfolio(portfolio_args)
    create_portfolio_pie_image(weights=parking_weights,
                               title="Parking portfolio",
                               filename="parking_portfolio_pie")
    save_portfolio_weights(name='parking', portfolio_weights=parking_weights)

    debug(f"Start calc allweather portfolio")
    # ======================================== A L L W E A T H E R ========================================
    portfolio_args['port_id'] = 'allweather'
    portfolio_args['etf_only'] = False
    portfolio_args['cor_perc'] = 0.8
    portfolio_args['sat_perc'] = 0.2
    # ********************* Allweather cor *********************
    portfolio_args['cor_alloctor_start_date'] = alloctor_start_date
    portfolio_args['cor_allocator_end_date'] = allocator_end_date
    portfolio_args['cor_selector_start_date'] = selector_start_date
    portfolio_args['cor_selector_end_date'] = selector_end_date
    portfolio_args['cor_etf_list'] = ALL_WEATHER
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

    allweather_weights = calc_portfolio(portfolio_args)
    create_portfolio_pie_image(weights=allweather_weights,
                               title="Allweather portfolio",
                               filename="allweather_portfolio_pie")
    save_portfolio_weights(name='allweather', portfolio_weights=allweather_weights)

    debug(f"Start calc balanced portfolio")
    # ======================================== B A L A N C E D ========================================
    portfolio_args['port_id'] = 'balanced'
    portfolio_args['etf_only'] = False
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

    balanced_weights = calc_portfolio(portfolio_args)
    create_portfolio_pie_image(weights=balanced_weights,
                               title="Balanced portfolio",
                               filename="balanced_portfolio_pie")
    save_portfolio_weights(name='balanced', portfolio_weights=balanced_weights)

    debug(f"Start calc aggressive portfolio")
    # ======================================== A G G R E S S I V E ========================================
    portfolio_args['port_id'] = 'aggressive'
    portfolio_args['etf_only'] = False
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
    portfolio_args['sat_cov_method'] = 'semi'
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

    aggressive_weights = calc_portfolio(portfolio_args)
    create_portfolio_pie_image(weights=aggressive_weights,
                               title="Aggressive portfolio",
                               filename="aggressive_portfolio_pie")
    save_portfolio_weights(name='aggressive', portfolio_weights=aggressive_weights)

    debug(f"Start calc leveraged portfolio")
    # ======================================== L E V E R A G E D ========================================
    portfolio_args['port_id'] = 'leveraged'
    portfolio_args['is_aliased'] = False
    portfolio_args['etf_only'] = False
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

    leveraged_weights = calc_portfolio(portfolio_args)
    create_portfolio_pie_image(weights=leveraged_weights,
                               title="Leveraged portfolio",
                               filename="leveraged_portfolio_pie")
    save_portfolio_weights(name='leveraged', portfolio_weights=leveraged_weights)
    debug("%%%%%%%%%%%%%%%Complete calc portfolios \n\n\n")
    debug_deinit()
