import argparse
from quotes.get_universe import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set log filename')
    parser.add_argument("--fname", default="cron_scheduler.log", help="This is the 'a' variable")
    args = parser.parse_args()
    log_file_name = args.fname

    debug_init(file_name=log_file_name)
    debug(f"### Start eod_get_and_save_holdings ###")
    eod_get_and_save_holdings()
    debug_deinit()
