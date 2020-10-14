import os
import time

from selenium import webdriver

import config
import public_fun
from definitions import ROOT_DIR, CHROME_DRIVER_PATH


def creat_driver(search_word):
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    index_url = 'https://kns.cnki.net/kns8/defaultresult/index'
    driver.get(url=index_url)
    driver.find_element_by_xpath('//*[@id="txt_search"]').send_keys(search_word)
    driver.find_element_by_xpath('//*[@class="search-btn"]').click()
    return driver


def get_url_list(driver, s_date, max_art, max_text=3000):
    count = 1
    path = os.path.join(ROOT_DIR, 'cache', search_word, 'news', 'zhiwang')
    while count < int(max_art / 20):
        time.sleep(10)
        labels = driver.find_element_by_xpath('//*[@class="result-table-list"]/tbody')
        for l in labels:
            e_date = l.find_element_by_xpath('./td[@class="date"]').text.replace(' ', '')
            if public_fun.calc_date(s_date=s_date, e_date=e_date):
                doc_id = l.find_element_by_xpath('./td[@class="name"]').get_attribute('href')
                json_result = {'source': 'zhilian', 'doc_id': '', 'date': '', 'download_url': '', 'org_name': '',
                               'page_num': '', 'doc_type': 'NEWS', 'title': ''}
                json_result['doc_id'] = doc_id
                json_result['download_url'] = 'https://' + doc_id
                json_result['org_name'] = l.find_element_by_xpath('./td[@class="author"]').text
                json_result['title'] = l.find_element_by_xpath('./td[@class="name"]').text
                public_fun.write_down_json(path=path, filename=doc_id[-10:] + '.json', text=json_result)
        try:
            driver.find_element_by_xpath('//*[@id="PageNext"]').click()
            count += 1
        except:
            count = 999


if __name__ == '__main__':
    search_word = '人工智能'
    s_date = 6
    max_art = 40
    driver = creat_driver(search_word=search_word)
    get_url_list(driver=driver, s_date=s_date, max_art=max_art)
