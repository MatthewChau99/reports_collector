from definitions import ROOT_DIR
import scrapers.report.fxbg_scraper as fxbg
import scrapers.report.robo_scraper as robo
import scrapers.report.woshipm_scrapper as wspm
import scrapers.news._36kr_scraper as _36kr
# import scrapers.news.cyzone as cyzone
# import scrapers.news.huxiu as huxiu
# import scrapers.news.iyiou as iyiou
# import scrapers.news.leiphone as leiphone
# import scrapers.news.pencilnews as pencilnews
# import scrapers.news.lieyunwang as lieyunwang
# import scrapers.report.woshipm_scrapper as wspm
# import scrapers.news._51pdf as _51pdf
# import scrapers.news._767stock as _767stock
import time
import sys


def search(search_keyword: str, filter_keyword: str, min_words: str, pdf_min_num_page: str, num_years: int,
           get_pdf: bool):
    fxbg.run(search_keyword=search_keyword, filter_keyword=filter_keyword, pdf_min_num_page=pdf_min_num_page,
             num_years=num_years, get_pdf=get_pdf)
    robo.run(search_keyword=search_keyword, filter_keyword=filter_keyword, pdf_min_num_page=pdf_min_num_page,
             num_years=num_years, get_pdf=get_pdf)
    _36kr.run(search_keyword=search_keyword, min_word_count=min_words, num_years=num_years, get_pdf=get_pdf)
    # wspm.run(search_keyword, min_words, num_years, 15, '', get_pdf=get_pdf)

    # cyzone.run(search_keyword=search_keyword)
    # huxiu.run(search_keyword=search_keyword)
    # iyiou.run(search_keyword=search_keyword)
    # leiphone.run(search_keyword=search_keyword)
    # pencilnews.run(search_keyword=search_keyword)
    # lieyunwang.run(search_keyword=search_keyword)

    # _51pdf.main(search_word=search_keyword, max_art=30, max_text=300, s_date='2018-01-01')
    # _767stock.main(search_word=search_keyword, max_art=30, max_text=300, s_date='2018-01-01')


def run_all(search_keyword, filter_keyword, min_words, pdf_min_num_page, num_years):
    start_time = time.time()
    if len(sys.argv) > 1:
        search(search_keyword=sys.argv[1], filter_keyword=filter_keyword, min_words=min_words,
               pdf_min_num_page=pdf_min_num_page, num_years=num_years,
               get_pdf=True)
    else:
        search(search_keyword=search_keyword, filter_keyword=filter_keyword, min_words=min_words,
               pdf_min_num_page=pdf_min_num_page, num_years=num_years,
               get_pdf=True)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    run_all(search_keyword='中芯国际', filter_keyword='', min_words='3000', pdf_min_num_page='120', num_years=1)

