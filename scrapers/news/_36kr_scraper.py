# -*- coding: utf-8 -*-
import json
import os
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from definitions import ROOT_DIR
from utils import blacklist

now = datetime.now()


def urlParser(search_keyword, path, sum, num_years):
    url = "https://36kr.com/search/articles/" + search_keyword + "?sort=score"

    res = requests.get(url)  # init page
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    articles = soup.find('ul',
                         {"class": "kr-search-result-list-main clearfloat"})  # find class that contains search results
    articles_count = 0

    sum.write("搜索内容：" + search_keyword + "\n")
    sum.write("date: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
    sum.write("\n")

    for a in articles.find_all('a', {"class": "article-item-title weight-bold"},
                               href=True):  # find all a links with href within class
        textScrape(search_keyword, "https://36kr.com" + a['href'], path, sum, num_years)
        articles_count += 1

    print('--------Finished downloading %d articles from 36kr--------' % articles_count)
    sum.close()


def prefilter(date, num_years, search_keyword):
    ret = True

    # Date Filter
    dateToday = datetime.now().strftime("%Y")
    if date[0:3].isnumeric():
        years = int(dateToday) - int(date[0:4])
        if years > num_years:
            ret = False

    # Blacklist Filter
    bl = blacklist.Blacklist(search_keyword)
    blacklist_exist = bl.blacklist_exist()
    if blacklist_exist and bl.in_blacklist(search_keyword, '36kr'):
        ret = False

    return ret


def textScrape(search_keyword, url, path, sum, num_years):
    url = url
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')

    pattern = re.compile(r"(?<=\"articleDetailData\":{\"code\":0,\"data\":{\"itemId\":)[0-9]*")
    doc_id = re.search(pattern, soup.text).group(0)
    print('Processing article %s' % doc_id)

    pattern = re.compile(r"(?<=\"author\":\")(.*)(?=\",\"authorId)")
    author = re.search(pattern, soup.text).group(0)

    title = soup.find('h1').getText()
    title = title.replace('|', '')
    date = soup.find('span', {"class": "title-icon-item item-time"}).getText()[3:]
    article = soup.find('div', {"class": "article-content"})

    if prefilter(date, num_years, search_keyword):
        json_save_path = os.path.join(path, str(doc_id) + '.json')
        html_save_path = os.path.join(path, str(doc_id) + '.html')

        with open(html_save_path, "w", encoding='utf-8') as file:
            file.write(str(article))

        # Saving doc attributes
        doc_info = {
            'source': '36kr',
            'doc_id': doc_id,
            'title': title,
            'date': date,
            'org_name': author,
            'doc_type': 'NEWS'
        }

        with open(json_save_path, 'w', encoding='utf-8') as f:
            json.dump(doc_info, f, ensure_ascii=False, indent=4)

        # shutil.move("article.pdf", folderPath)

        sum.write(title + "\n")
        sum.write(date + "\n")
        # sum.write(folderPath + "\n")
        sum.write("\n")


def run(search_keyword, num_years):
    # search = input("Please enter your search:")
    print('--------Begin searching articles from 36kr--------')

    os.chdir(ROOT_DIR)
    keyword_dir = os.path.join('cache', search_keyword)

    if search_keyword not in os.listdir('cache'):
        os.mkdir(keyword_dir)

    if 'news' not in os.listdir(keyword_dir):
        os.mkdir(os.path.join(keyword_dir, 'news'))

    if '36kr' not in os.listdir(os.path.join(keyword_dir, 'news')):
        os.mkdir(os.path.join(keyword_dir, 'news', '36kr'))

    current_path = os.path.join(keyword_dir, 'news', '36kr')

    if os.path.exists(current_path + "summary.txt"):
        sum = open(os.path.join(current_path, "summary" + ".txt"), "a", encoding='utf-8')
    else:
        sum = open(os.path.join(current_path, "summary" + ".txt"), "w", encoding='utf-8')
    urlParser(search_keyword, current_path, sum, num_years)


if __name__ == '__main__':
    run(search_keyword='中芯国际', num_years=2)
