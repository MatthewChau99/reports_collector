import os
import datetime
import pprint as pp
import requests
from fake_useragent import UserAgent
from xpdf_python import wrapper as xpdf
import json
import browser_cookie3


class ROBO:
    def __init__(self):
        self.s = requests.Session()
        # self.cookie = browser_cookie3.chrome(domain_name='robo.datayes.com')
        self.cookie = 'ggr_user_id=3b78c2cc-f7c5-4e93-b257-4985ae40b0e2; _ga=GA1.2.1823514846.1597399956; UM_distinctid=173ec74fbac680-0d995333c12c96-31667304-13c680-173ec74fbad761; _DA_pingback=af906782-96cb-4775-8f43-5e9c2cf3ad34; cloud-anonymous-token=1c24692788c54c34914cb93efa4fb687; grwng_uid=09544aa6-2eb5-49dc-bb6e-a9ba088eaac2; ba895d61f7404b76_gr_last_sent_cs1=7662411%40wmcloud.com; ba895d61f7404b76_gr_session_id=ec0c457b-461c-430e-a81e-4e093aa01fde; ba895d61f7404b76_gr_last_sent_sid_with_cs1=ec0c457b-461c-430e-a81e-4e093aa01fde; ba895d61f7404b76_gr_session_id_ec0c457b-461c-430e-a81e-4e093aa01fde=true; _gid=GA1.2.1792481964.1598080054; _gat=1; CNZZDATA1257961942=978492369-1597397288-%7C1598076005; cloud-sso-token=C8CF29B09ECEB4ABFBF8C2B30698D5A2; ba895d61f7404b76_gr_cs1=7662411%40wmcloud.com'
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
            download_url = self.s.get(url=download_api_url + str(id), headers=self.headers).json()['data']['downloadUrl']
            updated_dict = {}
            updated_dict.update({'doc_id': id})
            updated_dict.update({'date': id_list[id]['data']['publishTime']})
            updated_dict.update({'org_name': id_list[id]['data']['orgName']})
            updated_dict.update({'page_num': id_list[id]['data']['pageCount']})
            updated_dict.update({'doc_type': id_list[id]['type']})
            updated_dict.update({'download_url': download_url})

            updated_json.update({id: updated_dict})

        return updated_json

    def download_pdf(self, doc_id_list: dict):
        url_list = self.update_json(doc_id_list)

        pdf_count = 0

        os.chdir('/Users/admin/Desktop/资料库Startup')

        if '萝卜投研' not in os.listdir('cache'):
            os.mkdir('cache/萝卜投研')
        current_path = 'cache/萝卜投研'

        for pdf_id in url_list:
            content = self.s.get(url=url_list[pdf_id]['download_url'], headers=self.headers)
            content.encoding = 'utf-8'
            content = content.content

            pdf_save_path = os.path.join(current_path, str(pdf_id) + '.pdf')
            txt_save_path = os.path.join(current_path, str(pdf_id) + '.txt')

            try:
                print('saving pdf with id: %s' % pdf_id)

                with open(pdf_save_path, 'wb') as f:
                    f.write(content)

                content_text = xpdf.to_text(pdf_save_path)[0]
                doc_info = url_list[pdf_id]
                doc_info.update({'content': content_text})

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
        self.download_pdf(pdf_id_list)


def run(search_keyword: str, filter_keyword: str, pdf_min_num_page: str, num_years: int):
    robo_scraper = ROBO()
    robo_scraper.run(search_keyword=search_keyword, filter_keyword=filter_keyword, pdf_min_num_page=pdf_min_num_page,
                     num_years=num_years)


if __name__ == '__main__':
    run(search_keyword='中芯国际', filter_keyword='', pdf_min_num_page='200', num_years=5)
