from project_shared import *
from quotes.portfolios.sql_queries import *


def save_portfolio_weights(name="portfolio", portfolio_weights=None):
    if not is_table_exist(PORTFOLIO_ALLOCATION_TABLE_NAME):
        create_portfolio_allocation_table()
    update_portfolio_allocation(port_id=name, weights=portfolio_weights)


def save_portfolio_bars(name="portfolio", portfolio_bars=None):
    if not is_table_exist(PORTFOLIO_BARS_TABLE_NAME):
        create_portfolio_bars_table()
    insert_portfolio_bars(port_id=name, bar_list=portfolio_bars)