import json
import os

from xpdf_python import wrapper as xpdf

KEYWORD_LIST = ['市场', '股份', '国际', '芯片']


def pdf_to_text(pdf_path):
    text = xpdf.to_text(pdf_path)
    return text


def count_keywords(text: str, keywords: list) -> dict:
    # Can be replaced with a more optimized keyword count
    counter = {}

    for keyword in keywords:
        count = text.count(keyword)
        counter.update({keyword: count})

    return counter


def pdf_filter(dir):
    curr_dir = os.getcwd()
    os.chdir(dir)
    company_name_threshold = 30

    for filename in os.listdir(os.curdir):
        if filename.endswith('.pdf'):
            doc_id = filename[0:len(filename) - 4]
            json_filename = doc_id + '.json'

            try:
                # Getting text from pdf
                text = pdf_to_text(filename)[0]

                # Add company name to keyword
                company_name = os.path.basename(os.getcwd())
                update_kw_list = KEYWORD_LIST.copy()
                update_kw_list.append(company_name)

                # Adding attributes to txt
                keywords_count = count_keywords(text, update_kw_list)

                with open(json_filename, 'r', encoding='utf-8') as file:
                    attributes = json.load(file)

                    if 'content' in attributes.keys() or 'keywordCount' in attributes.keys():
                        continue

                    attributes.update({'content': text,
                                       'keywordCount': keywords_count})
                    file.close()

                # Company name count
                if attributes['keywordCount'][company_name] <= company_name_threshold:
                    print('Not enough keywords')
                    raise ValueError

                with open(doc_id + '.json', 'w', encoding='utf-8') as file:
                    json.dump(attributes, file, ensure_ascii=False, indent=4)
                    file.close()
            except:
                if os.path.exists(json_filename):
                    os.remove(json_filename)
                if os.path.exists(filename):
                    os.remove(filename)
                if os.path.exists(doc_id + '.txt'):
                    os.remove(doc_id + '.txt')
                continue
    os.chdir(curr_dir)


def run_pdf_filter():
    dir = 'cache/report'
    for source_name in os.listdir(dir):
        for keyword_name in os.listdir(os.path.join(dir, source_name)):
            curr_dir = os.path.join(dir, source_name, keyword_name)
            pdf_filter(curr_dir)


if __name__ == '__main__':
    run_pdf_filter()
