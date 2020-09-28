import os
import json
from definitions import ROOT_DIR
from definitions import translate
from oss.mongodb import insert_datas
import pprint as pp


def upload_all(search_keyword):
    """
    Given a search keyword, uploads all the json files within the keyword directory to database
    :param search_keyword: the search keyword
    :return: none
    """
    summary = os.path.join(ROOT_DIR, 'cache', search_keyword, 'summary.json')
    summary = json.load(open(summary))[search_keyword]

    for source_summary in summary.keys():
        source = summary[source_summary]
        source_name = source['source']              # e.g. '36kr'
        source_type = source['source_type']         # 'news'
        data_dir = os.path.join(ROOT_DIR, 'cache', search_keyword, source_type, translate[source_name])

        json_paths = [os.path.join(data_dir, pdf_id + '.json') for pdf_id in source['data'].keys()]
        json_files = [json.load(open(json_path)) for json_path in json_paths]

        insert_datas(data_list=json_files, collection=source_name)


if __name__ == '__main__':
    upload_all('中芯国际')
