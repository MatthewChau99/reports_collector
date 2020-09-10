import scrapers.report.fxbg_scraper as fxbg
import scrapers.report.robo_scraper as robo
import scrapers.news._36kr_scraper as _36kr
import time


def search(search_keyword: str, filter_keyword: str, pdf_min_num_page: str, num_years: int):
    fxbg.run(search_keyword=search_keyword, filter_keyword=filter_keyword, pdf_min_num_page=pdf_min_num_page,
             num_years=num_years)
    robo.run(search_keyword=search_keyword, filter_keyword=filter_keyword, pdf_min_num_page=pdf_min_num_page,
             num_years=num_years)
    _36kr.run(search_keyword=search_keyword, num_years=num_years)


if __name__ == '__main__':
    start_time = time.time()
    search(search_keyword='腾讯', filter_keyword='', pdf_min_num_page='100', num_years=1)
    print("--- %s seconds ---" % (time.time() - start_time))
