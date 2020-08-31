import json

import xpdf_python.wrapper as xpdf
import os
import pdfkit


class Filter:
    def __init__(self):
        """
        A filter that processes data collected from the scrapers
        either pdf -> text for pdf files
        or html -> pdf -> text for html files
        """
        self.tags = {'历史沿革': ({'历史沿革', '历史事件', '发展历程'}, 3),
                     '组织架构': ({'组织架构'}, 3),
                     '股权架构': ({'股权架构', '股权变动', '股权结构', '股东', '股权'}, 3),
                     '管理团队': ({'管理团队', '董事会', '管理人'}, 3),
                     '薪酬体系': ({'薪酬体系'}, 3),
                     '奖励机制': ({'奖励机制'}, 3),
                     '产品': ({'业务', '服务', '产品'}, 3),
                     '生产情况': ({'生产情况', '生产流程', '生产工艺', '产能'}, 3),
                     '销售情况': ({'销售', '市场需求', '渠道'}, 3),
                     '知识产权': ({'知识产权', '商标', '专利'}, 3),
                     '核心技术': ({'核心技术', '核心竞争力', '壁垒'}, 3),
                     '研发事项': ({'研发', '迭代'}, 3),
                     '客户': ({'客户', '用户', '合作', '伙伴'}, 3),
                     '市场需求': ({'市场需求'}, 3),
                     '竞争对象': ({'对手', '竞争格局', '竞争态势', '头部', '竞品'}, 3),
                     '供应商': ({'供应', '采购'}, 3),
                     '市场占有率': ({'市场占有率', '市场份额', '市场竞争力'}, 3),
                     '运营情况': ({'收入', '营收', '成本', '债务'}, 3),
                     '商业模式': ({'商业模式', '经营模式', '理念', '业务模型', '盈利模式', '增长点', '商业布局'}, 3),
                     '发展战略': ({'战略', '发展目标', '策略', '规划', '未来', '投资', '融资'}, 3)
                     }
        self.keyword_list = {'历史沿革': '历史沿革', '历史事件': '历史沿革', '发展历程': '历史沿革',
                             '组织架构': '组织架构',
                             '股权架构': '股权架构', '股权变动': '股权架构', '股权结构': '股权架构', '股东': '股权架构', '股权': '股权架构',
                             '管理团队': '管理团队', '董事会': '管理团队', '管理人': '管理团队',
                             '薪酬体系': '薪酬体系',
                             '奖励机制': '奖励机制',
                             '业务': '产品', '服务': '产品', '产品': '产品',
                             '生产情况': '生产情况', '生产流程': '生产情况', '生产工艺': '生产情况', '产能': '生产情况',
                             '销售': '销售情况', '市场需求': '销售情况', '渠道': '销售情况',
                             '知识产权': '知识产权', '商标': '知识产权', '专利': '知识产权',
                             '核心技术': '核心技术', '核心竞争力': '核心技术', '壁垒': '壁垒',
                             '研发': '研发事项', '迭代': '研发事项',
                             '客户': '客户', '用户': '客户', '合作': '客户', '伙伴': '客户',
                             '对手': '竞争对象', '竞争格局': '竞争对象', '竞争态势': '竞争对象', '头部': '竞争对象', '竞品': '竞争对象',
                             '供应': '供应商', '采购': '供应商',
                             '市场占有率': '市场占有率', '市场份额': '市场占有率', '市场竞争力': '市场占有率',
                             '收入': '运营情况', '营收': '运营情况', '成本': '运营情况', '债务': '运营情况',
                             '商业模式': '商业模式', '经营模式': '商业模式', '理念': '商业模式', '业务模型': '商业模式', '盈利模式': '商业模式',
                             '增长点': '商业模式', '商业布局': '商业模式',
                             '战略': '发展战略', '发展目标': '发展战略', '策略': '发展战略', '规划': '发展战略', '未来': '发展战略', '投资': '发展战略',
                             '融资': '发展战略'
                             }

    def count_keywords(self, text: str) -> dict:
        """
        Count the number of occurrences of each keyword in self.keyword_list in text
        :param text: string version of pdf
        :return: a {keyword:count} dictionary
        """
        counter = {}

        for keyword in self.keyword_list:
            count = text.count(keyword)
            counter.update({keyword: count})

        return counter

    def count_tags(self, keyword_counter: dict):
        counter = {}

        for tag in self.tags:
            count = sum([keyword_counter[keyword] for keyword in self.tags[tag][0]])
            if count >= self.tags[tag][1]:
                counter.update({tag: count})

        return counter

    def pdf_to_text(self, pdf_path):
        text = xpdf.to_text(pdf_path)
        return text

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

    def pdf_process(self, directory):
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
                    text = self.pdf_to_text(filename)[0]

                    # Add company name to keyword
                    company_name = os.path.basename(os.getcwd())
                    self.keyword_list.update({company_name: '公司名称'})

                    # Adding attributes to txt
                    keywords_count = self.count_keywords(text)

                    # Company name count
                    if keywords_count[company_name] <= company_name_threshold:
                        print('File %s deleted due to not enough keyword occurrences' % doc_id)
                        raise ValueError

                    # Adding tags to txt
                    tags_count = self.count_tags(keywords_count)

                    with open(json_filename, 'r', encoding='utf-8') as file:
                        attributes = json.load(file)

                        # Already been processed
                        if 'content' in attributes.keys() or 'keywordCount' in attributes.keys():
                            continue

                        # Update json file
                        attributes.update({'content': text,
                                           'keywordCount': keywords_count,
                                           'tags': tags_count})
                        file.close()

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
        """
        For news: html --> pdf --> process pdf --> update json
        For reports: pdf --> process pdf --> update json
        :param file_type: can either be 'news' or 'report'
        """
        content_dir = 'cache/news' if file_type == 'news' else 'cache/report'
        for source_name in os.listdir(content_dir):
            # source_name: 发现报告/萝卜投研……
            print('======== Processing files from %s ========' % source_name)
            for keyword_name in os.listdir(os.path.join(content_dir, source_name)):
                # keyword_name: 中芯国际/可口可乐……
                curr_dir = os.path.join(content_dir, source_name, keyword_name)
                if file_type == 'news':
                    self.html_to_pdf(curr_dir)
                self.pdf_process(curr_dir)


def run_both_filters():
    file_filter = Filter()
    file_filter.run_filter(file_type='news')
    file_filter.run_filter(file_type='report')


if __name__ == '__main__':
    run_both_filters()
