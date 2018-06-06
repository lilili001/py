import urllib
from urllib import request
from urllib.request import urlopen
from fake_useragent import UserAgent

from ali1688 import detail_craw

class HtmlDownloader(object):
    def download(self, url):

        # # 创建request对象
          request=urllib.request.Request(url)
        # # 添加数据
        # #request.add_data('a', 1)
        # # 添加http的header
          ua = UserAgent()
        #
          request.add_header('User-Agent', ua.random)
        # # 发送请求获取结果
          response=urlopen(request)
        #
          return response.read()

        #ua = UserAgent()
        # proxy = detail_craw.get_proxy()
        # proxy_handler = request.ProxyHandler({"http":"http://{}".format(proxy)})
        # opener = request.build_opener(proxy_handler)
        # req = request.Request(url)
        # req.add_header('User-Agent',ua.random)
        # r = opener.open(req)
        #print('=========cat download===================')
        # print(r)
        # r.close()
        #return r.read()
