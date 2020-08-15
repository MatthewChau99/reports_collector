import pdfkit
import requests
from bs4 import BeautifulSoup


def textScrape():
    url = 'https://36kr.com/p/834726945746304'
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')

    title = soup.find('h1').getText()
    fileTitle = title
    fileTitle = fileTitle.replace('|', '')
    date = soup.find('span', {"class": "title-icon-item item-time"}).getText()[3:]
    print(date)
    article = soup.find('div', {"class": "article-content"})
    with open("output1.html", "w", encoding='utf-8') as file:
        file.write(str(article))

    options = {
     'page-size': 'Letter',
     'margin-top': '0.75in',
     'margin-right': '0.75in',
     'margin-bottom': '0.75in',
     'margin-left': '0.75in',
     'encoding': "UTF-8",
     'no-outline': None
     }
    pdfkit.from_file("output1.html",'out.pdf', options = options)


textScrape()
