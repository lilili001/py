import urllib
from urllib import request
from urllib.request import urlopen
from fake_useragent import UserAgent

class HtmlDownloader(object):
    def download(self, url):

        # 创建request对象
        request=urllib.request.Request(url)
        # 添加数据
        #request.add_data('a', 1)
        # 添加http的header
        ua = UserAgent()

        request.add_header('User-Agent', ua.random)
        # 发送请求获取结果
        response=urlopen(request)

        return response.read()