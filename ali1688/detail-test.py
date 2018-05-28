import urllib
from urllib import request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from ali1688.proxy_ip import get_data_from_file, start_validate_https
import random
import os
import requests
from http import cookiejar

#url = "https://baike.baidu.com/item/Python/407313"

ua = UserAgent()

headers = {
                'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.8',
               'Cache-Control': 'max-age=0',
               'User-Agent': ua.random,
               'Connection': 'keep-alive',

               }

def get_random_ip():
    ips=get_data_from_file()
    return random.choice(ips)

def craw():
    # 这是代理IP
    proxy={'http': get_random_ip()}
    # 创建ProxyHandler
    proxy_support=request.ProxyHandler(proxy)
    # 创建Opener
    opener=request.build_opener(proxy_support)
    # 添加User Angent
    opener.addheaders = [('User-Agent:'+ua.random)]
    # 安装OPener
    request.install_opener(opener)
    # 使用自己安装好的Opener
    request1=urllib.request.Request(url)

    response = urlopen(request1)
    print(response)

    # if response.
    #     #读取相应信息并解码
    #     html=response.read().decode("utf-8")
    #
    #     # 将测试内容写入文件
    #     root_path=os.path.abspath('.')
    #     print('=parser tool root path=============')
    #     print(root_path)
    #     f=open('files/detail.txt', 'w')
    #     f.write(html)
    #     f.close()

#
# soup = BeautifulSoup(content,'html.parser',from_encoding="gbk")
#
# price = soup.select('.table-sku')
#
# print(price)

f1 = open('files/ip_https.txt','a')
f1.truncate()

print('cleared========')

#url = 'https://detail.1688.com/offer/540424293523.html'
url = 'https://www.1688.com'
#start_validate_https(url,5)
ips = get_data_from_file()


#cookie

#声明一个CookieJar对象实例来保存cookie
cookiejar = cookiejar.CookieJar()

random_ip = (random.choice(ips)).replace('\x00','')
proxy_ip={'http': random_ip}  #想验证的代理IP

proxy_support = urllib.request.ProxyHandler(proxy_ip)
#利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
cookieHandler = request.HTTPCookieProcessor(cookiejar)
opener = urllib.request.build_opener(cookieHandler)
opener.add_handler(proxy_support)

opener.addheaders=[("User-Agent",ua.random)]
urllib.request.install_opener(opener)

req0 = request.Request(url,None,headers)

res = opener.open(req0)
print(res.read().decode('gbk'))

# response = urllib.request.urlopen(url)
# print(response.read().decode('utf-8'))
#print(urllib.request.urlopen(url).read())


# response = requests.get(url,proxies=proxy_ip,timeout=3)
# print(response.text)
