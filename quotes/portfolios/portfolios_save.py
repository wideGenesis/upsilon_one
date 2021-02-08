from project_shared import *
from quotes.portfolios.sql_queries import *


def save_portfolio_weights(name="portfolio", portfolio_weights=None, allocation_date=date.today()):
    # ===== Сохраним текущую аллокацию =====
    # Для справки: она всегда перезаписывается, то есть старая аллокация всегда удаляется, а новая пишетя
    # Таким образом в таблице всегда одна - текущая аллокация
    if not is_table_exist(PORTFOLIO_ALLOCATION_TABLE_NAME):
        create_portfolio_allocation_table()
    update_portfolio_allocation(port_id=name, weights=portfolio_weights)


def save_hist_portfolio_weights(name="portfolio", portfolio_weights=None, allocation_date=date.today()):
    # ===== Сохраним текущую аллокацию в историческую таблицу =====
    # Для справки: она по умолчанию НЕ  перезаписывается, то есть если аллокация на эту дату уже есть
    # то она не перезапишется, если не подать в функцию спецаргумент overwrite=True
    # Таким образом в таблицу попдает расчетная аллокация и остаетя там
    if not is_table_exist(HIST_PORT_ALLOCATION_TABLE_NAME):
        create_hist_port_allocation_table()
    update_hist_port_allocation(port_id=name, weights=portfolio_weights, allo_date=allocation_date)


def save_portfolio_bars(name="portfolio", portfolio_bars=None):
    if not is_table_exist(PORTFOLIO_BARS_TABLE_NAME):
        create_portfolio_bars_table()
    insert_portfolio_bars(port_id=name, bar_list=portfolio_bars)


def save_portfolio_returns(name="portfolio", portfolio_returns=None):
    if not is_table_exist(PORTFOLIO_RETURNS_TABLE_NAME):
        create_portfolio_returns_table()
    insert_portfolio_returns(port_id=name, returns=portfolio_returns)