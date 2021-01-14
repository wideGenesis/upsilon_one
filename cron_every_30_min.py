from project_shared import *
from quotes.parsers_env import chrome_init, firefox_init
from quotes.parsers import get_tw_charts, get_finviz_treemaps, get_coins360_treemaps
from charter.charter import *


if __name__ == '__main__':
    debug_init(file_name="cron_scheduler.log")
    debug(f"### Start cron every 30 min scheduler ###")
    img_out_path = PROJECT_HOME_DIR + '/' + IMAGES_OUT_PATH
    debug(img_out_path)
    get_tw_charts(driver=chrome_init(), img_out_path_=img_out_path)
    get_finviz_treemaps(driver=firefox_init(), img_out_path_=img_out_path)
    # get_finviz_treemaps(driver=chrome_init(), img_out_path_=img_out_path)
    get_coins360_treemaps(driver=chrome_init(), img_out_path_=img_out_path)
    debug("%%%%%%%%%%%%%%%Complete Cron Every 30\n\n\n")
    debug_deinit()
