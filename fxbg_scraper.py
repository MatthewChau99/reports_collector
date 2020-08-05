import json
import os
from typing import Optional

import requests
from fake_useragent import UserAgent

USER_ID = '43934'
USER_TOKEN = 'Q7agWNeGdxkg16UjbWjjUHzz1FUf7YTeER5fZPBYrI97zc9oWbW3i6pw2Kcorr4h'


class FXBG:
    def __init__(self, user_token: str, user_id: str):
        """
        登录的时候需要提供一个用户token和一个用户id
        :param user_token: 用户密钥
        :param user_id: 用户ID
        """
        self.s = requests.Session()
        self.user_token = user_token
        self.user_id = str(user_id)

        # Request Headers
        self.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'no-cache',
            'origin': 'https://www.fxbaogao.com',
            'pragma': 'no-cache',
            'referer': 'https://www.fxbaogao.com/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': str(UserAgent().random)
        }

    def get_pdf_id(self, search_keyword: str, min_num_page: str) -> list:
        """
        根据搜索结果及搜索条件获取所有符合条件pdf的id
        :param search_keyword: 搜索关键词
        :param min_num_page: 最少页数限制
        :return: id_list: 所有符合条件的pdf文件的id的列表
        """
        search_url = 'https://api.mofoun.com/mofoun/search/report/search'
        payload = {
            'keywords': search_keyword,
            'order': '2',
            'pageNum': '1',
            'pageSize': min_num_page,
            'paragraphSize': '4',
            'pdfPage': '20'
        }
        headers = self.headers.copy()
        headers.update({
            'user-token': self.user_token,
            'Content-Type': 'application/json; charset=UTF-8',
            'User-Id': self.user_id,
            'VERSION': '1.0.0',
        })
        response = self.s.post(url=search_url, data=json.dumps(payload), headers=headers).json()
        id_list = [doc['docId'] for doc in response['data']['dataList']]
        return id_list

    def get_pdf_url(self, doc_id_list: list, doc_type: Optional[str] = '2') -> dict:
        """
        根据文档的id和类型选择获取pdf下载链接，该链接为在线查看pdf文档的链接
        :param doc_id_list: a list of 所有文档的id
        :param doc_type: 文档的类型，默认为2(pdf)
        :return: url_list: 所有所需要下载的pdf文件的下载链接， 形式为{pdf_id: pdf_url}
        """
        url_list = {}
        download_api_url = f'https://api.mofoun.com/mofoun/file/pdf/url'
        for doc_id in doc_id_list:
            params = {
                'docId': doc_id,
                'docType': doc_type
            }
            headers = self.headers.copy()
            headers.update({
                'user-token': self.user_token,
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'User-Id': self.user_id,
                'VERSION': '110100',
            })
            response = self.s.get(url=download_api_url, headers=headers, params=params).json()
            url_list.update({doc_id: 'https://oss-buy.hufangde.com' + response['data']})

        return url_list

    def download_pdf(self, url_list: dict):
        """
        通过提供的pdf下载url下载所有pdf至新建文件夹
        :param url_list: 所有所需要下载的pdf文件的下载链接
        """
        if '发现报告' not in os.listdir():
            os.mkdir('发现报告')
        current_path = '发现报告'
        for pdf_id in url_list:
            content = self.s.get(url=url_list[pdf_id], headers=self.headers).content
            save_path = os.path.join(current_path, str(pdf_id) + '.pdf')
            with open(save_path, 'wb') as f:
                f.write(content)

    def run(self, search_keyword, min_num_page):
        pdf_id_list = self.get_pdf_id(search_keyword, min_num_page)
        pdf_url_list = self.get_pdf_url(pdf_id_list)
        self.download_pdf(pdf_url_list)


if __name__ == '__main__':
    fxbg_scraper = FXBG(USER_TOKEN, USER_ID)
    fxbg_scraper.run('中芯国际', '20')
