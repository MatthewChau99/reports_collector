import json
import os
import random
from typing import Optional
import datetime
import shutil
import pprint as pp
import time

import requests
from fake_useragent import UserAgent
from xpdf_python import wrapper as xpdf

# User ID does not change for a fixed account
# User Token changes for each individual login
USER_ID = '43934'
USER_TOKEN = 'TQWb58QRnrJXtIKUr2VG4UYy56gQzOD9Wh7VYkRHoKdVEDyKsIji1YIyS813XOGG'


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

    def get_pdf_id(self, search_keyword: str, filter_keyword: str, pdf_min_num_page: str, num_years: int) -> dict:
        """
        根据搜索结果及搜索条件获取所有符合条件pdf的id
        :param search_keyword: 标题需要包含的关键词（公司名）
        :param filter_keyword: 标题不能包含的关键词
        :param pdf_min_num_page: 最少页数限制
        :param num_years: 筛选时间范围
        :return: id_list: 所有符合条件的pdf文件的id的列表
        """

        # This is the url for the redirected API
        current_year = datetime.date.today().year
        years = [year for year in range(current_year - num_years + 1, current_year + 1)]

        search_url = 'https://api.mofoun.com/mofoun/search/report/search'
        payload = {
            'advancedQuery': 'true',
            'advancedRequest': {
                'title': search_keyword,
                'titleMustNot': filter_keyword
            },
            'keywords': search_keyword,
            'order': '2',
            'pageSize': '1000',
            'paragraphSize': '4',
            'pdfPage': pdf_min_num_page,
            'years': years
        }
        headers = self.headers.copy()
        headers.update({
            'user-token': self.user_token,
            'Content-Type': 'application/json; charset=UTF-8',
            'User-Id': self.user_id,
            'VERSION': '1.0.0',
        })
        response = self.s.post(url=search_url, data=json.dumps(payload), headers=headers).json()
        id_list = {doc['docId']: doc for doc in response['data']['dataList']}
        return id_list

    def get_pdf_url(self, doc_list: dict, doc_type: Optional[str] = '2') -> dict:
        """
        根据文档的id和类型选择获取pdf下载链接，该链接为在线查看pdf文档的链接
        :param doc_list: a list of 所有文档的id
        :param doc_type: 文档的类型，默认为2(pdf)
        :return: url_list: 所有所需要下载的pdf文件的下载链接， 形式为{pdf_id: pdf_url}
        """

        download_api_url = f'https://api.mofoun.com/mofoun/file/pdf/url'
        for doc_id in doc_list:
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
            # time_interval = random.randint(5, 8)
            # time.sleep(time_interval)
            doc = doc_list[doc_id]
            updated_doc = {}
            updated_doc.update({'doc_id': doc_id})
            updated_doc.update({'download_url': 'https://oss-buy.hufangde.com' + response['data']})
            updated_doc.update({'org_name': doc['orgName']})
            updated_doc.update({'page_num': doc['pageNum']})
            updated_doc.update({'score': doc['score']})
            updated_doc.update({'title': doc['title']})
            updated_doc.update({'download_url': 'https://oss-buy.hufangde.com' + response['data']})
            doc_list.update({doc_id: updated_doc})

        return doc_list

    def download_pdf(self, search_keyword: str, url_list: dict):
        """
        通过提供的pdf下载url下载所有pdf至新建文件夹
        :param search_keyword: 标题需要包含的关键词（公司名）
        :param url_list: 所有所需要下载的pdf文件的下载链接
        """
        if '发现报告' not in os.listdir(os.curdir):
            os.mkdir('发现报告')
        current_path = '发现报告'

        pdf_count = 0
        num_keyword = 30

        for pdf_id in url_list:
            content = self.s.get(url=url_list[pdf_id]['download_url'], headers=self.headers)
            content.encoding = 'utf-8'

            content = content.content
            cache_path = 'cache'
            cache_save_path = os.path.join(cache_path, str(pdf_id) + '.pdf')

            # Save cache pdf
            with open(cache_save_path, 'wb') as f:
                f.write(content)

            # Temporary filtering, can be deleted later for modularization
            content_text = xpdf.to_text(cache_save_path)[0]
            keyword_count = content_text.count(search_keyword)
            save_path = os.path.join(current_path, str(pdf_id) + '.pdf')

            if keyword_count >= num_keyword:
                shutil.move(cache_save_path, save_path)
                print('downloading pdf with id: %d' % pdf_id)

                # Saving doc info
                doc_info = url_list[pdf_id]
                doc_info.update({'content': content_text})
                txt_save_path = os.path.join(current_path, str(pdf_id) + '.txt')

                with open(txt_save_path, 'w', encoding='utf-8') as f:
                    json.dump(doc_info, f, ensure_ascii=False, indent=4)
                pdf_count += 1

            else:
                os.remove(cache_save_path)

        print('--------Finished downloading %d pdfs--------' % pdf_count)

    def run(self, search_keyword, filter_keyword, pdf_min_num_page, num_years):
        print('--------Begin searching pdfs from the world--------')
        pdf_id_list = self.get_pdf_id(search_keyword, filter_keyword, pdf_min_num_page, num_years)
        pdf_url_list = self.get_pdf_url(pdf_id_list)
        print('--------Begin downloading pdfs--------')
        self.download_pdf(search_keyword, pdf_url_list)


if __name__ == '__main__':
    fxbg_scraper = FXBG(USER_TOKEN, USER_ID)
    fxbg_scraper.run(search_keyword='中芯国际', filter_keyword='', pdf_min_num_page='20', num_years=1)
    # print(fxbg_scraper.get_pdf_id(search_keyword='中芯国际', filter_keyword='', pdf_min_num_page='20', num_years=5))
