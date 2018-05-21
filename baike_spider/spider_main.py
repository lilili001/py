from baike_spider import url_manager, html_downloader, html_parser, html_outputer


class SpiderMain(object):
    def __init__(self):

        self.urls = url_manager.UrlManager()  #定义 url 管理器
        self.downloader = html_downloader.HtmlDownloader() #定义 html 下载器
        self.parser = html_parser.HtmlParser()  #定义 html 贾西奇
        self.outputer = html_outputer.HtmlOutputer()  #定义 html 输出器

    def craw(self,root_url):

        count =1
        self.urls.add_new_url(root_url) # 将入口url 添加到url管理器

        # 当URL管理器中有待爬取的url的时候,启动爬虫循环
        while self.urls.has_new_url(): #当有url的时候
            try:
                new_url = self.urls.get_new_url() #获取url
                print('craw %d : %s' % (count,new_url) )
                html_cont = self.downloader.download(new_url) #下载url页面
                print(html_cont)
                new_urls,new_data = self.parser.parse(new_url,html_cont) #下载好了页面，解析页面数据 得到新的url 列表和数据

                self.urls.add_new_urls(new_urls) #对urls添加进url管理器
                self.outputer.collect_data(new_data)  #收集数据

                if count == 10 :
                    break

                count = count+1
            except:
                print('failed')

        self.outputer.output_html() #输出收集好的数据

#定义main函数
if __name__ == "__main__":
    #定义爬虫入口url
    root_url = "https://baike.baidu.com/item/Python/407313"
    #创建一个Spider
    obj_spider = SpiderMain()
    #启动爬虫
    obj_spider.craw(root_url)