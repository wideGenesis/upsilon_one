import io
import os
import undetected_chromedriver as uc
from time import sleep
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image


proxy = "81.177.167.92:3128"
chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--proxy-server=direct://")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument(f'user-agent={agent_rotation}')
chrome_options.add_argument("--enable-javascript")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--proxy-server={}'.format(proxy))
# chrome_options.add_argument("user-data-dir=/home/upsilonsfather/.config/google-chrome")
# chrome_options.add_argument('--profile-directory=Default')


# ============================== Inflows GET ================================
def get_flows(driver=None, img_out_path_='./'):
    etfs = ['VCIT', 'SPY', 'VTI', 'VEA', 'VWO', 'QQQ', 'VXX', 'TLT', 'SHY', 'LQD']
    with driver:
        driver.get('https://www.etf.com/etfanalytics/etf-fund-flows-tool')
        sleep(10)
        html = driver.page_source
        print(html)
        try:
            elem = driver.find_element_by_xpath(".//*[@id='edit-tickers']")
            print('elem 1 has been located')
        except Exception:
            return
        elem.send_keys("GLD, SPY, VTI, VEA, VWO, QQQ, VXX, TLT, SHY, LQD, VCIT")
        print('keys has been send')
        sleep(0.7)
        today = date.today()
        day7 = timedelta(days=7)
        delta = today - day7
        start_d = delta.strftime("%Y-%m-%d")
        end_d = today.strftime("%Y-%m-%d")
        elem = driver.find_element_by_xpath(".//*[@id='edit-startdate-datepicker-popup-0']")
        elem.send_keys(start_d)
        sleep(1)
        elem = driver.find_element_by_xpath(".//*[@id='edit-enddate-datepicker-popup-0']")
        elem.send_keys(end_d)
        sleep(1)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, ".//*[@id='edit-submitbutton']"))).click()
            print('Button has been clicked')
        except Exception as e1:
            print('Button click error. Try to re-run the scraper', e1)
            return
        sleep(8)
        try:
            elem = driver.find_element_by_xpath(".//*[@id='fundFlowsTitles']")
            print('elem 2-Titles has been located')
        except Exception as e2:
            print('Titles elem error. Try to re-run the scraper', e2)
            return
        webdriver.ActionChains(driver).move_to_element(elem).perform()
        driver.execute_script("return arguments[0].scrollIntoView();", elem)
        sleep(1)

        for etf in etfs:
            sleep(2)
            print(etf)
            tag = ".//*[@id=\'" + f'{etf}' + "_nf']"
            tag2 = ".//*[@id=\'container_" + f'{etf}' + "'" + "]"
            icon = driver.find_element_by_xpath(tag)  # ".//*[@id='{etf}_nf']"
            driver.execute_script("arguments[0].click();", icon)
            sleep(3)
            graph = driver.find_element_by_xpath(tag2)  # ".//*[@id='container_{etf}']"
            # driver.execute_script("return arguments[0].scrollIntoView();", graph)
            sleep(1)
            image = graph.screenshot_as_png
            image_stream = io.BytesIO(image)
            im = Image.open(image_stream)
            im.save(os.path.join(img_out_path_, f'inflows_{etf}.png'))
    print('Get Fund Flows complete' + '\n')


def browser_check(driver=None, url="", fname=""):
    with driver:
        driver.get(url)
        sleep(10)
        el = driver.find_element_by_tag_name('body')
        el.screenshot(fname)
        driver.quit()


def main():
    url = "https://proxy6.net/en/privacy"
    browser_check(driver=uc.Chrome(options=chrome_options), url=url, fname="screen.png")
    url = "https://browserleaks.com/javascript"
    browser_check(driver=uc.Chrome(options=chrome_options), url=url, fname="screen1.png")
    url = "http://ip-check.info/?lang=en"
    browser_check(driver=uc.Chrome(options=chrome_options), url=url, fname="screen2.png")
    # get_flows(driver=uc.Chrome(options=chrome_options))


if __name__ == '__main__':
    print(f"Starting scrapers {os.path.realpath(__file__)}, this may take a while")
    main()