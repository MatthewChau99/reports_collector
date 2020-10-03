# -*- coding: utf-8 -*-
import json
import os
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from definitions import ROOT_DIR
from utils import bwlist
from utils.errors import NoDocError

now = datetime.now()


def urlParser(search_keyword, path, summary, num_years, get_pdf: bool):
    url = "https://36kr.com/search/articles/" + search_keyword + "?sort=score"

    res = requests.get(url)  # init page
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    articles = soup.find('ul',
                         {"class": "kr-search-result-list-main clearfloat"})  # find class that contains search results

    if not articles:
        raise NoDocError('No documents found')

    articles_count = 0

    summary.update({'source': '36kr'})
    summary.update({'source_type': 'news'})
    summary.update({'search_keyword': search_keyword})
    summary.update({'search_time': str(datetime.now())})
    summary.update({'data': {}})

    for a in articles.find_all('a', {"class": "article-item-title weight-bold"},
                               href=True):  # find all a links with href within class
        valid, summary = textScrape(search_keyword, "https://36kr.com" + a['href'], path, summary, num_years, get_pdf)
        if valid:
            articles_count += 1

    if summary['data']:
        summary_save_path = os.path.join(path, 'summary.json')
        with open(summary_save_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=4)

    print('--------Finished downloading %d articles from 36kr--------' % articles_count)


def prefilter(date, num_years, search_keyword, doc_id):
    ret = True

    # Date processing
    dateToday = datetime.now().strftime("%Y")
    if date[0:3].isnumeric():
        years = int(dateToday) - int(date[0:4])
        if years > num_years:
            ret = False

    # Blacklist processing
    bl = bwlist.BWList(search_keyword, 'black')
    blacklist_exist = bl.bwlist_exist()
    wh = bwlist.BWList(search_keyword, 'white')
    whitelist_exist = wh.bwlist_exist()

    if blacklist_exist and bl.in_bwlist(doc_id, '36kr') or whitelist_exist and wh.in_bwlist(doc_id, '36kr'):
        ret = False

    return ret


def textScrape(search_keyword, url, path, summary, num_years, get_pdf: bool):
    url = url
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')

    pattern = re.compile(r"(?<=\"articleDetailData\":{\"code\":0,\"data\":{\"itemId\":)[0-9]*")
    doc_id = re.search(pattern, soup.text).group(0)

    pattern = re.compile(r"(?<=\"author\":\")(.*)(?=\",\"authorId)")
    author = re.search(pattern, soup.text).group(0)

    title = soup.find('h1').getText()
    title = title.replace('|', '')
    date = soup.find('span', {"class": "title-icon-item item-time"}).getText()[3:]
    article = soup.find('div', {"class": "article-content"})

    valid = prefilter(date, num_years, search_keyword, doc_id)

    if valid:
        print('Processing article %s' % doc_id)
        json_save_path = os.path.join(path, str(doc_id) + '.json')
        html_save_path = os.path.join(path, str(doc_id) + '.html')
        pdf_save_path = os.path.join(path, str(doc_id) + '.pdf')

        if get_pdf:
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

        if 'data' not in summary.keys():
            summary.update({'data': {}})
        else:
            summary['data'].update({doc_id: pdf_save_path})

        with open(json_save_path, 'w', encoding='utf-8') as f:
            json.dump(doc_info, f, ensure_ascii=False, indent=4)

    return valid, summary


def run(search_keyword, num_years, get_pdf: bool):
    print('--------Begin searching articles from 36kr--------')

    try:
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
            sum = open(os.path.join(current_path, "summary" + ".json"), "a", encoding='utf-8')
        else:
            sum = open(os.path.join(current_path, "summary" + ".json"), "w", encoding='utf-8')

        summary = {}
        urlParser(search_keyword, current_path, summary, num_years, get_pdf)

    except NoDocError:
        print('--------No documents found in 36kr--------')
        pass


if __name__ == '__main__':
    run(search_keyword='可口可乐', num_years=1)
