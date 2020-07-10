#!/usr/bin/python

"""
Created on Fri July 10 11:22:02 2020
@author: Zefang
"""

import urllib3
from os import getcwd
from os import remove
from datetime import datetime
from datetime import timedelta
from PyPDF2 import PdfFileReader, PdfFileWriter

import warnings
warnings.resetwarnings()
warnings.filterwarnings('ignore')#supress PdfFileReader warnings

#download pages and merge into single pdf
def download_newspaper(date):
    path = getcwd()
    url1 = "http://bjwb.bjd.com.cn/images/"
    pages = [str(x).zfill(2) for x in range(1,100)]    
    filename = "BJENewspaper_" + date.replace('/','').replace('-','') + ".pdf"
    if filename in listdir(path):
       print("found " + filename)
       return

    writer = PdfFileWriter()
    for page in pages:
        url = url1 + date + "/" + page + "/" + page + ".pdf"
        temp_page = "BJENewspaper_" + date.replace('/','').replace('-','') + "-" + page + ".pdf"        
        http = urllib3.PoolManager()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = http.request('GET', url, preload_content=False)
        print("try download " + date + " Page " + page)
        
        if (len(response.data) < 2**13): #empty page if less than 5.1K
            break
        with open(path + 'temp/' + temp_page,"wb") as outpage:
            outpage.write(response.data)
        reader = PdfFileReader(path + 'temp/' + temp_page, strict=False)
        writer.addPage(reader.getPage(0))
        remove(path + 'temp/' + temp_page)#clear temp depository
    with open(filename, 'wb') as outfile:
        writer.write(outfile)
    print("Completed "+filename)
        
def main_history(): #use to pull archieve from 2019-01-01
    today = datetime.today()
    while(today.date() > datetime(2018 , 12, 31).date()):
        today = today - timedelta(days=1)
        date = today.strftime('%Y-%m/%d')
        download_newspaper(date)
                
def main(): #run with cronjob for daily update
    today = datetime.today()
    date = today.strftime('%Y-%m/%d')
    download_newspaper(date)

if __name__ == "__main__":
    main()
