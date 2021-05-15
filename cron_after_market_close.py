from project_shared import *
from quotes.quote_loader import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set log filename')
    parser.add_argument("--fname", default="cron_scheduler.log", help="This is the 'a' variable")
    args = parser.parse_args()
    log_file_name = args.fname

    debug_init(file_name=log_file_name)
    debug(f"### Start cron after market close scheduler ###")

    start_date = datetime.datetime.now()-timedelta(days=1)
    update_db_last_ohlc_data(BENCHMARKS, start_date)
