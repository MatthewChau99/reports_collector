# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
now = datetime.now()
import pdfkit
import shutil
import json
pagesize = 60
errorChars = [' ', '|','丨','\\','/','“','"','」','「']

def urlParser(search, path, sum):

    url = "http://search.199it.com/?q="+search+"&page=1"
    print(url)
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    articles = soup.find('div', {"class": "row"})
    sum.write("搜索内容：" + search + "\n")
    sum.write("date: "+ datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n" )
    sum.write("\n")
    i = 0
    for a in soup.find_all('p', {"class": "row_url"}): #find all a links with href within class
        print(1)
        url = a
        print(url)
        # textScrape(url, path, sum, url[17:-5])
    sum.close()

def textScrape(url, path, sum, id):
    url = url
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    title = soup.find('h1').getText()
    title = nameCleaner(title, errorChars)
    date = soup.find('span', {"class": "title-icon-item item-time"}).getText()[3:]
    article = soup.find('div', {"class": "article-content"})
    htmltopdf(path,title,date,sum,id)

def nameCleaner(string, chars):
    for elem in chars :
        if elem in string :
            string = string.replace(elem, '')
    return  string

def main():
    search = input("Please enter your search:")
    path = "36kr/reports/"+ search + "/"
    if not os.path.exists(path):
        os.makedirs(path)
    if os.path.exists(path+"summary.txt"):
        sum = open(path+"summary"+".txt", "a", encoding='utf-8')
    else:
        sum = open(path+"summary"+".txt", "w", encoding='utf-8')
    urlParser(search, path, sum)


main()
