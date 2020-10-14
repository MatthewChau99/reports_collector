import os
import requests
from lxml import etree
import pandas as pd
import re
import json
from selenium import webdriver
import time
import datetime


#%%

import config
import public_fun
def handle(search_word, page, s_date):
    path = os.path.join(config.SAVE_PATH, search_word, 'news', 'askci')
    url = 'https://wk.askci.com/ListTable/GetList?keyword={}&bookName=&tradeId=&typeId=&tagName=&publisher=&page={}&limit=100'.format(search_word, page)
    res = requests.post(url=url, headers=config.HEADERS)
    res.encoding = res.apparent_encoding
    data = json.loads(res.text)['data'][:5] if config.DEBUG else json.loads(res.text)['data']
    if data:
        for d in data:
            e_date = d['StrBookPublishDate']
            if public_fun.calc_date(s_date=s_date, e_date=e_date):
                json_result = {'source': 'askci', 'doc_id': '', 'date': '', 'download_url': '',
                               'org_name': '', 'page_num': '1', 'doc_type': 'NEW', 'title': ''}
                doc_id = d['DownloadUrl'].split('/')[-2].replace('/', '')
                json_result['doc_id'] = doc_id
                json_result['date'] = e_date
                json_result['download_url'] = d['DownloadUrl']
                json_result['org_name'] = d['BookPublisher']
                json_result['title'] = d['BookName']
                public_fun.write_down_json(path=path, filename=doc_id + '.json', text=json_result)
    else:
        print('url1 404错误:', res.status_code, url)


def main(search_word, s_date, max_art, max_text):
    s_date = public_fun.reduce_date(s_date)
    page = 1
    handle(search_word=search_word, page=page, s_date=s_date)



if __name__ == '__main__':
    p1 = '人工智能'
    p2 = '2'
    p3 = 10
    p4 = 500
    r2 = main(search_word=p1, s_date=p2, max_art=p3, max_text=p4)

