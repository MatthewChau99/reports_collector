import json
import os

import pdfkit
from xpdf_python import wrapper as xpdf
from Filter.pdf_filter import pdf_filter
import pprint as pp

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


def html_to_pdf(dir):
    curr_dir = os.getcwd()
    os.chdir(dir)

    # Add company name to keyword
    company_name = os.path.basename(os.getcwd())
    update_kw_list = KEYWORD_LIST.copy()
    update_kw_list.append(company_name)

    for filename in os.listdir(os.curdir):
        if filename.endswith('.html'):
            doc_id = filename[0:len(filename) - 5]
            pdf_filename = doc_id + '.pdf'

            # Converting to PDF
            options = {
                'quiet': '',
                'page-size': 'Letter',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'no-outline': None
            }
            pdfkit.from_file(filename, pdf_filename, options=options)

            os.remove(filename)
    os.chdir(curr_dir)


def run_html_filter():
    dir = 'cache/news'
    for source_name in os.listdir(dir):
        for keyword_name in os.listdir(os.path.join(dir, source_name)):
            curr_dir = os.path.join(dir, source_name, keyword_name)
            html_to_pdf(curr_dir)
            pdf_filter(curr_dir)


if __name__ == '__main__':
    run_html_filter()
