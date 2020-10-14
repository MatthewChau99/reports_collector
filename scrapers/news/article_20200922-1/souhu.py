from selenium import webdriver
import requests
from lxml import etree
import time
import re
import os
from selenium.webdriver.support.wait import WebDriverWait
import config
import public_fun


class SouHu:
    def __init__(self, search_word, s_date, max_art, max_text=3000):
        url = 'https://search.sohu.com/?keyword={}'.format(search_word)
        chrome_opt = webdriver.ChromeOptions()
        chrome_opt.add_argument('--headless')
        self.s_date = public_fun.reduce_date(reduction=s_date)
        self.max_art = max_art
        self.max_text = max_text
        self.path = os.path.join(config.SAVE_PATH, search_word, 'news', 'souhu')
        self.driver = webdriver.Chrome()
        self.driver.get(url=url)
        self.main()
        self.driver.close()

    def get_url_list(self):
        key = True
        count = 1
        while key and count < int(self.max_art / 10):
            self.driver.execute_script("window.scrollBy(0,3000)")
            time.sleep(1)
            try:
                self.driver.find_element_by_xpath('//*[@id="no-more"]')
                key = False
            except:
                key = True
            count += 1
        labels = self.driver.find_elements_by_xpath('//*[@class="cards-content-title"]/a')
        labels2 = self.driver.find_elements_by_xpath('//*[@class="cards-content-right-comm"]')
        s_data = public_fun.reduce_date(reduction=p2)
        href = [l.get_attribute('href') for l in labels]
        dates = [l2.text.split()[-1] for l2 in labels2 if l2.text]
        _list = [href[n] for n in range(len(href)) if public_fun.calc_date(s_date=s_data, e_date=dates[n])]
        return _list

    def get_content(self, url):
        self.driver.get(url)
        time.sleep(1)
        doc_id = url.split('/')[4]  # 取后十个英文
        text = ''.join(self.driver.find_element_by_xpath('//*[@class="text"]').text.split())
        if len(text) > self.max_text:
            # ===========================html==========================
            content = self.driver.find_element_by_xpath('//*[@class="text"]').get_attribute('outerHTML')
            html = [content]
            # ===========================json==========================
            json_result = {'source': 'souhu', 'doc_id': '', 'date': '', 'download_url': url, 'org_name': '',
                           'page_num': '1', 'doc_type': 'NEW', 'title': ''}
            json_result['doc_id'] = doc_id
            try:
                json_result['date'] = ''.join(
                    self.driver.find_element_by_xpath('//*[@class="time"]').text.split()[0])
                try:
                    json_result['org_name'] = ''.join(
                        self.driver.find_element_by_xpath('//*[@class="user-info"]/h4').text.split()[-1])
                except:
                    json_result['org_name'] = ''
                json_result['title'] = ''.join(
                    self.driver.find_element_by_xpath('//*[@class="text-title"]/h1').text.split())
            except:
                pass
            public_fun.write_down_html(path=self.path, filename=doc_id[:9] + '.html', text=html)
            public_fun.write_down_json(path=self.path, filename=doc_id[:9] + '.json', text=json_result)
        else:
            print(url)
            print('文章字数不足', self.max_text)

    def main(self):
        self.url2_list = self.get_url_list()
        self.url2_list = self.url2_list[:5] if config.DEBUG else self.url2_list
        for url in self.url2_list:
            self.get_content(url=url)

if __name__ == '__main__':
    p1 = '人工智能'  # 搜索关键词
    p2 = '5'  # 最早时间
    p3 = 100  # 文章数
    p4 = 500  # 文字数量
    sougou = SouHu(search_word=p1, s_date=p2, max_art=p3, max_text=p4)
