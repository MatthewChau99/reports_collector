from selenium import webdriver
import requests
from lxml import etree
import os
import config
import public_fun
from definitions import ROOT_DIR, CHROME_DRIVER_PATH


def creat_driver(url):
    chrome_opt = webdriver.ChromeOptions()
    chrome_opt.add_argument('--headless')
    driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=chrome_opt)
    driver.get(url)
    return driver


def get_url2(driver):
    one_page_url = []
    labels = driver.find_elements_by_xpath('//*[@class="news-item"]/h3/a')
    for l in labels:
        one_page_url.append(l.get_attribute('href'))

    lis = driver.find_elements_by_xpath('//*[@class="page-group"]//li')
    for l in lis:
        if '下一页' in l.text:
            l.click()
            return one_page_url, True
    return one_page_url, False


def get_data(url, search_word, s_date, max_text):
    s_date = s_date
    json_result = {'source': 'dfcfw', 'doc_id': '', 'date': '', 'download_url': '',
                   'org_name': '', 'page_num': '', 'doc_type': 'NEWS', 'title': ''}
    path = os.path.join(ROOT_DIR, 'cache', search_word, 'news', 'eastmoney')  # 路径
    res = requests.get(url=url, headers=config.HEADERS)
    res.encoding = res.apparent_encoding
    html = etree.HTML(res.text)
    content_text = public_fun.filter_space_json(html.xpath('//*[@id="ContentBody"]//text()'))  # 正文内容

    if len(content_text) > max_text:
        try:
            # ==============================html=========================
            # doc_id = re.findall('\d+', string=url)[0]  # 文章ID
            doc_id = url.split('/')[-1].split('.')[0]  # 文章ID
            title = html.xpath('//*[@class="newsContent"]')[0]  # 标题
            description = html.xpath('//*[@id="ContentBody"]')[0]  # 文章内容 html
            html_list = [title, description]
            html_result = public_fun.filter_space_html(html_list)
            # ==============================json=========================
            json_result['doc_id'] = doc_id
            json_result['date'] = public_fun.filter_space_json(
                html.xpath('//*[@class="time"]/text()')[0].replace('-', ''))[:10] \
                .replace('年', '-').replace('月', '-')
            json_result['download_url'] = url
            json_result['org_name'] = public_fun.filter_space_json(
                html.xpath('//*[@class="source data-source"]/@data-source'))
            json_result['title'] = public_fun.filter_space_json(html.xpath('//*[@class="newsContent"]/h1/text()'))
            public_fun.write_down_json(path=path, filename=doc_id + '.json', text=json_result)
            public_fun.write_down_html(path=path, filename=doc_id + '.html', text=html_result)
        except Exception as e:
            print(e.__traceback__.tb_lineno, url, e)
    else:
        print('文章字数不足', max_text, url)


def main(search_word, s_date, max_atr, max_text):
    s_date = public_fun.reduce_date(s_date)
    url = 'http://so.eastmoney.com/news/s?keyword={}'.format(search_word)
    url2_list = []
    driver = creat_driver(url)
    n = True
    while n and len(url2_list) < max_atr:
        one_page_url, n = get_url2(driver)
        url2_list += one_page_url
    url2_list = url2_list[:5] if config.DEBUG else url2_list
    [get_data(url=r, search_word=search_word, max_text=max_text, s_date=s_date) for r in url2_list]


if __name__ == '__main__':
    p1 = '人工智能'  # 搜索关键词
    p2 = '4'  # 最早时间
    p3 = 10  # 文章数
    p4 = 500  # 文字数量
    main(search_word=p1, s_date=p2, max_atr=p3, max_text=p4)
