from selenium import webdriver
import os
import pprint as pp


def get_cookies(url):
    CHROME_DRIVER_PATH = os.path.join('venv', 'chromedriver')
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    driver.get(url)
    cookies = driver.get_cookies()
    driver.close()
    return cookies
