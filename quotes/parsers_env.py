import os
import pathlib
from time import sleep
from random import choice
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from project_shared import *


def agents():
    # ua = [
    #     'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
    #     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36',
    #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    #     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
    #     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    #     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0',
    #     'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    #
    # ]
    # return choice(ua)
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    return ua


# def firefox_init(webdriver_path=WEBDRIVER, agent_rotation=agents()):
#     profile = webdriver.FirefoxProfile()
#     profile.set_preference("network.http.use-cache", False)
#     profile.set_preference("javascript.enabled", True)
#     profile.set_preference("general.useragent.override", f"{agent_rotation}")
#     ff_options = webdriver.FirefoxOptions()
#     ff_options.add_argument('-window-size=1980,1080')
#     ff_options.add_argument('-headless')
#
#
# def firefox_init(webdriver_path=WEBDRIVER, agent_rotation=agents()):
#     driver = webdriver.Firefox(executable_path=os.path.join(webdriver_path, 'geckodriver_0_28'),
#                                firefox_profile=profile, options=ff_options)
#     p = str(pathlib.Path('adblock_for_firefox-4.24.1-fx.xpi').parent.absolute()) + \
#         '/webdriver/adblock_for_firefox-4.24.1-fx.xpi'
#     driver.install_addon(str(os.path.abspath(p)), temporary=True)
#     driver.maximize_window()
#     sleep(1)
#     print(driver.execute_script("return navigator.userAgent"))
#     print('Firefox has been initialized')
#     return driver


def chrome_opt(agent_rotation=agents(), headless=True):
    chrome_options = Options()

    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # chrome_options.add_argument("--proxy-server==localhost:6969")
    # chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--proxy-server=direct://")
    # chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    if headless:
        chrome_options.add_argument("--headless")
    else:
        pass
    # chrome_options.add_argument("--incognito")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument(f'user-agent={agent_rotation}')
    chrome_options.add_argument("--enable-javascript")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("user-data-dir=/home/upsilonsfather/.config/google-chrome")
    return chrome_options


def chrome_init(webdriver_path=WEBDRIVER, agent_rotation=agents(), chrome_options=chrome_opt()):

    driver_path = os.path.join(webdriver_path, 'chromedriver_87')
    driver = webdriver.Chrome(driver_path, options=chrome_options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": f'{agent_rotation}'})
    print(driver.execute_script("return navigator.userAgent"))
    print('Chrome has been initialized')
    return driver
