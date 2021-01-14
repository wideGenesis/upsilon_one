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

if __name__ == '__main__':
    debug_init(file_name="cron_scheduler.log")
    debug(f"### Start update universe prices ###")
    update_universe_prices1()

    td = timedelta(days=365)
    ed = date.today()
    sd = ed - td

    debug("Calc capital for parking")
    # ======================================== P A R K I N G ========================================
    port_id = 'parking'
    ohlc = get_ohlc_dict_by_port_id(port_id=port_id, start_date=sd, end_date=ed)
    portfolio_bars, portfolio_returns = returns_calc(ohlc=ohlc)
    save_portfolio_bars(name=port_id, portfolio_bars=portfolio_bars)
    save_portfolio_returns(name=port_id, portfolio_returns=portfolio_returns)
    create_candle_portfolio_img(port_id=port_id, compare_ticker="TLT", start_date=sd, end_date=ed)

    debug("Calc capital for allweather")
    # ======================================== A L L W E A T H E R ========================================
    port_id = 'allweather'
    ohlc = get_ohlc_dict_by_port_id(port_id=port_id, start_date=sd, end_date=ed)
    portfolio_bars, portfolio_returns = returns_calc(ohlc=ohlc)
    save_portfolio_bars(name=port_id, portfolio_bars=portfolio_bars)
    save_portfolio_returns(name=port_id, portfolio_returns=portfolio_returns)
    create_candle_portfolio_img(port_id=port_id, compare_ticker="SPY", start_date=sd, end_date=ed)

    debug("Calc capital for balanced")
    # ======================================== B A L A N C E D ========================================
    port_id = 'balanced'
    ohlc = get_ohlc_dict_by_port_id(port_id=port_id, start_date=sd, end_date=ed)
    portfolio_bars, portfolio_returns = returns_calc(ohlc=ohlc)
    save_portfolio_bars(name=port_id, portfolio_bars=portfolio_bars)
    save_portfolio_returns(name=port_id, portfolio_returns=portfolio_returns)
    create_candle_portfolio_img(port_id=port_id, compare_ticker="QQQ", start_date=sd, end_date=ed)

    debug("Calc capital for aggressive")
    # ======================================== A G G R E S S I V E ========================================
    port_id = 'aggressive'
    ohlc = get_ohlc_dict_by_port_id(port_id=port_id, start_date=sd, end_date=ed)
    portfolio_bars, portfolio_returns = returns_calc(ohlc=ohlc)
    save_portfolio_bars(name=port_id, portfolio_bars=portfolio_bars)
    save_portfolio_returns(name=port_id, portfolio_returns=portfolio_returns)
    create_candle_portfolio_img(port_id=port_id, compare_ticker="QQQ", start_date=sd, end_date=ed)

    debug("Calc capital for leveraged")
    # ======================================== L E V E R A G E D ========================================
    port_id = 'leveraged'
    ohlc = get_ohlc_dict_by_port_id(port_id=port_id, start_date=sd, end_date=ed)
    portfolio_bars, portfolio_returns = returns_calc(ohlc=ohlc)
    save_portfolio_bars(name=port_id, portfolio_bars=portfolio_bars)
    save_portfolio_returns(name=port_id, portfolio_returns=portfolio_returns)
    create_candle_portfolio_img(port_id=port_id, compare_ticker="QQQ", start_date=sd, end_date=ed)
    debug_deinit()
    debug("Complete update closes and capital returns")