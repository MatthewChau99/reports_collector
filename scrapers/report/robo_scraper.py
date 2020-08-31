import datetime
import json
import os

import requests
from fake_useragent import UserAgent


class ROBO:
    def __init__(self):
        self.s = requests.Session()
        # self.cookie = browser_cookie3.chrome(domain_name='robo.datayes.com')
        self.cookie = 'gr_user_id=e097b71f-2765-486a-b4f4-acf7cc4d8140; ba895d61f7404b76_gr_session_id=2bd11f04-74b6-42ce-bb8b-a049cbdac411; UM_distinctid=1744493d767f4-00bbf701952605-31677304-13c680-1744493d768d62; ba895d61f7404b76_gr_session_id_2bd11f04-74b6-42ce-bb8b-a049cbdac411=true; grwng_uid=23298924-e484-4fd4-80d6-33f8b8e749b3; cloud-sso-token=C6A7E1424B0039B433E3EB03E1184993; cloud-anonymous-token=13e68f6f127e4580a01069d918f3daf7; _ga=GA1.2.72455160.1598878374; _gid=GA1.2.162239657.1598878374; _gat=1'
        self.headers = {
            'accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, image/apng, */*; '
                      'q=0.8, application/signed-exchange; v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': self.cookie,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': str(UserAgent().random)
        }

    def get_pdf_id(self, search_keyword: str, filter_keyword: str, pdf_min_num_page: str, num_years: int) -> dict:
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
        json_list = response['data']['list']
        # pp.pprint(json_list)
        id_list = {doc['data']['id']: doc for doc in json_list}
        print('--------Found %d pdfs in 萝卜投研--------' % len(id_list))
        return id_list

    def update_json(self, id_list: dict):
        download_api_url = f'https://gw.datayes.com/rrp_adventure/web/externalReport/'
        updated_json = {}

        for id in id_list:
            download_url = self.s.get(url=download_api_url + str(id), headers=self.headers).json()['data'][
                'downloadUrl']

            date = id_list[id]['data']['publishTime']
            date = date[0:4] + date[5:7] + date[8:10]

            updated_dict = {'source': 'robo',
                            'doc_id': id,
                            'date': date,
                            'org_name': id_list[id]['data']['orgName'],
                            'page_num': id_list[id]['data']['pageCount'],
                            'doc_type': id_list[id]['type'],
                            'download_url': download_url,
                            'title': id_list[id]['data']['title']}

            updated_json.update({id: updated_dict})

        return updated_json

    def download_pdf(self, search_keyword: str, doc_id_list: dict):
        url_list = self.update_json(doc_id_list)

        pdf_count = 0

        os.chdir('/Users/admin/Desktop/资料库Startup')

        if 'report' not in os.listdir('cache'):
            os.mkdir('cache/report')
        if '萝卜投研' not in os.listdir('cache/report'):
            os.mkdir('cache/report/萝卜投研')

        current_path = 'cache/report/萝卜投研'

        if search_keyword not in os.listdir(current_path):
            os.mkdir(os.path.join(current_path, search_keyword))
        current_path = os.path.join(current_path, search_keyword)

        for pdf_id in url_list:
            content = self.s.get(url=url_list[pdf_id]['download_url'], headers=self.headers)
            content.encoding = 'utf-8'
            content = content.content

            pdf_save_path = os.path.join(current_path, str(pdf_id) + '.pdf')
            txt_save_path = os.path.join(current_path, str(pdf_id) + '.json')

            try:
                print('saving pdf with id: %s' % pdf_id)

                with open(pdf_save_path, 'wb') as f:
                    f.write(content)

                # content_text = xpdf.to_text(pdf_save_path)[0]
                doc_info = url_list[pdf_id]
                # doc_info.update({'content': content_text})

                with open(txt_save_path, 'w', encoding='utf-8') as f:
                    json.dump(doc_info, f, ensure_ascii=False, indent=4)

                pdf_count += 1
            except:
                if os.path.exists(pdf_save_path):
                    os.remove(pdf_save_path)

                if os.path.exists(txt_save_path):
                    os.remove(txt_save_path)

                continue

        print('--------Finished downloading %d pdfs from 萝卜投研--------' % pdf_count)

    def run(self, search_keyword: str, filter_keyword: str, pdf_min_num_page: str, num_years: int):
        print('--------Begin searching pdfs from 萝卜投研--------')
        pdf_id_list = self.get_pdf_id(search_keyword, filter_keyword, pdf_min_num_page, num_years)
        self.download_pdf(search_keyword, pdf_id_list)


def run(search_keyword: str, filter_keyword: str, pdf_min_num_page: str, num_years: int):
    robo_scraper = ROBO()
    robo_scraper.run(search_keyword=search_keyword, filter_keyword=filter_keyword, pdf_min_num_page=pdf_min_num_page,
                     num_years=num_years)


if __name__ == '__main__':
    run(search_keyword='中芯国际', filter_keyword='', pdf_min_num_page='200', num_years=5)
