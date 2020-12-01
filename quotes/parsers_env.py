import os
import pathlib
from time import sleep
from random import choice
from selenium import webdriver
from PIL import Image, ImageFilter


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
    # driver.set_window_size(1600, 1200)
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


def crop(img_path, img_path_save, a, b, c, d):
    # 56 pixels from the left
    # 44 pixels from the top
    # 320 pixels from the right
    # 43 pixels from the bottom
    img = Image.open(img_path)
    img = img.filter(ImageFilter.DETAIL)
    width, height = img.size
    print(width, height)
    cropped = img.crop((a, b, width - c, height - d))
    cropped.save(img_path_save, quality=100, subsampling=0)