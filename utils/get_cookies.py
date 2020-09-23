from selenium import webdriver
import os
from definitions import ROOT_DIR
import pprint as pp


def get_cookies(url):
    CHROME_DRIVER_PATH = os.path.join(ROOT_DIR, 'venv', 'chromedriver')
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    driver.get(url)
    cookies = driver.get_cookies()
    driver.close()
    return cookies
