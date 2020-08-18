import os
import datetime

import requests
from fake_useragent import UserAgent


class ROBO:
    def __init__(self):
        self.s = requests.Session()
        self.session_id = 'aa8f1d82-359a-4e8b-bd6f-283e23cdcc1b'
        self.cloud_sso_token = '0FF8BCFFD1E7F2F04DB5CF3388626943'
        self.headers = {
            'accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, image/apng, */*; '
                      'q=0.8, application/signed-exchange; v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'gr_user_id=3b78c2cc-f7c5-4e93-b257-4985ae40b0e2; _ga=GA1.2.1823514846.1597399956; UM_distinctid=173ec74fbac680-0d995333c12c96-31667304-13c680-173ec74fbad761; cloud-anonymous-token=1c24692788c54c34914cb93efa4fb687; grwng_uid=09544aa6-2eb5-49dc-bb6e-a9ba088eaac2; ba895d61f7404b76_gr_session_id=aa8f1d82-359a-4e8b-bd6f-283e23cdcc1b; _gid=GA1.2.21976762.1597680845; _gat=1; ba895d61f7404b76_gr_session_id_aa8f1d82-359a-4e8b-bd6f-283e23cdcc1b=true; cloud-sso-token=67985D9A5566BB9AC5953F254E08FE61',
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
        print(response)
        json_list = response['data']['list']
        id_list = [doc['data']['id'] for doc in json_list]
        return id_list

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
