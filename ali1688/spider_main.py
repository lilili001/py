from ali1688 import list_url_manager,product_url_manager,html_downloader,html_outputer,html_parser

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

        count = 1
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
        self.craw_detail_page()

    def craw_detail_page(self):
        parser=html_parser.HtmlParser()
        item_urls = self.product_urls.getAllUrls()
        count = 1
        while self.product_urls.hasUrl():
            item_url = self.product_urls.getUrl()
            print('craw detail page %d : %s' % (count, item_url))
            item_page_content = self.downloader.download(item_url)

            ##获取所需要的数据  title price qty images  属性
            res_content = parser.parseDetailPage(item_page_content)
            self.outputer.outputDetailPage(res_content)

            if( count == 2 ):
                return
            count = count+1


if __name__ == "__main__":
    list_urls = ["https://1618fz.1688.com/page/offerlist.htm?pageNum={}".format(str(i)) for i in range(1,11)]
    spider001 = SpiderMain()
    spider001.craw(list_urls)