import json
import os
from typing import Optional
import datetime
import pprint as pp
import datetime

import requests
from fake_useragent import UserAgent


class ROBO:
    def __init__(self):
        self.s = requests.Session()
        self.session_id = '445f4837-489e-4d02-9361-ec4aec16e1cc'
        self.cloud_sso_token = 'C79EF2FE14F494F336864BAE48E0151B'
        self.headers = {
            'accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, image/apng, */*; '
                      'q=0.8, application/signed-exchange; v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': '_ga=GA1.2.1531716279.1597394052; '
                      '_gid=GA1.2.1588925542.1597394052; '
                      'UM_distinctid=173ec1ae4b692d-02d0eb94d36ef9-31667304-13c680-173ec1ae4b750d; '
                      'gr_user_id=1e7779f9-ff2e-4358-97d7-3959eb44cbc0; '
                      'cloud-anonymous-token=8f8e8d705ee440598b70ab8651ea6c36; '
                      'grwng_uid=be9587f5-9787-4409-bf6e-c733155c9a6d; '
                      '_DA_pingback=d27b1587-1f27-4dd8-8b30-cbe4f4698326; '
                      'cloud-sso-token=%s; '
                      'ba895d61f7404b76_gr_last_sent_cs1=7662411ds40wmcloud.com; '
                      'ba895d61f7404b76_gr_session_id=%s; '
                      'ba895d61f7404b76_gr_last_sent_sid_with_cs1=%s; '
                      'ba895d61f7404b76_gr_cs1=7662411ds40wmcloud.com; '
                      '_gat=1; '
                      'ba895d61f7404b76_gr_session_id_%s=true' % (
                          self.cloud_sso_token, self.session_id, self.session_id, self.session_id),
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': str(UserAgent().random)
        }

    def get_pdf_id(self, search_keyword: str, filter_keyword: str, pdf_min_num_page: str, num_years: int) -> list:
        search_url = 'https://gw.datayes.com/rrp_adventure/web/search'
        headers = self.headers.copy()
        curr_year = datetime.datetime.today().year
        start_year = curr_year - num_years
        params = {
            'type': 'EXTERNAL_REPORT',
            'pageSize': 1000,
            'pageNow': '1',
            'sortOrder': 'desc',
            'query': search_keyword,
            'pubTimeStart': str(start_year) + '0101',
            'pubTimeEnd': str(curr_year) + '1231',
            'minPageCount': pdf_min_num_page
        }
        response = self.s.get(url=search_url, headers=headers, params=params).json()
        # print(response)
        json_list = response['data']['list']
        id_list = [doc['data']['id'] for doc in json_list]
        return id_list

    # def get_pdf_url(self, doc_id_list: list) -> dict:
    #     url_list = {}
    #     download_api_url = f'https://gw.datayes.com/rrp_adventure/web/externalReport/'
    #
    #     for doc_id in doc_id_list:
    #         headers = self.headers.copy()
    #         download_url = download_api_url + str(doc_id)
    #         response = self.s.get(url=download_url, headers=headers).json()
    #         url_list.update({doc_id: response['data']['downloadUrl']})
    #
    #     return url_list

    def download_pdf(self, doc_id_list: list):
        download_api_url = f'https://gw.datayes.com/rrp_adventure/web/externalReport/'
        url_list = {doc_id: download_api_url + str(doc_id) for doc_id in doc_id_list}

        if '萝卜投研' not in os.listdir(os.curdir):
            os.mkdir('萝卜投研')
        current_path = '萝卜投研'

        for pdf_id in url_list:
            content = self.s.get(url=url_list[pdf_id], headers=self.headers).content
            save_path = os.path.join(current_path, str(pdf_id) + '.pdf')
            with open(save_path, 'wb') as f:
                f.write(content)

    def run(self, search_keyword, filter_keyword, pdf_min_num_page, num_years):
        pdf_id_list = self.get_pdf_id(search_keyword, filter_keyword, pdf_min_num_page, num_years)
        # pdf_url_list = self.get_pdf_url(pdf_id_list)
        self.download_pdf(pdf_id_list)


if __name__ == '__main__':
    robo_scraper = ROBO()
    robo_scraper.run(search_keyword='中芯国际', filter_keyword='', pdf_min_num_page='100', num_years=5)
    # print(robo_scraper.get_pdf_id(search_keyword='中芯国际', filter_keyword='', pdf_min_num_page='120', num_years=1))
