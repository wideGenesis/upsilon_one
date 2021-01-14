from project_shared import *
from quotes.parsers_env import chrome_init, agents
from quotes.parsers import get_economics
from charter.charter import *


if __name__ == '__main__':
    debug_init(file_name="cron_scheduler.log")
    debug(f"### Start cron every 720 min scheduler ###")
    img_out_path = PROJECT_HOME_DIR + '/' + IMAGES_OUT_PATH
    debug(img_out_path)
    get_economics(ag=agents(), img_out_path_=img_out_path)
    debug_deinit()
