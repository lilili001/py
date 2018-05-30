# coding=utf-8

import csv
import datetime
import math
import random
import time
import os
from ali1688 import list_url_manager,product_url_manager,html_downloader,html_outputer,html_parser, detail_craw
from ali1688.helper import changeTime

root_path = os.path.abspath('.')

class SpiderMain(object):

    def __init__(self):

        self.list_urls = list_url_manager.ListUrlManager()
        self.product_urls = product_url_manager.ProductUrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        #self.parser=html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, list_urls):
        #目标 爬取所有的列表页

        parser = html_parser.HtmlParser()

        count = 0
        self.list_urls.addUrls(list_urls)

        while self.list_urls.hasUrl():

            list_url = self.list_urls.getUrl()
            print('craw %d : %s' % (count, list_url))

            content = self.downloader.download(list_url)

            item_urls = parser.parse(content) #获取当前列表页的产品url
            self.product_urls.addUrls(item_urls)

            if count == 2:
                break
            count = count+1

        print("=====================开始爬详情页咯===========================")
        startTime = datetime.datetime.now()
        self.craw_detail_page()
        endTime = datetime.datetime.now()
        allTime = (endTime-startTime).seconds
        usedTime = changeTime( allTime )
        print('========任务结束:用时 %s=============' % usedTime )
        
    def craw_detail_page(self):
        item_urls = self.product_urls.getAllUrls()

        csvfile = open(root_path + '/files/data.csv', 'w', newline='')
        writer = csv.writer(csvfile)
        writer.writerow(('title', 'price', 'filedir', 'supplier', 'colors', 'sizes', 'delivery-addr' ,'supplier_url' ,'title_translate','colors_translate' ))

        count = 0
        while self.product_urls.hasUrl():
            # 延时执行
            time.sleep( random.randint(2,12) )
            item_url = self.product_urls.getUrl()
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            count = count + 1
            print('\n[[==================craw detail page %d : %s time is : %s' % (count, item_url, nowTime))
            detail_craw.getHtml( item_url , writer )

            # if count == 2:
            #     break

        csvfile.close()

if __name__ == "__main__":
    list_urls = ["https://ruiyige.1688.com/page/offerlist_91223991.htm?pageNum={}".format(str(i)) for i in range(1,17)]
    spider001 = SpiderMain()
    spider001.craw(list_urls)

