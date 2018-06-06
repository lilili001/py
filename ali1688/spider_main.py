# coding=utf-8

import csv
import datetime
import math
import random
import socket
import time
import os
from ali1688 import list_url_manager,product_url_manager,html_downloader,html_outputer,html_parser, detail_craw
from ali1688.helper import changeTime

import redis
import time


root_path = os.path.abspath('.')

class SpiderMain(object):

    def __init__(self):
        self.spidername = 'baita-2018-06-05'

        pool=redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        self.r=redis.Redis(connection_pool=pool)

        self.list_urls = list_url_manager.ListUrlManager()
        self.product_urls = product_url_manager.ProductUrlManager(self.spidername,self.r)
        self.downloader = html_downloader.HtmlDownloader()
        #self.parser=html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, list_urls):

        #目标 爬取所有的列表页

        #如果redis缓存里有就不用再重新爬一次列表页来获取产品urls了
        if( self.product_urls.hasUrl() == False ):

            parser = html_parser.HtmlParser()

            count = 0
            self.list_urls.addUrls(list_urls)

            while self.list_urls.hasUrl() :

                list_url = self.list_urls.getUrl()
                print('craw %d : %s' % (count, list_url))

                content = self.downloader.download(list_url)

                item_urls = parser.parse(content) #获取当前列表页的产品url
                self.product_urls.addUrls(item_urls)


        print("=====================开始爬详情页咯===========================")
        socket.setdefaulttimeout(20)

        startTime = datetime.datetime.now()
        self.craw_detail_page()
        endTime = datetime.datetime.now()
        allTime = (endTime-startTime).seconds
        usedTime = changeTime( allTime )
        print('========任务结束:用时 %s=============' % usedTime )

    def craw_detail_page(self):
        pdc_urls = self.product_urls.getAllUrls()

        count = 0
        csvfile = open(root_path + '/%s/data-%s.csv' % ( self.spidername,  self.spidername ), 'a', newline='')
        writer = csv.writer(csvfile)

        if count == 0:
            writer.writerow(('title', 'price', 'filedir', 'supplier', 'colors', 'sizes',
                             'delivery-addr' ,'supplier_url' ,'garantee','hunpi_des','guige',
                             'title_translate','colors_translate' ))

        while self.product_urls.hasUrl():
            #while count != len( pdc_urls ):
            # 延时执行
            time.sleep( random.randint(2,12) )
            item_url = self.product_urls.getUrl()
            #item_url = pdc_urls[count]
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            count = count + 1
            print('\n[[==================craw detail page %d : %s time is : %s' % (count, item_url, nowTime))
            detail_craw.getHtml( item_url , writer ,self.spidername )

            # if count == 2:
            #     break

        csvfile.close()

if __name__ == "__main__":
    list_urls = ["https://tootang.1688.com/page/offerlist.htm?pageNum={}".format(str(i)) for i in range(1,32)]
    spider001 = SpiderMain()
    spider001.craw(list_urls)


