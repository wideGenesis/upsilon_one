from quotes.get_universe import *

if __name__ == '__main__':
    debug_init(file_name="cron_scheduler.log")
    debug(f"### Start eod_get_and_save_holdings ###")
    eod_get_and_save_holdings()
    debug_deinit()
