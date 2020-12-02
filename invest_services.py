import os
import yaml
from quotes.parsers_env import firefox_init, chrome_init, agents
from parsers import get_flows, advance_decline, get_finviz_treemaps,\
    get_coins360_treemaps, get_economics, get_sma50, get_tw_charts
import schedule
from time import sleep

conf = yaml.safe_load(open('config/settings.yaml'))
LOGS = conf['PATHS']['LOGS']
WEBDRIVER = conf['PATHS']['WEBDRIVER']
IMAGES_OUT_PATH = conf['PATHS']['IMAGES_OUT_PATH']


def main():
    get_flows(driver=firefox_init(webdriver_path=WEBDRIVER, agent_rotation=agents()), img_out_path_=IMAGES_OUT_PATH)
    advance_decline(ag=agents())
    get_finviz_treemaps(driver=firefox_init(webdriver_path=WEBDRIVER, agent_rotation=agents()),
                        img_out_path_=IMAGES_OUT_PATH)
    get_coins360_treemaps(driver=firefox_init(webdriver_path=WEBDRIVER, agent_rotation=agents()),
                          img_out_path_=IMAGES_OUT_PATH)
    get_economics(ag=agents(), img_out_path_=IMAGES_OUT_PATH)
    get_sma50(ag=agents())
    get_tw_charts(driver=chrome_init(webdriver_path=WEBDRIVER, agent_rotation=agents()), img_out_path_=IMAGES_OUT_PATH)

    # schedule.every(1440).minutes.do(get_crypto)
    # schedule.every(15).minutes.do(get_coins360_treemaps)
    # schedule.every(15).minutes.do(tw_multi_render)
    # schedule.every(60).minutes.do(advance_decline)
    # schedule.every(720).minutes.do(get_etf_flows)
    # schedule.every(15).minutes.do(get_finviz)
    # schedule.every(480).minutes.do(get_indicies)
    # schedule.every().monday.do(scrape_economics)

    while True:
        schedule.run_pending()
        sleep(5)


if __name__ == '__main__':
    print(f"Starting scrapers {os.path.realpath(__file__)}, this may take a while")
    main()


if __name__ == '__main__':
    pass



