from project_shared import *
from quotes.parsers_env import chrome_init, agents
from quotes.parsers import advance_decline, vix_curve, get_sma50
from time import sleep
from charter.charter import *

if __name__ == '__main__':
    debug_init(file_name="cron_scheduler.log")
    debug(f"### Start cron every 120 min scheduler ###")
    img_out_path = PROJECT_HOME_DIR + '/' + IMAGES_OUT_PATH
    debug(img_out_path)
    advance_decline(ag=agents(), img_out_path_=img_out_path)
    vix_curve(driver=chrome_init(), img_out_path_=img_out_path)

    # Every 125 min
    sleep(300)
    get_sma50(ag=agents(), img_out_path_=img_out_path)
    debug_deinit()
