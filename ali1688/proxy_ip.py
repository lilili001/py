import urllib
import urllib.request
from bs4 import BeautifulSoup
import requests
import threading

import os

User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header = {}
header['User-Agent'] = User_Agent

def getIps(ip_page_count=1):

    httpRes = []
    httpsRes = []
    try:

        for page in range(1,ip_page_count):

            url = 'http://www.xicidaili.com/nn/%s'%page
            req = urllib.request.Request(url,headers=header)
            res = urllib.request.urlopen(req).read()

            soup = BeautifulSoup(res,'html.parser')
            trs = soup.findAll('tr')

            for tr in trs[1:]:
                tds=tr.find_all('td')
                ip=((tds[1].contents[0]).strip()).replace('\x00','')
                port=(tds[2].text).strip()
                protocol=(tds[5].text).strip()
                if protocol == 'HTTP':
                    httpRes.append('http://' + ip + ':' + port)
                elif protocol == 'HTTPS':
                    httpsRes.append('https://' + ip + ':' + port)

    except:
        print('error')

    return httpRes,httpsRes

#验证ip有效性 并存在本地文件中

def validate_http(host,port,url):
    f = open('files/ip_http.txt','a')
    f.truncate()
    try:
        requests.get(url,proxies={'http':host+":"+port},timeout=3)
    except:
        print(f)
    else:
        print('==============================success\n')
        f.write(host+':'+port+'\n')

def validate_https(host,port,url):
    print('start validate https:\n')
    f = open('files/ip_https.txt','a')
    print('***************开始清空咯。。。\n')
    f.truncate()
    try:
        res = requests.get(url,proxies={'http':host+":"+port},timeout=3)
    except:
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxx false\n')
        #print(f)
    else:
        print('==============================success\n')
        #print(res.text)
        host = host.replace("\x00",'')
        f.write(host+':'+port+'\n')
        print('=========='+host+':'+port+'====================写入成功\n')


#开启线程验证有效性 目的是的得到有效的ip地址列表
def validate(url,ip_page_count=1,is_https=None):
    httpRes, httpsRes=getIps(ip_page_count)

    print('====http ips=========')
    print(httpRes)
    print('====https ips=========')
    print(httpsRes)

    thread1=[]

    root_path=os.path.abspath('.')

    ip_res = httpRes
    target = validate_http
    file_path = root_path+'/files/ip_http.txt'

    if is_https == 1:
        ip_res = httpsRes
        target = validate_https
        file_path= root_path+'/files/ip_https.txt'

    open(file_path, 'a').truncate()

    for ip in ip_res:
        host=str(ip.split(':')[-2][2:]).strip()
        port=str(ip.split(':')[-1]).strip()
        t=threading.Thread(target=target, args=(host, port, url))
        thread1.append(t)

    for i in range(len(ip_res)):
        thread1[i].start()

    for i in range(len(ip_res)):
        thread1[i].join()

#验证http
def start_validate_http(url,ip_page_count=1):
    validate( url,ip_page_count)

#验证https
def start_validate_https(url,ip_page_count=1):
    validate( url,ip_page_count,1)


#开始验证调用
#start_validate_https('https://detail.1688.com/offer/540424293523.html',5)

#从txt 获取ip列表
def get_data_from_file():
    data = []
    root_path = os.path.abspath('.')
    print('进入到了 proxy_ip 模块 Root Path===========================')
    print(root_path)
    f = open(root_path+'/files/ip_https.txt')
    for line in f.readlines():
        data.append(line)
    return data

#print(get_data_from_file())


root_path = os.path.abspath('.')
# print('Root Path===========================')
# print(root_path)