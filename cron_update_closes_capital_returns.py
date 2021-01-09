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
    debug(f"### Start update universe prices ###")
    update_universe_prices1()

    td = timedelta(days=365)
    ed = date.today()
    sd = ed - td

    # ======================================== P A R K I N G ========================================
    ohlc = get_ohlc_dict_by_port_id('parking', start_date=sd, end_date=ed)
    portfolio_bars, portfolio_returns = returns_calc(ohlc=ohlc)
    save_portfolio_bars(name="parking", portfolio_bars=portfolio_bars)
    create_candle_portfolio_img(port_id="parking", compare_ticker="TLT", start_date=sd, end_date=ed)

