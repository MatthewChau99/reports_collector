# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

import pdfkit
import shutil

now = datetime.now()


def urlParser(search, path, sum):
    url = "https://36kr.com/search/articles/" + search + "?sort=score"

    res = requests.get(url)  # init page
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    articles = soup.find('ul',
                         {"class": "kr-search-result-list-main clearfloat"})  # find class that contains search results

    sum.write("搜索内容：" + search + "\n")
    sum.write("date: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
    sum.write("\n")

    for a in articles.find_all('a', {"class": "article-item-title weight-bold"},
                               href=True):  # find all a links with href within class
        url = "https://36kr.com" + a['href']
        textScrape("https://36kr.com" + a['href'], path, sum)
    sum.close()


def prefilter(date):
    ret = True
    dateToday = datetime.now().strftime("%Y")
    years = int(dateToday) - int(date[0:4])
    if date[0] == '2' and years > 2:
        ret = False
    return ret


def textScrape(url, path, sum):
    url = url
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')

    title = soup.find('h1').getText()
    title = title.replace('|', '')
    date = soup.find('span', {"class": "title-icon-item item-time"}).getText()[3:]
    article = soup.find('div', {"class": "article-content"})
    if prefilter(date):
        with open("temp.html", "w", encoding='utf-8') as file:
            file.write(str(article))
        file.close()

        folderTitle = title.replace(' ', '_')
        folderPath = path + folderTitle + "/"
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
            options = {
                'quiet': '',
                'page-size': 'Letter',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'no-outline': None
            }
            pdfkit.from_file("temp.html", 'article.pdf', options=options)
            shutil.move("article.pdf", folderPath)

            sum.write(title + "\n")
            sum.write(date + "\n")
            sum.write(folderPath + "\n")
            sum.write("\n")


def main():
    search = input("Please enter your search:")
    path = "36kr/" + search + "/"
    if not os.path.exists(path):
        os.makedirs(path)
    if os.path.exists(path + "summary.txt"):
        sum = open(path + "summary" + ".txt", "a", encoding='utf-8')
    else:
        sum = open(path + "summary" + ".txt", "w", encoding='utf-8')
    urlParser(search, path, sum)


if __name__ == '__main__':
    main()
