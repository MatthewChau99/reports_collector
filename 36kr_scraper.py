import requests
from fpdf import FPDF
from bs4 import BeautifulSoup

url = 'https://36kr.com/p/1724365176833'
res = requests.get(url)
html_page = res.content
soup = BeautifulSoup(html_page, 'html.parser')
title = soup.find('h1').getText()
date = soup.find('span', {"class": "title-icon-item item-time"}).getText()[3:]
article = soup.find('div', {"class": "common-width content articleDetailContent kr-rich-text-wrapper"})
text = article.find_all("p")

f = open(title+".txt", "w", encoding='utf-8')
f.write("Title: " + title + "\n")
f.write("Date: "  + date + "\n")
for t in text:
    f.write(t.getText() + '\n')


f.close()
