# -*- coding: utf-8 -*-
import re
import json
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

import pdfkit
import shutil

now = datetime.now()


def urlParser(search, path, sum, num_years):
    url = "https://36kr.com/search/articles/" + search + "?sort=score"

    res = requests.get(url)  # init page
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    articles = soup.find('ul',
                         {"class": "kr-search-result-list-main clearfloat"})  # find class that contains search results
    articles_count = 0

    sum.write("搜索内容：" + search + "\n")
    sum.write("date: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
    sum.write("\n")

    for a in articles.find_all('a', {"class": "article-item-title weight-bold"},
                               href=True):  # find all a links with href within class
        url = "https://36kr.com" + a['href']
        textScrape("https://36kr.com" + a['href'], path, sum, num_years)
        articles_count += 1

    print('--------Finished downloading %d articles from 36kr--------' % articles_count)
    sum.close()


def prefilter(date, num_years):
    ret = True
    dateToday = datetime.now().strftime("%Y")
    if date[0:3].isnumeric():
        years = int(dateToday) - int(date[0:4])
        if years > num_years:
            ret = False
    return ret


def textScrape(url, path, sum, num_years):
    url = url
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')

    pattern = re.compile(r"(?<=\"articleDetailData\":{\"code\":0,\"data\":{\"itemId\":)[0-9]*")
    id = re.search(pattern, soup.text).group(0)
    print('Processing article %s' % id)

    pattern = re.compile(r"(?<=\"author\":\")(.*)(?=\",\"authorId)")
    author = re.search(pattern, soup.text).group(0)

    title = soup.find('h1').getText()
    title = title.replace('|', '')
    date = soup.find('span', {"class": "title-icon-item item-time"}).getText()[3:]
    article = soup.find('div', {"class": "article-content"})

    if prefilter(date, num_years):
        json_save_path = os.path.join(path, str(id) + '.json')
        pdf_save_path = os.path.join(path, str(id) + '.pdf')
        html_save_path = os.path.join(path, str(id) + '.html')

        with open(html_save_path, "w", encoding='utf-8') as file:
            file.write(str(article))
        # file.close()

        # Saving doc attributes
        doc_info = {
            'doc_id': id,
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
    os.chdir('/Users/admin/Desktop/资料库Startup')

    if 'news' not in os.listdir('cache'):
        os.mkdir('cache/news')
    if '36kr' not in os.listdir('cache/news'):
        os.mkdir('cache/news/36kr')
    path = 'cache/news/36kr'

    if search_keyword not in os.listdir(path):
        os.mkdir(os.path.join(path, search_keyword))
    path = os.path.join(path, search_keyword)

    if not os.path.exists(path):
        os.makedirs(path)
    if os.path.exists(path + "summary.txt"):
        sum = open(os.path.join(path, "summary" + ".txt"), "a", encoding='utf-8')
    else:
        sum = open(os.path.join(path, "summary" + ".txt"), "w", encoding='utf-8')
    urlParser(search_keyword, path, num_years)


if __name__ == '__main__':
    run(search_keyword='中芯国际', num_years=2)
