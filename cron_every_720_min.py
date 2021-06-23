import argparse
from project_shared import *
from quotes.parsers_env import chrome_init
from quotes import sql_queries as sql_q
from quotes import quote_loader as ql
from charter.charter import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set log filename')
    parser.add_argument("--fname", default="cron_scheduler.log", help="This is the 'a' variable")
    args = parser.parse_args()
    log_file_name = args.fname

    debug_init(file_name=log_file_name)
    debug(f"### Start cron every 720 min scheduler ###")
    img_out_path = PROJECT_HOME_DIR + '/' + IMAGES_OUT_PATH
    debug(img_out_path)
    # get_etfdb_flows(driver=chrome_init(), img_out_path_=img_out_path)
    # get_flows(driver=chrome_init(), img_out_path_=img_out_path)
    currency = 'RUB=X'
    last_usd_price = ql.get_last_currency_price_yq(currency)
    sql_q.update_last_currency_price(currency, last_usd_price)
    debug(f'{currency} LAST_PRICE == {last_usd_price}')
    debug("%%%%%%%%%%%%%%%Complete cron every 720\n\n\n")
    debug_deinit()
