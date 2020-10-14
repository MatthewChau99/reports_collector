import os
import requests
from lxml import etree
import json
import config
import public_fun


def handle(search_word, page, s_date):
    '''
    获取搜索结果中的文章url
    :param search_word: 搜素关键词
    :param page: 页数
    :return:
    '''
    url = 'https://www.analysys.cn/es/eaapi?keyword={}&page={}'.format(search_word, page)
    index_url2 = 'https://www.analysys.cn/article/detail/{}'
    res = requests.get(url=url, headers=config.HEADERS)
    data = json.loads(res.text)
    result = []
    if data['list']:
        pages = page + 1 if data["list"] else 0
        for d in data['list']:
            e_date = d['publishDate']
            if public_fun.calc_date(s_date=s_date, e_date=e_date):
                result.append(index_url2.format(d['id']))
        return result, pages
    else:
        print('url1 404错误:', res.status_code, url)
        return [], 0


def get_data(url, search_word, max_text):
    json_result = {'source': 'yg', 'doc_id': '', 'date': '', 'download_url': '',
                   'org_name': '', 'page_num': '1', 'doc_type': 'NEW', 'title': ''}
    path = os.path.join(config.SAVE_PATH, search_word, 'news', 'analysys')
    res = requests.get(url=url, headers=config.HEADERS)
    html = etree.HTML(res.text)
    content_text = public_fun.filter_space_json(html.xpath('//*[@class="detail-left col-md-9"]//text()'))
    if len(content_text) > max_text:
        try:
            doc_id = url.split('/')[-1]  # 文章ID
            title = html.xpath('//*[@class="container"]/h1')[0]  # 文章标题
            description = html.xpath('//*[@class="detail-left col-md-9"]')[0]  # 文章内容
            html_list = [title, description]
            html_result = public_fun.filter_space_html(html_list)
            json_result['doc_id'] = doc_id
            json_result['date'] = public_fun.filter_space_json(html.xpath('//*[@class="head-other"]/span[3]/text()')[-1])
            json_result['download_url'] = url
            try:
                json_result['org_name'] = public_fun.filter_space_json(
                    html.xpath('//*[@class="head-other"]/span/text()')[2])
            except:
                json_result['org_name'] = ''
            json_result['title'] = public_fun.filter_space_json(html.xpath('//*[@class="container"]/h1/text()')[0])
            public_fun.write_down_json(path=path, filename=doc_id + '.json', text=json_result)
            public_fun.write_down_html(path=path, filename=doc_id + '.html', text=html_result)
        except Exception as e:
            print(e.__traceback__.tb_lineno, url, e)
    else:
        print('文章字数不足', max_text)


def main(search_word, max_art, max_text, s_date):
    '''
    铅笔道爬虫入口函数
    :param search_word:搜索关键词
    :return: None
    '''
    s_date = public_fun.reduce_date(s_date)
    page = 1
    url2_list = []
    while page:
        one_page_url, pages = handle(search_word=search_word, page=page, s_date=s_date)
        url2_list += one_page_url
        if len(url2_list) < max_art and page < int(pages):
            page += 1
        else:
            page = 0
    url2_list = url2_list[:5] if config.DEBUG else url2_list
    for url2 in url2_list:
        get_data(url=url2, search_word=search_word, max_text=max_text)


if __name__ == '__main__':
    p0 = '人工智能'
    p1 = 10
    p2 = 200
    p3 = '2'
    r2 = main(search_word=p0, max_art=p1, max_text=p2, s_date=p3)
