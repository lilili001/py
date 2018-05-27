
import urllib
from urllib import request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

import random
import os


url = "https://detail.1688.com/offer/525034967662.html"

ua = UserAgent()

headers = {'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.8',
               'Cache-Control': 'max-age=0',
               'User-Agent': ua.random,
               'Connection': 'keep-alive',
               'Referer': 'https://detail.1688.com/offer/523819601189.html'
               }

ips = get_data_from_file()

#这是代理IP
proxy = {'http':random.choice( ips )}
#创建ProxyHandler
proxy_support = request.ProxyHandler(proxy)
#创建Opener
opener = request.build_opener(proxy_support)
#添加User Angent
opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
#安装OPener
request.install_opener(opener)
#使用自己安装好的Opener
response = request.urlopen(url)
#读取相应信息并解码
html = response.read().decode("gbk")

#将测试内容写入文件
root_path = os.path.abspath('.')
print('=parser tool root path=============')
print(root_path)
f = open('files/detail.txt','w')
f.write(html)
f.close()

#打印信息
print(f.read())
#
# soup = BeautifulSoup(content,'html.parser',from_encoding="gbk")
#
# price = soup.select('.table-sku')
#
# print(price)