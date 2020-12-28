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


def portfolio_tester(init_cap=10000, port_id='parking', data_interval=-3, start_test_date=datetime.date(2019, 1, 1)):
    in_cap = init_cap
    compare_ticker = ""
    wend_date = start_test_date
    wstart_date = add_months(wend_date, data_interval)
    debug(f'Port_id={port_id}  wend_date={wend_date}  wstart_date={wstart_date}')

    weights = {}
    if port_id == 'parking':
        weights = parking_portfolio(wstart_date, wend_date)
        compare_ticker = "TLT"
    elif port_id == 'allweather':
        weights = allweather_portfolio(wstart_date, wend_date)
        compare_ticker = "TLT"
    elif port_id == 'balanced':
        weights = balanced_portfolio(wstart_date, wend_date)
        compare_ticker = "QQQ"
    elif port_id == 'aggressive':
        weights = aggressive_portfolio(wstart_date, wend_date)
        compare_ticker = "QQQ"
    elif port_id == 'leveraged':
        weights = leveraged_portfolio(wstart_date, wend_date)
        compare_ticker = "QQQ"

    debug(f'Start allo({port_id}) [{wend_date}]:{weights}')
    save_portfolio_weights(name=port_id, portfolio_weights=weights)

    while wend_date <= date.today():
        wend_date = add_months(wend_date, 1)
        wstart_date = add_months(wend_date, data_interval)
        pstart_date = add_months(wend_date, -1)

        ohlc = get_ohlc_dict_by_port_id(port_id, start_date=pstart_date, end_date=wend_date)
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

        if port_id == 'parking':
            weights = parking_portfolio(wstart_date, wend_date)
        elif port_id == 'allweather':
            weights = allweather_portfolio(wstart_date, wend_date)
        elif port_id == 'balanced':
            weights = balanced_portfolio(wstart_date, wend_date)
        elif port_id == 'aggressive':
            weights = aggressive_portfolio(wstart_date, wend_date)
        elif port_id == 'leveraged':
            weights = leveraged_portfolio(wstart_date, wend_date)

        debug(f'allo [{wend_date.strftime("%Y %b")}]:{weights}')
        save_portfolio_weights(name=port_id, portfolio_weights=weights)

    sd = start_test_date
    create_candle_portfolio_img(port_id=port_id, compare_ticker=compare_ticker, start_date=sd, chart_type='Line')


def main():
    portfolio_tester(init_cap=10000, port_id='parking', data_interval=-3, start_test_date=datetime.date(2007, 1, 1))


if __name__ == '__main__':
    # main()
    mp.set_start_method('spawn')
    q = mp.Queue()
    p1 = mp.Process(target=portfolio_tester, args=(10000, 'parking', -3, datetime.date(2007, 1, 1),))
    p1.start()
    p2 = mp.Process(target=portfolio_tester, args=(10000, 'allweather', -3, datetime.date(2007, 1, 1),))
    p2.start()
    p3 = mp.Process(target=portfolio_tester, args=(10000, 'balanced', -3, datetime.date(2007, 1, 1),))
    p3.start()
    p4 = mp.Process(target=portfolio_tester, args=(10000, 'aggressive', -3, datetime.date(2007, 1, 1),))
    p4.start()
    # p5 = mp.Process(target=portfolio_tester, args=(10000, 'leveraged', -3, datetime.date(2007, 1, 1),))
    # p5.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    # p5.join()
