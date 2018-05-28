import datetime
import json
import re
import time
from urllib.request import urlretrieve

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from urllib import error
import os

root_path = os.path.abspath('.')

class People(object):
    color = 'yellow'

    def __init__(self,c):
        print("Init..."+c)
        self.dwell='Earth'

    def think(self):
        self.color = "black"
        print("I am a %s " % self.color)
        print("I am a thinker")

class Chinese(People):
    def __init__(self):
        People.__init__(self,'red')
    pass


if __name__ =="__main__":
    #cn = Chinese()
    # print(cn.dwell)
    # cn.think()

    ua = UserAgent()

# your spider code

def getHtml():
    # ....

    headers = {
               'User-Agent': ua.random
               }
    retry_count = 5


    while retry_count > 0:
        try:
            print('======start detail craw %s======================\n' % (retry_count) )
            html = requests.get('https://detail.1688.com/offer/540424293523.html', proxies={"http": "60.176.235.132:6666" } ,headers=headers )
            print('===========content below====================\n')

            print(html.text)

            f = open(root_path+'/ali1688/files/detail.txt','w',encoding="utf-8")
            f.write(html.text )
            f.close()

            # 使用代理访问
            return html
        except error.URLError as e:
            print('===========error====================\n')
            print(e.errno, ":", e.reason)

            retry_count -= 1
    # 出错5次, 删除代理池中代理
    print(retry_count)

    return None

#getHtml()



def parse_detail():
    content = open(root_path+'/ali1688/files/detail.txt' ,encoding='utf-8' ).read()

    soup = BeautifulSoup(content, 'html.parser' )
    res = {}

    # title
    title_node = soup.find('h1', class_="d-title")
    res['title'] = title_node.get_text()


    # price
    price_node = soup.find('table',class_='table-sku').find('td',class_='price').find('em',class_='value')
    res['price'] = price_node.get_text()


    # specifications

#通过正则获取图片
def getImg(html):
    reg = r'src="(.*?\.jpg)" alt'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    return imglist
#循环把图片存到本地

    # x = 0
    # for imgurl in imglist:
    #     #保存到本地
    #     urllib.urlretrieve(imgurl,'/Applications/MAMP/image/%s.jpg' % x)
    #     x+=1

#parse_detail()

content = open(root_path+'/ali1688/files/detail.txt' ,encoding='utf-8' ).read()
# print( getImg(content) )

imgurl = 'https://cbu01.alicdn.com/img/ibank/2016/261/233/3561332162_838608928.32x32.jpg'

#print( re.search('32x32\.jpg',imgurl) )

#获取详情页主图图片
def get_main_pics(html):
    soup = BeautifulSoup(html, 'html.parser' )
    lis = soup.find('div',id='dt-tab').find_all('li',class_='tab-trigger')

    #创建商品图片文件目录
    filename = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    os.makedirs('F:/laragon/www/python/image/%s/400' % filename)
    os.makedirs('F:/laragon/www/python/image/%s/800' % filename)

    count = 1
    for li in lis:
        count = count+1
        json_obj = json.loads( li.attrs['data-imgs'] )
        preview_url = json_obj['preview']
        original_url = json_obj['original']

        urlretrieve(preview_url, 'F:/laragon/www/python/image/%s/400/%s.jpg' % (filename,count))
        urlretrieve(original_url, 'F:/laragon/www/python/image/%s/800/%s.jpg' % (filename,count))

# 获取详情页描述的所有图片
def get_description_pics(html):
    headers = {
        'User-Agent': ua.random
    }
    soup = BeautifulSoup(html,'html.parser')
    imgs = soup.find('div',id='desc-lazyload-container')
    print(imgs.attrs['data-tfs-url'])

    content = requests.get(imgs.attrs['data-tfs-url'], proxies={"http": "60.176.235.132:6666" } ,headers=headers ).content
    print(content)

    # imgs = content.content.find_all('img')
    # print(imgs)

#获取主图图片方法调用
#get_main_pics(content)

#获取描述图片方法调用
get_description_pics(content)

