from project_shared import *
from quotes.parsers import qt_curve, spx_yield, vix_cont
from charter.charter import *

if __name__ == '__main__':
    debug_init(file_name="cron_scheduler.log")
    debug(f"### Start cron every 480 min scheduler ###")
    img_out_path = PROJECT_HOME_DIR + '/' + IMAGES_OUT_PATH
    debug(img_out_path)
    qt_curve(img_out_path_=img_out_path)
    spx_yield(img_out_path_=img_out_path)
    vix_cont(img_out_path_=img_out_path)
    debug("%%%%%%%%%%%%%%%Comlete every 480\n\n\n")
    debug_deinit()
