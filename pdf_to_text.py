import os
import time

import xpdf_python.wrapper as wrapper
from definitions import ROOT_DIR

if __name__ == '__main__':
    start_time = time.time()

    # file = 'cache/中芯国际/news/36kr/1723761262593.pdf'
    path = os.path.join(ROOT_DIR, 'cache', '中芯国际', 'report', '萝卜投研', '3807813.pdf')

    text = wrapper.to_text(path)[0]
    text = text
    print(text)
    print(len(text))

    # pdf = pdfplumber.open(path)
    # page = pdf.pages[0]
    # text = page.extract_text()
    # print(text)
    # pdf.close()

    print("--- %s seconds ---" % (time.time() - start_time))
