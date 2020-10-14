import os
import requests
from lxml import etree
import config
import public_fun


def handle(url, s_date):
    res = requests.get(url=url, headers=config.HEADERS)
    if res.status_code != 404:
        res.encoding = res.apparent_encoding
        html = etree.HTML(res.text)
    else:
        print('url1 404错误:', res.status_code, url)
        return [], ''
    urls = html.xpath('//*[@class="f20"]/a/@href')
    times = html.xpath('//*[@class="f12 blue_lighten"]/text()')  # 获取时间
    try:
        index_next_page = 'https://t.qianzhan.com{}'
        title = html.xpath('//*[@class="listpage mt30 page_comm"]/a/text()')
        href = html.xpath('//*[@class="listpage mt30 page_comm"]/a/@href')
        for n in range(len(title)):
            if '下一页' in title[n]:
                next_href = index_next_page.format(href[-1])
    except:
        next_href = ''
    if len(urls) != len(times):
        print('链接长度:', len(urls), '时间长度:', len(times))
        return False
    else:
        index_url2 = 'https:{}'
        new_urls = []
        for u in urls:
            new_urls.append(u if 'http' in u else index_url2.format(u))
        urls = new_urls
        result = [urls[n] for n in range(len(urls)) if
                  public_fun.calc_date(s_date=s_date, e_date=times[n])]  # 通过时间过滤url2
    return result, next_href


def get_data(url, search_word, max_text):
    json_result = {'source': 'qz', 'doc_id': '', 'date': '', 'download_url': '',
                   'org_name': '', 'page_num': '1', 'doc_type': 'NEW', 'title': ''}
    path = os.path.join(config.SAVE_PATH, search_word, 'news', 'qianzhan')  # 路径
    res = requests.get(url=url, headers=config.HEADERS)
    res.encoding = res.apparent_encoding
    html = etree.HTML(res.text)
    content_text = public_fun.filter_space_json(html.xpath('//*[@class="art"]//text()'))  # 正文内容

    if len(content_text) > max_text:
        try:
            # ==============================html=========================
            doc_id = url.split('/')[-1].replace('.html', '')  # 文章ID
            title = html.xpath('//*[@id="h_title"]')[0]  # 标题
            description = html.xpath('//*[@class="art"]')[0]  # 文章内容 html
            html_list = [title, description]
            html_result = public_fun.filter_space_html(html_list)
            # ==============================json=========================
            json_result['doc_id'] = doc_id
            json_result['date'] = public_fun.filter_space_json(
                html.xpath('//*[@id="pubtime_baidu"]/text()')[0].split(' ')[0])
            json_result['download_url'] = url
            json_result['org_name'] = public_fun.filter_space_json(
                html.xpath('//*[@class="l f15 mr5 lh24 bljjxue"]/a/text()'))
            json_result['title'] = public_fun.filter_space_json(html.xpath('//*[@id="h_title"]//text()'))
            public_fun.write_down_json(path=path, filename=doc_id + '.json', text=json_result)
            public_fun.write_down_html(path=path, filename=doc_id + '.html', text=html_result)
        except Exception as e:
            print(e.__traceback__.tb_lineno, url, e)
    else:
        print('文章字数不足', max_text, url)


def main(search_word, max_art, max_text, s_date):
    s_date = public_fun.reduce_date(s_date)
    url1 = 'https://t.qianzhan.com/search/?q={}'.format(search_word)  # 文章url列表
    url2_list = []  # 文章内容url
    while url1:
        one_page_url, next_page = handle(url=url1, s_date=s_date)
        url2_list += one_page_url
        if next_page and len(url2_list) < max_art:
            url1 = next_page
        else:
            url1 = ''
    url2_list = url2_list[:5] if config.DEBUG else url2_list  # 取十条测试数据
    for url2 in url2_list:
        get_data(url=url2, search_word=search_word, max_text=max_text)


if __name__ == '__main__':
    p0 = '人工智能'
    p1 = 10
    p2 = 500
    p3 = '2'
    r = main(search_word=p0, max_art=p1, max_text=p2, s_date=p3)
