import os
import shutil
import pdfkit
from datetime import datetime
now = datetime.now()

def htmltopdf(article,path,title,date,sum,id):
    if(prefilter(date)):
        with open("temp.html", "w", encoding='utf-8') as file:
            file.write(str(article))
        file.close()
        folderPath = path + title + "/"
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
            options = {
                'quiet': '',
                'encoding': "UTF-8"
            }
            pdfkit.from_file("temp.html", str(id)+'.pdf', options = options)
            shutil.move(str(id)+'.pdf',folderPath)
            sum.write(title + "\n")
            sum.write(date + "\n")
            sum.write(folderPath + "\n")
            sum.write("\n")

def prefilter(date):
    ret = True
    dateToday = datetime.now().strftime("%Y")
    years = int(dateToday) - int(date[0:4])
    if(date[0] == '2' and years > 2):
        ret = False
    return ret
