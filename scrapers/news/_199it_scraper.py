# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
now = datetime.now()
from common import htmltopdf

errorChars = [' ', '|','丨','\\','/','“','"','」','「',':']


def urlParser(search, path, sum):

    url = "http://search.199it.com:8001/?word="+search+"&page=1"

    res = requests.get(url)
    sum.write("搜索内容：" + search + "\n")
    sum.write("date: "+ datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n" )
    sum.write("\n")
    print(url)

    if(len(res.json()) > 1):
        resp = res.json()
        pages = resp[0]
        count = 0
        articles = []
        for i in range(1, len(resp)):
            if(count == 0):
                articles.append(resp[i])
            if(count == 2):
                count = 0
            else:
                count+=1
        i = 1
        for obj in articles:
            sum.write(str(i)+"\n")
            url = str(obj)
            id = findId(url)
            textScrape(url, path, sum, id)
            i+=1
    sum.close()

def textScrape(url, path, sum, id):
    url = url
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')

    title = soup.find('h1', {"class": "entry-title"}).getText()
    title = nameCleaner(title, errorChars)
    date = soup.find('time', {"class": "entry-date"}).getText()
    soup.find('div', {"id": "wp_rp_first"}).decompose()
    for s in soup(['script', 'style']):
        s.decompose()
    article = soup.find('div', {"class": "entry-content articlebody"})

    htmltopdf(article,path,title,date,sum,id)



def findId(inp):
    left = 0
    right = 0
    for i in range(15,len(inp)):
        if(inp[i].isdigit()):
            left = i
            break
    for i in range(len(inp),0,-1):
        if(inp[i-1].isdigit()):
            right = i
            break
    return inp[left:right]
def nameCleaner(string, chars):
    for elem in chars :
        if elem in string :
            string = string.replace(elem, '')
    return  string



def main():
    search = input("Please enter your search:")
    path = "199it/reports/" + search + "/"
    if not os.path.exists(path):
        os.makedirs(path)
    if os.path.exists(path+"summary.txt"):
        sum = open(path+"summary"+".txt", "a", encoding='utf-8')
    else:
        sum = open(path+"summary"+".txt", "w", encoding='utf-8')
    urlParser(search, path, sum)


main()
