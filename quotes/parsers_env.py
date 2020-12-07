import os
import pathlib
from time import sleep
from random import choice
# from bs4 import BeautifulSoup
# from mitmproxy import ctx
# from mitmproxy import http
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def firefox_init(webdriver_path, agent_rotation):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.http.use-cache", False)
    profile.set_preference("javascript.enabled", True)
    profile.set_preference("general.useragent.override", f"{agent_rotation}")
    ff_options = webdriver.FirefoxOptions()
    ff_options.add_argument('-window-size=1980,1080')
    ff_options.add_argument('-headless')
    driver = webdriver.Firefox(executable_path=os.path.join(webdriver_path, 'geckodriver_0_28'),
                               firefox_profile=profile, options=ff_options)
    # driver.install_addon(os.path.join(WEBDRIVER, 'adblock_plus-3.10-an+fx.xpi'), temporary=True)
    p = str(pathlib.Path('adblock_for_firefox-4.24.1-fx.xpi').parent.absolute()) + \
        '/webdriver/adblock_for_firefox-4.24.1-fx.xpi'
    driver.install_addon(str(os.path.abspath(p)), temporary=True)
    driver.maximize_window()
    sleep(1)
    print(driver.execute_script("return navigator.userAgent"))
    return driver


def agents():
    ua = [
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

    ]
    return choice(ua)


def chrome_init(webdriver_path, agent_rotation):
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
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--incognito")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument(f'user-agent={agent_rotation}')
    chrome_options.add_argument("--enable-javascript")
    chrome_options.add_argument("--no-sandbox")
    config = '/home/upsilonsfather/.config/google-chrome/'
    chrome_options.add_argument(f"user-data-dir=f{config}")
    z = os.path.pardir
    p = str(pathlib.Path(f'{z}').parent.parent.absolute())
    x = str(os.path.abspath(p))
    print(p)
    print(x)
    driver_path = os.path.join(webdriver_path, 'chromedriver_87')
    driver = webdriver.Chrome(driver_path, options=chrome_options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": f'{agent_rotation}'})
    print(driver.execute_script("return navigator.userAgent"))
    print('Chrome has been started')
    sleep(1)
    return driver

#
# def response(flow):
#     with open('injected-test-bypasses.js', 'r') as f:
#         content_js = f.read()
#         if flow.response.headers['Content-Type'] != 'text/html':
#             return
#         if not flow.response.status_code == 200:
#             return
#
#         html = BeautifulSoup(flow.response.text, 'lxml')
#         container = html.head or html.body
#         if container:
#             script = html.new_tag('script', type='text/javascript')
#             script.string = content_js
#             container.insert(0, script)
#             flow.response.text = str(html)
#             ctx.log.info('Successfully injected the content.js script.')

#
# import os
# from seleniumwire import webdriver
# from gzip import compress, decompress
# from urllib.parse import urlparse
#
# from lxml import html
# from lxml.etree import ParserError
# from lxml.html import builder
#
# script_elem_to_inject = builder.SCRIPT('alert("injected-test-bypasses")')
#
# def inject(req, req_body, res, res_body):
#     # various checks to make sure we're only injecting the script on appropriate responses
#     # we check that the content type is HTML, that the status code is 200, and that the encoding is gzip
#     if res.headers.get_content_subtype() != 'html' or res.status != 200 or res.getheader('Content-Encoding') != 'gzip':
#         return None
#     try:
#         parsed_html = html.fromstring(decompress(res_body))
#     except ParserError:
#         return None
#     try:
#         parsed_html.head.insert(0, script_elem_to_inject)
#     except IndexError: # no head element
#         return None
#     # injected.append((req, req_body, res, res_body, parsed_html))
#     return compress(html.tostring(parsed_html))
#
# drv = webdriver.Chrome(seleniumwire_options={'custom_response_handler': inject})
# drv.header_overrides = {'Accept-Encoding': 'gzip'} # ensure we only get gzip encoded responses