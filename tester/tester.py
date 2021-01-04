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
import multiprocessing as mp


def find_start_date(port_id, data_interval, start_test_date):
    min_dat = ""
    ticker = ""
    if port_id == 'parking':
        min_dat, ticker = find_min_date(PARKING)
    elif port_id == 'allweather':
        min_dat, ticker = find_min_date(ALL_WEATHER)
    elif port_id == 'balanced':
        min_dat, ticker = find_min_date(BALANCED)
    elif port_id == 'aggressive':
        min_dat, ticker = find_min_date(AGGRESSIVE)
    elif port_id == 'leveraged':
        min_dat, ticker = find_min_date(LEVERAGED)

    if min_dat is not None and ticker is not None:
        if min_dat.day > 1:
            min_dat = add_months(min_dat, data_interval+1)
            min_dat = datetime.date(min_dat.year, min_dat.month, 1)
        else:
            min_dat = add_months(min_dat, data_interval)
        if start_test_date >= min_dat:
            return start_test_date
        else:
            debug(f'[{port_id}][{ticker}]: You must start test from:{min_dat}', "WARNING")
            return min_dat
    elif min_dat is None and ticker is not None:
        debug(f'[{port_id}]: Can\'t find data for ticker :{ticker}', "ERROR")
    elif min_dat is None and ticker is None:
        debug(f'[{port_id}]: Can\'t lookup ticker!', "ERROR")


def portfolio_tester(init_cap=10000, port_id='parking', allocator_data_interval=3, selector_data_interval=1, start_test_date=datetime.date(2008, 1, 1)):
    in_cap = init_cap
    compare_ticker = ""
    max_date_interval = max(allocator_data_interval, selector_data_interval)
    real_start_date = find_start_date(port_id=port_id, data_interval=max_date_interval, start_test_date=start_test_date)
    allocator_end_date = real_start_date
    alloctor_start_date = add_months(allocator_end_date, -allocator_data_interval)
    selector_end_date = real_start_date
    selector_start_date = add_months(allocator_end_date, -selector_data_interval)
    pend_date = real_start_date

    portfolio_args = {}
    if port_id == 'parking':
        # ======================================== P A R K I N G ========================================
        portfolio_args['etf_only'] = True
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
        portfolio_args['cor_selector_type'] = 1
        portfolio_args['cor_selector_adjustment'] = False
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
        portfolio_args['sat_selector_type'] = 1
        portfolio_args['sat_selector_adjustment'] = False
        compare_ticker = "TLT"

    elif port_id == 'allweather':
        # ======================================== A L L W E A T H E R ========================================
        portfolio_args['etf_only'] = True
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
        portfolio_args['cor_selector_type'] = 1
        portfolio_args['cor_selector_adjustment'] = False
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
        portfolio_args['sat_selector_type'] = 1
        portfolio_args['sat_selector_adjustment'] = False
        compare_ticker = "SPY"

    elif port_id == 'balanced':
        # ======================================== B A L A N C E D ========================================
        portfolio_args['etf_only'] = True
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
        portfolio_args['cor_selector_type'] = 1
        portfolio_args['cor_selector_adjustment'] = False
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
        portfolio_args['sat_selector_type'] = 1
        portfolio_args['sat_selector_adjustment'] = False
        compare_ticker = "QQQ"
    elif port_id == 'aggressive':
        # ======================================== A G G R E S S I V E ========================================
        portfolio_args['etf_only'] = True
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
        portfolio_args['cor_selector_type'] = 1
        portfolio_args['cor_selector_adjustment'] = False
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
        portfolio_args['sat_selector_type'] = 1
        portfolio_args['sat_selector_adjustment'] = False
        compare_ticker = "QQQ"
    elif port_id == 'leveraged':
        # ======================================== L E V E R A G E D ========================================
        portfolio_args['etf_only'] = True
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
        portfolio_args['cor_selector_type'] = 1
        portfolio_args['cor_selector_adjustment'] = False
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
        portfolio_args['sat_selector_type'] = 1
        portfolio_args['sat_selector_adjustment'] = False
        compare_ticker = "QQQ"

    weights = calc_portfolio(portfolio_args)

    debug(f'Start allo({port_id}) [{allocator_end_date}]:{weights}')
    save_portfolio_weights(name=port_id, portfolio_weights=weights)

    while allocator_end_date <= date.today():
        allocator_end_date = add_months(allocator_end_date, 1)
        selector_end_date = add_months(selector_end_date, 1)
        alloctor_start_date = add_months(allocator_end_date, -allocator_data_interval)
        selector_start_date = add_months(allocator_end_date, -selector_data_interval)
        pend_date = add_months(pend_date, 1)
        pstart_date = add_months(pend_date, -1)

        ohlc = get_ohlc_dict_by_port_id(port_id, start_date=pstart_date, end_date=pend_date)
        if len(ohlc) == 0:
            break
        portfolio_bars, returns = returns_calc(init_capital=in_cap, ohlc=ohlc)
        save_portfolio_bars(name=port_id, portfolio_bars=portfolio_bars)
        save_portfolio_returns(name=port_id, portfolio_returns=returns)

        pb = list(portfolio_bars)
        cash = round(in_cap - pb[0][4], 2)
        if cash > 0:
            in_cap = round(pb[-1][4] + cash, 2)
        else:
            debug("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            in_cap = pb[-1][4]

        # debug(f'{allocator_end_date}:{cash}')
        portfolio_args['cor_alloctor_start_date'] = alloctor_start_date
        portfolio_args['cor_allocator_end_date'] = allocator_end_date
        portfolio_args['cor_selector_start_date'] = selector_start_date
        portfolio_args['cor_selector_end_date'] = selector_end_date
        portfolio_args['sat_alloctor_start_date'] = alloctor_start_date
        portfolio_args['sat_allocator_end_date'] = allocator_end_date
        portfolio_args['sat_selector_start_date'] = selector_start_date
        portfolio_args['sat_selector_end_date'] = selector_end_date

        weights = calc_portfolio(portfolio_args)

        debug(f'allo [{allocator_end_date.strftime("%Y %b")}]:{weights}')
        save_portfolio_weights(name=port_id, portfolio_weights=weights)

    sd = real_start_date
    create_candle_portfolio_img(port_id=port_id, compare_ticker=compare_ticker, start_date=sd, chart_type='Line')


def main():
    # portfolio_tester(init_cap=10000, port_id='parking', allocator_data_interval=3, selector_data_interval=1,
    #                  start_test_date=datetime.date(2008, 1, 1))
    pass


if __name__ == '__main__':
    # main()
    mp.set_start_method('spawn')
    q = mp.Queue()
    p1 = mp.Process(target=portfolio_tester, args=(10000, 'parking', 3, 1, datetime.date(2008, 1, 1),))
    p1.start()
    p2 = mp.Process(target=portfolio_tester, args=(10000, 'allweather', 3, 1, datetime.date(2008, 1, 1),))
    p2.start()
    # p3 = mp.Process(target=portfolio_tester, args=(10000, 'balanced', 3, 1, datetime.date(2008, 1, 1),))
    # p3.start()
    # p4 = mp.Process(target=portfolio_tester, args=(10000, 'aggressive', 3, 1, datetime.date(2008, 1, 1),))
    # p4.start()
    # p5 = mp.Process(target=portfolio_tester, args=(10000, 'leveraged', 3, 1,  datetime.date(2010, 1, 1),))
    # p5.start()
    p1.join()
    p2.join()
    # p3.join()
    # p4.join()
    # p5.join()
