from project_shared import *
from quotes.portfolios.rp_portfolio import *

"""
1000000000 - 1bln
10000000000 - 10bln
100000000000 - 100bln
50/50 denom 2 
"""


def calc_portfolio(portfolio_args):
    cor_closes = get_closes_universe_df(etf_list=portfolio_args['cor_etf_list'],
                                        start_date=portfolio_args['cor_selector_start_date'],
                                        end_date=portfolio_args['cor_selector_end_date'])
    cor_select = Selector(closes=cor_closes,
                          assets_to_hold=portfolio_args['cor_assets_to_hold'],
                          selectors_mode=portfolio_args['cor_selectors_mode'])
    cor_tickers = []
    if portfolio_args['cor_selector_type'] == 'rs_sharpe':
        cor_tickers = cor_select.rs_sharpe()
    elif portfolio_args['cor_selector_type'] == 'momentum':
        cor_tickers = cor_select.momentum()

    cor_list = get_closes_by_ticker_list(cor_tickers,
                                         start_date=portfolio_args['cor_alloctor_start_date'],
                                         end_date=portfolio_args['cor_allocator_end_date'])
    cor_rp = RiskParityAllocator(closes=cor_list,
                                 cov_method=portfolio_args['cor_cov_method'],
                                 herc=portfolio_args['cor_herc'],
                                 linkage_=portfolio_args['cor_linkage_'],
                                 risk_measure_=portfolio_args['cor_risk_measure_'],
                                 graphs_show=portfolio_args['cor_graphs_show'])
    cor_rp.calc_returns()
    core = cor_rp.allocator()
    if portfolio_args['etf_only']:
        return core
    else:
        sat_closes = get_closes_universe_df(cap_filter=portfolio_args['sat_cap_filter'],
                                            etf_list=portfolio_args['sat_etf_list'],
                                            start_date=portfolio_args['sat_selector_start_date'],
                                            end_date=portfolio_args['sat_selector_end_date'])
        sat_select = Selector(closes=sat_closes,
                              assets_to_hold=portfolio_args['sat_assets_to_hold'],
                              selectors_mode=portfolio_args['sat_selectors_mode'])

        sat_tickers = []
        if portfolio_args['sat_selector_type'] == 'rs_sharpe':
            sat_tickers = sat_select.rs_sharpe()
        elif portfolio_args['sat_selector_type'] == 'momentum':
            sat_tickers = cor_select.momentum()

        sat_list = get_closes_by_ticker_list(sat_tickers,
                                             start_date=portfolio_args['sat_alloctor_start_date'],
                                             end_date=portfolio_args['sat_allocator_end_date'])
        sat_rp = RiskParityAllocator(closes=sat_list,
                                     cov_method=portfolio_args['sat_cov_method'],
                                     herc=portfolio_args['sat_herc'],
                                     linkage_=portfolio_args['sat_linkage_'],
                                     risk_measure_=portfolio_args['sat_risk_measure_'],
                                     graphs_show=portfolio_args['sat_graphs_show'])
        sat_rp.calc_returns()
        satellite = sat_rp.allocator()

        weights = core_sat(cor=core,
                           cor_perc=portfolio_args['cor_perc'],
                           sat=satellite,
                           sat_perc=portfolio_args['sat_perc'])
        return weights


def parking_portfolio(start_date=None, end_date=date.today(), **kwargs):
    # cor_closes = get_closes_universe_df(cap_filter=200000000000, etf_list=PARKING)
    cor_closes = get_closes_universe_df(etf_list=PARKING, start_date=start_date, end_date=end_date)
    cor_select = Selector(closes=cor_closes, assets_to_hold=4, selectors_mode=1, performance_period=21)
    # cor_tickers = cor_select.rs_sharpe()
    cor_tickers = cor_select.momentum()
    cor_list = get_closes_by_ticker_list(cor_tickers)
    cor_rp = RiskParityAllocator(closes=cor_list, cov_method='semi', herc=False, linkage_='ward',
                                 risk_measure_='variance', graphs_show=False)
    cor_rp.calc_returns()
    core = cor_rp.allocator()
    return core

    # sat_closes = get_closes_universe_df(cap_filter=100000000000, etf_list=None)
    # sat_select = Selector(closes=sat_closes, assets_to_hold=4)
    # sat_tickers = sat_select.rs_sharpe()
    # sat_list = get_closes_by_ticker_list(sat_tickers, start_date=start_date, end_date=end_date)
    # sat_rp = RiskParityAllocator(closes=sat_list, cov_method='semi', herc=False, linkage_='ward',
    #                              risk_measure_='variance', graphs_show=False)
    # sat_rp.calc_returns()
    # satellite = sat_rp.allocator()
    #
    # weights = core_sat(cor=core, cor_perc=0.9, sat=satellite, sat_perc=0.1)
    # return weights


def allweather_portfolio(start_date=None, end_date=date.today()):
    # cor_closes = get_closes_universe_df(cap_filter=200000000000, etf_list=ALL_WEATHER)
    cor_closes = get_closes_universe_df(etf_list=ALL_WEATHER, start_date=start_date, end_date=end_date)
    cor_select = Selector(closes=cor_closes, assets_to_hold=4, selectors_mode=1, performance_period=21)
    cor_tickers = cor_select.rs_sharpe()
    cor_tickers = cor_select.momentum()
    cor_list = get_closes_by_ticker_list(cor_tickers)
    cor_rp = RiskParityAllocator(closes=cor_list, cov_method='semi', herc=False, linkage_='ward',
                                 risk_measure_='variance', graphs_show=False)
    cor_rp.calc_returns()
    core = cor_rp.allocator()
    return core

    # sat_closes = get_closes_universe_df(cap_filter=150000000000, etf_list=None)
    # sat_select = Selector(closes=sat_closes, assets_to_hold=6)
    # sat_tickers = sat_select.rs_sharpe()
    # sat_list = get_closes_by_ticker_list(sat_tickers, start_date=start_date, end_date=end_date)
    # sat_rp = RiskParityAllocator(closes=sat_list, cov_method='semi', herc=False, linkage_='ward',
    #                              risk_measure_='variance', graphs_show=False)
    # sat_rp.calc_returns()
    # satellite = sat_rp.allocator()
    #
    # weights = core_sat(cor=core, cor_perc=0.8, sat=satellite, sat_perc=0.2)
    # return weights


def balanced_portfolio(start_date=None, end_date=date.today()):
    # cor_closes = get_closes_universe_df(cap_filter=200000000000, etf_list=BALANCED)
    cor_closes = get_closes_universe_df(etf_list=BALANCED, start_date=start_date, end_date=end_date)
    cor_select = Selector(closes=cor_closes, assets_to_hold=3, selectors_mode=1, performance_period=21)
    # cor_tickers = cor_select.rs_sharpe()
    cor_tickers = cor_select.momentum()
    cor_list = get_closes_by_ticker_list(cor_tickers)
    cor_rp = RiskParityAllocator(closes=cor_list, cov_method='semi', herc=False, linkage_='ward',
                                 risk_measure_='variance', graphs_show=False)
    cor_rp.calc_returns()
    core = cor_rp.allocator()
    # debug(f'CORE:{core}')    return core
    return core

    # sat_closes = get_closes_universe_df(cap_filter=100000000000, etf_list=None)
    # sat_select = Selector(closes=sat_closes, assets_to_hold=7)
    # sat_tickers = sat_select.rs_sharpe()
    # sat_list = get_closes_by_ticker_list(sat_tickers, start_date=start_date, end_date=end_date)
    # sat_rp = RiskParityAllocator(closes=sat_list, cov_method='semi', herc=False, linkage_='ward',
    #                              risk_measure_='variance', graphs_show=False)
    # sat_rp.calc_returns()
    # satellite = sat_rp.allocator()
    #
    # weights = core_sat(cor=core, cor_perc=0.7, sat=satellite, sat_perc=0.3)
    # return weights


def aggressive_portfolio(start_date=None, end_date=date.today()):
    # cor_closes = get_closes_universe_df(cap_filter=200000000000, etf_list=AGGRESSIVE)
    cor_closes = get_closes_universe_df(etf_list=AGGRESSIVE, start_date=start_date, end_date=end_date)
    cor_select = Selector(closes=cor_closes, assets_to_hold=3, selectors_mode=1, performance_period=21)
    # cor_tickers = cor_select.rs_sharpe()
    cor_tickers = cor_select.momentum()
    cor_list = get_closes_by_ticker_list(cor_tickers)
    cor_rp = RiskParityAllocator(closes=cor_list, cov_method='semi', herc=False, linkage_='ward',
                                 risk_measure_='conditional_drawdown_risk', graphs_show=False)
    cor_rp.calc_returns()
    core = cor_rp.allocator()
    return core

    # sat_closes = get_closes_universe_df(cap_filter=5000000000, etf_list=None)
    # sat_select = Selector(closes=sat_closes, assets_to_hold=7)
    # sat_tickers = sat_select.rs_sharpe()
    # sat_list = get_closes_by_ticker_list(sat_tickers, start_date=start_date, end_date=end_date)
    # sat_rp = RiskParityAllocator(closes=sat_list, cov_method='semi', herc=False, linkage_='ward',
    #                              risk_measure_='variance', graphs_show=False)
    # sat_rp.calc_returns()
    # satellite = sat_rp.allocator()
    #
    # weights = core_sat(cor=core, cor_perc=0.7, sat=satellite, sat_perc=0.3)
    # return weights


def leveraged_portfolio(start_date=None, end_date=date.today()):
    # cor_closes = get_closes_universe_df(cap_filter=200000000000, etf_list=LEVERAGED)
    cor_closes = get_closes_universe_df(etf_list=LEVERAGED, start_date=start_date, end_date=end_date)
    cor_select = Selector(closes=cor_closes, assets_to_hold=3, selectors_mode=1, performance_period=21)
    # cor_tickers = cor_select.rs_sharpe()
    cor_tickers = cor_select.momentum()
    cor_list = get_closes_by_ticker_list(cor_tickers)
    cor_rp = RiskParityAllocator(closes=cor_list, cov_method='semi', herc=False, linkage_='ward',
                                 risk_measure_='variance', graphs_show=False)
    cor_rp.calc_returns()
    core = cor_rp.allocator()
    return core

    # sat_closes = get_closes_universe_df(cap_filter=20000000000, etf_list=None)
    # sat_select = Selector(closes=sat_closes, assets_to_hold=9)
    # sat_tickers = sat_select.rs_sharpe()
    # sat_list = get_closes_by_ticker_list(sat_tickers, start_date=start_date, end_date=end_date)
    # sat_rp = RiskParityAllocator(closes=sat_list, cov_method='semi', herc=False, linkage_='ward',
    #                              risk_measure_='variance', graphs_show=False)
    # sat_rp.calc_returns()
    # satellite = sat_rp.allocator()
    #
    # weights = core_sat(cor=core, cor_perc=0.65, sat=satellite, sat_perc=0.35)
    # return weights