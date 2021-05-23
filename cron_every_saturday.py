import argparse
from project_shared import *
from quotes import screeners as scr
from charter.charter import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set log filename')
    parser.add_argument("--fname", default="cron_scheduler.log", help="This is the 'a' variable")
    args = parser.parse_args()
    log_file_name = args.fname

    debug_init(file_name=log_file_name)
    debug(f"### Start cron every Saturday scheduler ###")

    rocket = scr.GuruRocketScreener(guru=False)
    post = rocket.publish_to_telegraph()
    rocket_link_file = f'{PROJECT_HOME_DIR}/results/gururocketscreener/rocket.lnk'
    with open(rocket_link_file, 'w') as f:
        f.write(f"{post['url']}")

    guru = scr.GuruRocketScreener(guru=True)
    post = guru.publish_to_telegraph()
    guru_link_file = f'{PROJECT_HOME_DIR}/results/gururocketscreener/guru.lnk'
    with open(guru_link_file, 'w') as f:
        f.write(f"{post['url']}")

    debug("%%%%%%%%%%%%%%%Complete every Saturday\n\n\n")
    debug_deinit()
