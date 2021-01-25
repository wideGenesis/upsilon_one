from project_shared import *
from quotes.sql_queries import *
from datetime import date, timedelta
from charter.charter import *


def get_global_tickers():
    u_table_name = HIST_UNIVERSE_TABLE_NAME
    with engine.connect() as connection:
        if is_table_exist(u_table_name):
            res = list()
            sel_query = f'SELECT DISTINCT(ticker) FROM  {u_table_name} '
            result = connection.execute(sel_query)
            if result.rowcount > 0:
                query_result = result.fetchall()
                for item in query_result:
                    res.append(item[0])
                return res
            else:
                return None
        else:
            debug(f'Can\'t find table: {u_table_name}!')


def create_all_charts():
    local_path = PROJECT_HOME_DIR + '/tester/Universe_Charts'
    global_tickers = get_global_tickers()
    t_len = len(global_tickers)
    print_progress_bar(0, t_len, prefix='Progress:', suffix='Complete', length=50)
    for count, ticker in enumerate(global_tickers, start=1):
        create_chart_img(ticker=ticker,
                         start_date=DEFAULT_START_QUOTES_DATE,
                         chart_type='Line',
                         chart_path=local_path)
        print_progress_bar(count, t_len, prefix='Progress:', suffix=f'Complete:{ticker}:[{count}:{t_len}]   ',
                           length=50)


def main():
    debug("__Start create charts__")
    create_all_charts()


if __name__ == '__main__':
    debug("*********** Start create_all_charts ***********")
    main()


