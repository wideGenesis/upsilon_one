from project_shared import *
import argparse
from quotes.parsers_env import chrome_init, firefox_init
from quotes.parsers import get_tw_charts, get_finviz_treemaps, get_coins360_treemaps, get_moex
from charter.charter import *
from quotes import quote_loader as ql


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set log filename')
    parser.add_argument("--fname", default="cron_scheduler.log", help="This is the 'a' variable")
    args = parser.parse_args()
    log_file_name = args.fname

    debug_init(file_name=log_file_name)
    debug(f"### Start cron every 30 min scheduler ###")
    img_out_path = PROJECT_HOME_DIR + '/' + IMAGES_OUT_PATH
    debug(img_out_path)
    get_tw_charts(driver=chrome_init(), img_out_path_=img_out_path)
    get_moex(driver=chrome_init(), img_out_path_=img_out_path)
    get_finviz_treemaps(driver=firefox_init(), img_out_path_=img_out_path)
    # get_finviz_treemaps(driver=chrome_init(), img_out_path_=img_out_path)
    get_coins360_treemaps(driver=chrome_init(), img_out_path_=img_out_path)
    ql.ohlc_data_updater(BENCHMARKS, table_name=BENCHMARKS_QUOTES_TABLE_NAME, is_update=True)
    debug("%%%%%%%%%%%%%%%Complete Cron Every 30\n\n\n")
    debug_deinit()
