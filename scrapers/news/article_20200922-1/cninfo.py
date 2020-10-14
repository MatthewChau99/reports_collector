import os
import time

import requests
from lxml import etree
import json
import config
import public_fun


def handle(search_word, page, s_date):
    url = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
    index_down_url = 'http://www.cninfo.com.cn/new/announcement/download?bulletinId={}&announceTime={}'
    json_result = {'source': 'jzcx', 'doc_id': '', 'date': '', 'download_url': '',
                   'org_name': '', 'page_num': '1', 'doc_type': 'NEW', 'title': ''}
    path = os.path.join(config.SAVE_PATH, search_word, 'news', 'cninfo')
    form_data = {
        'pageNum': page,
        'pageSize': '30',
        'column': 'szse',
        'tabName': 'fulltext',
        'searchkey': search_word,
        'isHLtitle': 'true'
    }
    res = requests.post(url=url, headers=config.HEADERS, data=form_data)
    res.encoding = res.apparent_encoding
    data = json.loads(res.text)
    if data['announcements']:
        pages = page + 1 if data['totalAnnouncement'] > page*30 else 0
        for d in data['announcements']:
            e_date =d['announcementTime']
            if public_fun.calc_date(s_date=s_date, e_date=e_date):
                # http://www.cninfo.com.cn/new/announcement/download?bulletinId=1208504509&announceTime=2020-9-29
                json_result['doc_id'] = d['announcementId']
                timeArray = time.localtime(e_date/1000)
                otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
                json_result['date'] = otherStyleTime
                json_result['download_url'] = index_down_url.format(d['announcementId'], otherStyleTime)
                json_result['org_name'] = d['secName']
                json_result['title'] = d['announcementTitle']
                public_fun.write_down_json(path=path, filename=json_result['doc_id']+'.json', text=json_result)
        return pages
    else:
        print('url1 404错误:', res.status_code, url)
        return [], 0


# def get_data(url, search_word, max_text):
#     json_result = {'source': 'blzk', 'doc_id': '', 'date': '', 'download_url': '',
#                    'org_name': '', 'page_num': '1', 'doc_type': 'NEW', 'title': ''}
#     path = os.path.join(config.SAVE_PATH, search_word, 'news', 'bailuzhiku')
#     res = requests.get(url=url, headers=config.HEADERS)
#     html = etree.HTML(res.text)
#     content_text = public_fun.filter_space_json(html.xpath('//*[@class="textarea-box policy-textarea"]//text()'))
#     if len(content_text) > max_text:
#         try:
#             doc_id = url.split('/')[-1].replace('.html', '')  # 文章ID
#             title = html.xpath('//*[@class="policy-wrap-title"]/h1')[0]  # 文章标题
#             description = html.xpath('//*[@class="textarea-box policy-textarea"]')[0]  # 文章内容
#             html_list = [title, description]
#             html_result = public_fun.filter_space_html(html_list)
#             json_result['doc_id'] = doc_id
#             json_result['date'] = public_fun.filter_space_json(
#                 html.xpath('//*[@class="attribute-table"]/tbody/tr[2]/td[1]/div/text()')[0])
#             json_result['download_url'] = 'http://www.bailuzhiku.com/' + \
#                                           html.xpath('//*[@class="header-tool-link download"]/@href')[0]
#             try:
#                 json_result['org_name'] = public_fun.filter_space_json(
#                     html.xpath('//*[@class="attribute-table"]/tbody/tr[1]/td[1]/div/text()')[0])
#             except:
#                 json_result['org_name'] = ''
#             json_result['title'] = public_fun.filter_space_json(html.xpath('//h1[@class="title"]/text()')[0])
#             public_fun.write_down_json(path=path, filename=doc_id + '.json', text=json_result)
#             public_fun.write_down_html(path=path, filename=doc_id + '.html', text=html_result)
#         except Exception as e:
#             print(e.__traceback__.tb_lineno, url, e)
#     else:
#         print('文章字数不足', max_text)


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
        pages = handle(search_word=search_word, page=page, s_date=s_date)
        if len(url2_list) < max_art and page < int(2):
            page += 1
        else:
            page = 0
    # return url2_list
    # url2_list = url2_list[:5] if config.DEBUG else url2_list
    # for url2 in url2_list:
    #     get_data(url=url2, search_word=search_word, max_text=max_text)


if __name__ == '__main__':
    p0 = '人工智能'
    p1 = 10
    p2 = 500
    p3 = '2'
    r2 = main(search_word=p0, max_art=p1, max_text=p2, s_date=p3)
