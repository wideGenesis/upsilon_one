from project_shared import *
from quotes.quote_loader import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set log filename')
    parser.add_argument("--fname", default="cron_scheduler.log", help="This is the 'a' variable")
    args = parser.parse_args()
    log_file_name = args.fname

    debug_init(file_name=log_file_name)
    debug(f"### Start cron on market open scheduler ###")

    ohlc_data_updater_yq(BENCHMARKS, table_name=BENCHMARKS_QUOTES_TABLE_NAME, is_update=True)

    debug("%%%%%%%%%%%%%%%Complete on market open \n\n\n")
    debug_deinit()
