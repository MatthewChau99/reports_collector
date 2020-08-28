import json

import xpdf_python.wrapper as xpdf
import os
import pdfkit


def pdf_to_text(pdf_path):
    text = xpdf.to_text(pdf_path)
    return text


class Filter:
    def __init__(self):
        """
        A filter that processes data collected from the scrapers
        either pdf -> text for pdf files
        or html -> pdf -> text for html files
        """
        self.keyword_list = ['市场', '股份', '国际', '芯片']

    def count_keywords(self, text: str) -> dict:
        counter = {}

        for keyword in self.keyword_list:
            count = text.count(keyword)
            counter.update({keyword: count})

        return counter

    def html_to_pdf(self, directory):
        """
        Data processing for data collected from websites that do now allow pdf download
        :param directory: the directory that contains the .html and .json files
        """
        curr_dir = os.getcwd()
        os.chdir(directory)

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

                # Removing html files
                os.remove(filename)
        os.chdir(curr_dir)

    def pdf_filter(self, directory):
        """
        Data processing for data collected from websites that allow pdf download
        :param directory: the directory that contains the .pdf and .json files
        """
        curr_dir = os.getcwd()
        os.chdir(directory)
        company_name_threshold = 30

        for filename in os.listdir(os.curdir):
            if filename.endswith('.pdf'):
                doc_id = filename[0:len(filename) - 4]
                json_filename = doc_id + '.json'

                print('Processing file with id %s' % doc_id)


                try:
                    # Getting text from pdf
                    text = pdf_to_text(filename)[0]

                    # Add company name to keyword
                    company_name = os.path.basename(os.getcwd())
                    self.keyword_list.append(company_name)

                    # Adding attributes to txt
                    keywords_count = self.count_keywords(text)

                    with open(json_filename, 'r', encoding='utf-8') as file:
                        attributes = json.load(file)

                        # Already been processed
                        if 'content' in attributes.keys() or 'keywordCount' in attributes.keys():
                            continue

                        attributes.update({'content': text,
                                           'keywordCount': keywords_count})
                        file.close()

                    # Company name count
                    if attributes['keywordCount'][company_name] <= company_name_threshold:
                        print('File %s deleted due to not enough keyword occurrences' % doc_id)
                        raise ValueError

                    with open(doc_id + '.json', 'w', encoding='utf-8') as file:
                        json.dump(attributes, file, ensure_ascii=False, indent=4)
                        file.close()
                except (ValueError, SyntaxError):
                    if os.path.exists(json_filename):
                        os.remove(json_filename)
                    if os.path.exists(filename):
                        os.remove(filename)
                    if os.path.exists(doc_id + '.txt'):
                        os.remove(doc_id + '.txt')
                    continue
        os.chdir(curr_dir)

    def run_filter(self, file_type: str):
        content_dir = 'cache/news' if file_type == 'news' else 'cache/report'
        for source_name in os.listdir(content_dir):
            print('======== Processing files from %s ========' % source_name)
            for keyword_name in os.listdir(os.path.join(content_dir, source_name)):
                curr_dir = os.path.join(content_dir, source_name, keyword_name)
                if file_type == 'news':
                    self.html_to_pdf(curr_dir)
                self.pdf_filter(curr_dir)


def run_both_filters():
    file_filter = Filter()
    file_filter.run_filter(file_type='news')
    file_filter.run_filter(file_type='report')


if __name__ == '__main__':
    run_both_filters()
