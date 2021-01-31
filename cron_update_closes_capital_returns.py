import argparse
from project_shared import *
from quotes.quote_loader import *
from quotes.portfolios.portfolios_calc import *
from quotes.portfolios.portfolios_save import *
from charter.charter import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set log filename')
    parser.add_argument("--fname", default="cron_scheduler.log", help="This is the 'a' variable")
    args = parser.parse_args()
    log_file_name = args.fname

    # debug_init(file_name=log_file_name)
    debug(f"### Start update universe prices ###")
    # update_universe_prices1()

    debug(f"### Start update VIX prices ###")
    universe = ['VIX']
    # eod_update_universe_prices(universe)

    td = timedelta(days=365)
    ed = date.today()
    sd = ed - td

    debug("Calc capital for parking")
    # ======================================== P A R K I N G ========================================
    port_id = 'parking'
    ohlc = get_ohlc_dict_by_port_id_w(port_id=port_id, start_date=sd, end_date=ed)
    portfolio_bars, portfolio_returns = returns_calc_w(data=ohlc)
    save_portfolio_bars(name=port_id, portfolio_bars=portfolio_bars)
    save_portfolio_returns(name=port_id, portfolio_returns=portfolio_returns)
    create_candle_portfolio_img(port_id=port_id, compare_ticker="TLT", start_date=sd, end_date=ed)

    debug("Calc capital for allweather")
    # ======================================== A L L W E A T H E R ========================================
    port_id = 'allweather'
    ohlc = get_ohlc_dict_by_port_id_w(port_id=port_id, start_date=sd, end_date=ed)
    portfolio_bars, portfolio_returns = returns_calc_w(data=ohlc)
    save_portfolio_bars(name=port_id, portfolio_bars=portfolio_bars)
    save_portfolio_returns(name=port_id, portfolio_returns=portfolio_returns)
    create_candle_portfolio_img(port_id=port_id, compare_ticker="SPY", start_date=sd, end_date=ed)

    debug("Calc capital for balanced")
    # ======================================== B A L A N C E D ========================================
    port_id = 'balanced'
    ohlc = get_ohlc_dict_by_port_id_w(port_id=port_id, start_date=sd, end_date=ed)
    portfolio_bars, portfolio_returns = returns_calc_w(data=ohlc)
    save_portfolio_bars(name=port_id, portfolio_bars=portfolio_bars)
    save_portfolio_returns(name=port_id, portfolio_returns=portfolio_returns)
    create_candle_portfolio_img(port_id=port_id, compare_ticker="QQQ", start_date=sd, end_date=ed)

    debug("Calc capital for aggressive")
    # ======================================== A G G R E S S I V E ========================================
    port_id = 'aggressive'
    ohlc = get_ohlc_dict_by_port_id_w(port_id=port_id, start_date=sd, end_date=ed)
    portfolio_bars, portfolio_returns = returns_calc_w(data=ohlc)
    save_portfolio_bars(name=port_id, portfolio_bars=portfolio_bars)
    save_portfolio_returns(name=port_id, portfolio_returns=portfolio_returns)
    create_candle_portfolio_img(port_id=port_id, compare_ticker="QQQ", start_date=sd, end_date=ed)

    debug("Calc capital for leveraged")
    # ======================================== L E V E R A G E D ========================================
    port_id = 'leveraged'
    ohlc = get_ohlc_dict_by_port_id_w(port_id=port_id, start_date=sd, end_date=ed)
    portfolio_bars, portfolio_returns = returns_calc_w(data=ohlc)
    save_portfolio_bars(name=port_id, portfolio_bars=portfolio_bars)
    save_portfolio_returns(name=port_id, portfolio_returns=portfolio_returns)
    create_candle_portfolio_img(port_id=port_id, compare_ticker="QQQ", start_date=sd, end_date=ed)
    debug("%%%%%%%%%%%%%%%Complete update closes and capital returns\n\n\n")
    debug_deinit()
