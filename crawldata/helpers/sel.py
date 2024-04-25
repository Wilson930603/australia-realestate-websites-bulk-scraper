import logging
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
logger.setLevel(logging.WARNING)


class SeleniumSpider():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--log-level=3")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1200x600')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(options=options)
        self.base_wait_time = 5

    def get(self, url):
        self.driver.get(url)

    def get_page_source(self):
        return self.driver.page_source

    def wait(self, seconds):
        sleep(seconds)

    def locate_element(self, path):
        try:
            return self.driver.find_element(By.XPATH, path)
        except NoSuchElementException:
            return None

    def click_element(self, el):
        el.click()

    def quit(self):
        self.driver.close()
        self.driver.quit()
