# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
now = datetime.now()
from common import htmltopdf

pagesize = 60
errorChars = [' ', '|','丨','\\','/','“','"','」','「',':']

def urlParser(search, path, sum):
    url = 'https://gateway.36kr.com/api/mis/nav/search/resultbytype'
    payload = {"partner_id":"web","timestamp":1597836514683,"param":{"searchType":"article","searchWord":search,"sort":"score","pageSize":pagesize,"pageEvent":0,"pageCallback":"eyJmaXJzdElkIjoxOCwibGFzdElkIjoxMywiZmlyc3RDcmVhdGVUaW1lIjozMDU0MiwibGFzdENyZWF0ZVRpbWUiOjM5NjI1NX0","siteId":1,"platformId":2}}
    headers = {
        'accept':'*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'content-length': '293',
        'content-type': 'application/json',
        'cookie': 'Hm_lvt_1684191ccae0314c6254306a8333d090=1596210296; Hm_lvt_713123c60a0e86982326bae1a51083e1=1596210297; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22173a58c3e5e469-02e84f5fa3b948-3323765-2073600-173a58c3e5fa9a%22%2C%22%24device_id%22%3A%22173a58c3e5e469-02e84f5fa3b948-3323765-2073600-173a58c3e5fa9a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ss_pp_id=d59787798bd08f8853d1596224723372; _td=2dab35d3-7b8a-48bc-bd03-96124935a411; acw_tc=2760827e15978348728514947ed067e1ffc7190f2e025127214afcfc370af8; Hm_lpvt_713123c60a0e86982326bae1a51083e1=1597836508; Hm_lpvt_1684191ccae0314c6254306a8333d090=1597836508',
        'origin': 'https://36kr.com',
        'referer': 'https://36kr.com/search/articles/%E4%B8%AD%E8%8A%AF%E5%9B%BD%E9%99%85?sort=score',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
    }
    res = requests.post(url, headers = headers, data = json.dumps(payload))
    sum.write("搜索内容：" + search + "\n")
    sum.write("date: "+ datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n" )
    sum.write("\n")
    if(res.json()['data']['totalNum']!=0):
        articles = res.json()['data']['itemList']
        i = 1
        for obj in articles:
            sum.write(str(i)+"\n")
            url = "https://36kr.com/p/"+str(obj['itemId'])
            textScrape(url, path, sum, obj['itemId'])
            i+=1
    sum.close()


def textScrape(url, path, sum, id):
    url = url
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')

    title = soup.find('h1').getText()
    title = nameCleaner(title, errorChars)
    date = soup.find('span', {"class": "title-icon-item item-time"}).getText()[3:]
    article = soup.find('div', {"class": "article-content"})
    htmltopdf(article,path,title,date,sum, id)

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
