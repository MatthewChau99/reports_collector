from definitions import ROOT_DIR
import scrapers.report.fxbg_scraper as fxbg
import scrapers.report.robo_scraper as robo
import scrapers.news._36kr_scraper as _36kr
import scrapers.news.cyzone as cyzone
import scrapers.news.huxiu as huxiu
import scrapers.news.iyiou as iyiou
import scrapers.news.leiphone as leiphone
import scrapers.news.pencilnews as pencilnews
import scrapers.news.lieyunwang as lieyunwang
import scrapers.report.woshipm_scrapper as wspm
import time


def search(search_keyword: str, filter_keyword: str, pdf_min_num_page: str, num_years: int):
    fxbg.run(search_keyword=search_keyword, filter_keyword=filter_keyword, pdf_min_num_page=pdf_min_num_page,
             num_years=num_years)
    robo.run(search_keyword=search_keyword, filter_keyword=filter_keyword, pdf_min_num_page=pdf_min_num_page,
             num_years=num_years)
    _36kr.run(search_keyword=search_keyword, num_years=num_years)
    wspm.run(search_keyword, '3000', num_years, 30, '')

    # cyzone.run(search_keyword=search_keyword)
    # huxiu.run(search_keyword=search_keyword)
    # iyiou.run(search_keyword=search_keyword)
    # leiphone.run(search_keyword=search_keyword)
    # pencilnews.run(search_keyword=search_keyword)
    # lieyunwang.run(search_keyword=search_keyword)


if __name__ == '__main__':
    start_time = time.time()
    search(search_keyword='中芯国际', filter_keyword='', pdf_min_num_page='150', num_years=1)
    print("--- %s seconds ---" % (time.time() - start_time))
