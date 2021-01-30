from project_shared import *
from quotes.portfolios.rp_portfolio import *

"""
1000000000 - 1bln
10000000000 - 10bln
100000000000 - 100bln
50/50 denom 2 
"""


def calc_portfolio(portfolio_args):
    if portfolio_args['etf_only'] and portfolio_args['stacks_only']:
        debug('Incorrect calculation parameters', WARNING)

    # Расчет COR части портфеля
    if not portfolio_args['stacks_only']:
        cor_closes = get_closes_universe_df(etf_list=portfolio_args['cor_etf_list'],
                                            start_date=portfolio_args['cor_selector_start_date'],
                                            end_date=portfolio_args['cor_selector_end_date'])

        cor_rp = RiskParityAllocator(closes=cor_closes,
                                     cov_method=portfolio_args['cor_cov_method'],
                                     herc=portfolio_args['cor_herc'],
                                     linkage_=portfolio_args['cor_linkage_'],
                                     risk_measure_=portfolio_args['cor_risk_measure_'],
                                     graphs_show=portfolio_args['cor_graphs_show'],
                                     assets_to_hold=portfolio_args['cor_assets_to_hold'],
                                     selector_type=portfolio_args['cor_selector_type'],
                                     std_adj=portfolio_args['cor_selector_adjustment'],
                                     p1=portfolio_args['cor_selector_p1'],
                                     p2=portfolio_args['cor_selector_p2'],
                                     c_p1=portfolio_args['cor_selector_c_p1'],
                                     c_p2=portfolio_args['cor_selector_c_p2'],
                                     )
        cor_tickers = []
        cor_tickers = cor_rp.selector()
        cor_list = get_closes_by_ticker_list(cor_tickers,
                                             start_date=portfolio_args['cor_alloctor_start_date'],
                                             end_date=portfolio_args['cor_allocator_end_date'])
        cor_rp.closes_updater(new_closes=cor_list)
        cor_rp.calc_returns()
        core = cor_rp.allocator()

        # Aliases for leveraged
        if portfolio_args['port_id'] == 'leveraged' and portfolio_args['is_aliased']:
            if 'QQQ' in core:
                qqq_weight = core.pop('QQQ')
                core['QLD'] = qqq_weight
            if 'TLT' in core:
                tlt_weight = core.pop('TLT')
                core['TMF'] = tlt_weight

        if portfolio_args['etf_only']:
            return core

    sat_closes = {}
    mkt_caps = {}
    if portfolio_args['port_id'] == 'tinkoff_portfolio':
        td = timedelta(days=1)
        universe_date = portfolio_args['sat_selector_end_date'] - td
        sat_closes, mkt_caps = get_closes_universe_by_date_df(universe_date=universe_date,
                                                              u_table_name=TINKOFF_HIST_UNIVERSE_TABLE_NAME,
                                                              cap_filter=portfolio_args['sat_cap_filter'],
                                                              etf_list=portfolio_args['sat_etf_list'],
                                                              start_date=portfolio_args['sat_selector_start_date'],
                                                              end_date=portfolio_args['sat_selector_end_date'])
    elif portfolio_args['port_id'] == 'test_stacks_only':
        td = timedelta(days=1)
        universe_date = portfolio_args['sat_selector_end_date'] - td
        debug(f'Try get universe closes to {str(universe_date)}')
        sat_closes, mkt_caps = get_closes_universe_by_date_df(universe_date=universe_date,
                                                              cap_filter=portfolio_args['sat_cap_filter'],
                                                              etf_list=portfolio_args['sat_etf_list'],
                                                              start_date=portfolio_args['sat_selector_start_date'],
                                                              end_date=portfolio_args['sat_selector_end_date'])

    elif portfolio_args['port_id'] != 'tinkoff_portfolio' and portfolio_args['port_id'] != 'test_stacks_only':
        sat_closes, mkt_caps = get_closes_universe_df(cap_filter=portfolio_args['sat_cap_filter'],
                                                      etf_list=portfolio_args['sat_etf_list'],
                                                      start_date=portfolio_args['sat_selector_start_date'],
                                                      end_date=portfolio_args['sat_selector_end_date'])

    # Тут создаем и инициализируем класс, который занимется селекцией и аллокацией
    sat_rp = RiskParityAllocator(closes=sat_closes,
                                 cov_method=portfolio_args['sat_cov_method'],
                                 shrinkage_type=portfolio_args['sat_shrinkage_type'],
                                 denoise_method=portfolio_args['sat_denoise_method'],
                                 detone=portfolio_args['sat_detone'],
                                 herc=portfolio_args['sat_herc'],
                                 linkage_=portfolio_args['sat_linkage_'],
                                 risk_measure_=portfolio_args['sat_risk_measure_'],
                                 graphs_show=portfolio_args['sat_graphs_show'],
                                 assets_to_hold=portfolio_args['sat_assets_to_hold'],
                                 selector_type=portfolio_args['sat_selector_type'],
                                 std_adj=portfolio_args['sat_selector_adjustment'],
                                 p1=portfolio_args['sat_selector_p1'],
                                 p2=portfolio_args['sat_selector_p2'],
                                 c_p1=portfolio_args['sat_selector_c_p1'],
                                 c_p2=portfolio_args['sat_selector_c_p2'],
                                 mkt_caps=mkt_caps,
                                 cap_weight=portfolio_args['sat_cap_weight'],
                                 cap_limit_1=portfolio_args['cap_limit_1']
                                 )
    sat_tickers = []
    sat_tickers = sat_rp.selector()
    sat_list = get_closes_by_ticker_list(sat_tickers,
                                         start_date=portfolio_args['sat_alloctor_start_date'],
                                         end_date=portfolio_args['sat_allocator_end_date'])
    sat_rp.closes_updater(new_closes=sat_list)
    sat_rp.calc_returns()
    satellite = sat_rp.allocator()
    if portfolio_args['stacks_only']:
        return satellite

    weights = core_sat(cor=core,
                       cor_perc=portfolio_args['cor_perc'],
                       sat=satellite,
                       sat_perc=portfolio_args['sat_perc'])
    return weights
