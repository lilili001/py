import datetime
import json
import math
import re
import time
from urllib.request import urlretrieve

import demjson
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from urllib import error
import os

import csv

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

################################################################################################################
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

# your spider code

# csvfile = open(root_path + '/ali1688/files/data.csv', 'w', newline='')
# writer = csv.writer(csvfile)
# writer.writerow(('title', 'price', 'filedir' ,'supplier' , 'colors' , 'sizes' , 'delivery-addr' ))

def getHtml():

    headers = {'User-Agent': ua.random}
    retry_count = 5

    while retry_count > 0:
        try:
            print('======start detail craw %s======================\n' % (retry_count) )
            html = requests.get('https://detail.1688.com/offer/540424293523.html', proxies={"http":"http://{}".format(proxy) } ,headers=headers )
            content = html.text
            print('===========content below====================\n')

            #content = open(root_path + '/ali1688/files/detail.txt', encoding='utf-8').read()

            #print(html.text)

            # f = open(root_path+'/ali1688/files/detail.txt','w',encoding="utf-8")
            # f.write(html.text )
            # f.close()

            filename = time.strftime("%Y%m%d-%H%M%S", time.localtime())

            # 将数据写入csv

            parse_detail(content,filename)
            get_main_pics(content, filename)
            get_description_pics(content,filename)

            # 使用代理访问
            return content
        except error.URLError as e:
            print('===========error====================\n')
            print(e.errno, ":", e.reason)

            retry_count -= 1
    # 出错5次, 删除代理池中代理
    print(retry_count)
    delete_proxy(proxy)
    return None

def parse_detail(content=None , filename=None ):
    #content = open(root_path+'/ali1688/files/detail.txt' ,encoding='utf-8' ).read()

    soup = BeautifulSoup(content, 'html.parser' )
    res = {}

    # title
    title_node = soup.find('h1', class_="d-title")
    res['title'] = title_node.get_text()

    # price
    price_node = soup.find('table',class_='table-sku').find('td',class_='price').find('em',class_='value')
    res['price'] = price_node.get_text()

    #supplier
    supplier_node = soup.find('a',class_='company-name')
    res['supplier'] = supplier_node.get_text()

    #product_url
    #res['supplier_item_url'] = url

    #shipping district
    res['delivery-addr'] = soup.find('span',class_='delivery-addr').get_text()

    #规格
    res['colors'] = []
    color_nodes = soup.find_all('div',class_='unit-detail-spec-operator')
    for div in color_nodes:
        img_a = div.find('a',class_='image')
        res['colors'].append( img_a.attrs['title']  )
    res['colors'] = ','.join( res['colors'] )

    res['sizes'] = []
    size_nodes = soup.find('table', class_='table-sku').find_all('td', class_='name')
    for td in size_nodes:
        size_span = td.find('span')
        res['sizes'].append( size_span.get_text() )

    res['sizes'] = ','.join(res['sizes'])

    writer.writerow((res['title'], res['price'], filename , res['supplier'] ,  res['colors'] , res['sizes'] , res['delivery-addr']  ))

    print(res)
    return res

#通过正则获取图片
def getImg(html):
    reg = r'src="(.*?\.jpg)" alt'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    return imglist

#获取详情页主图图片
def get_main_pics(html,filename):
    soup = BeautifulSoup(html, 'html.parser' )
    lis = soup.find('div',id='dt-tab').find_all('li',class_='tab-trigger')

    print('======主图列表====================\n')
    print(lis)
    #创建商品图片文件目录 以及详情图片文件夹

    os.makedirs('F:/laragon/www/python/image/%s/400' % filename)
    os.makedirs('F:/laragon/www/python/image/%s/800' % filename)

    count = 0
    for li in lis:
        count = count+1
        json_obj = json.loads( li.attrs['data-imgs'] )
        preview_url = json_obj['preview']
        original_url = json_obj['original']

        urlretrieve(preview_url, 'F:/laragon/www/python/image/%s/400/%s.jpg' % (filename,count))
        urlretrieve(original_url, 'F:/laragon/www/python/image/%s/800/%s.jpg' % (filename,count))


# 获取详情页描述的所有图片
def get_description_pics(html,filename):
    headers = {
        'User-Agent': ua.random
    }
    soup = BeautifulSoup(html,'html.parser')
    imgs = soup.find('div',id='desc-lazyload-container')

    #详情页url
    print(imgs.attrs['data-tfs-url'])
    content = requests.get(imgs.attrs['data-tfs-url'], proxies={"http": proxy } ,headers=headers ).content

    #content = open( root_path+'/ali1688/files/detail_pics.txt' , 'rb' ).read()
    content = content.decode('gbk')
    content = content.split('var offer_details=')[1]
    reg = r'(https.*?\.jpg)'
    image = re.compile(reg)
    imgList = re.findall(image, content)

    os.makedirs('F:/laragon/www/python/image/%s/detail' % filename)
    i = 0
    for detail_img in imgList:
        i = i + 1
        urlretrieve(detail_img, 'F:/laragon/www/python/image/%s/detail/%s.jpg' % (filename, i))

    print('=====详情图片列表===================================\n')
    print(imgList)
    return imgList

proxy = get_proxy()
# getHtml()

# headers = {
#         'User-Agent': ua.random
#     }
# content = requests.get('https://img.alicdn.com/tfscom/TB1K0fbkN9YBuNjy0FfXXXIsVXa', proxies={"http": proxy } ,headers=headers ).content
# content = content.decode('gbk')
#
# soup = BeautifulSoup(content,'html.parser')
# imgList = soup.find_all('img',src=re.compile(r'jpg'))
#
# temp = []
# for img in imgList:
#     url = img.attrs['src'].replace('\\','')
#     url = url.replace('\"','')
#     temp.append(url)
#
# print(temp)

# str = '中华人名共和国'
#
# print( str.replace('中华' , '中国') )

# reg = r'https.*?\.jpg'
# image = re.compile(reg)
# imgList = re.findall(image, str)
# print(imgList)


def changeTime(allTime):
    day = 24*60*60
    hour = 60*60
    min = 60
    if allTime <60:
        return  "%d sec"%math.ceil(allTime)
    elif  allTime > day:
        days = divmod(allTime,day)
        return "%d days, %s"%(int(days[0]),changeTime(days[1]))
    elif allTime > hour:
        hours = divmod(allTime,hour)
        return '%d hours, %s'%(int(hours[0]),changeTime(hours[1]))
    else:
        mins = divmod(allTime,min)
        return "%d mins, %d sec"%(int(mins[0]),math.ceil(mins[1]))


# start = datetime.datetime.now()
# time.sleep(5)
# end = datetime.datetime.now()
# end2 = start + datetime.timedelta(hours=10.5)
#
# used_time = (end2-start)
# alltime = used_time.seconds
#
# str = "促销 女装背带性感伴娘晚礼服 交叉露背亮片Wish连衣裙"
# reg = r'[促销|wish]'
# pattern = re.compile(reg,re.IGNORECASE)
# out = re.sub(pattern , '',str )
# print(out) #女装背带性感伴娘晚礼服 交叉露背亮片连衣裙

f = open('test.csv','a',newline='')
writer = csv.writer(f)
writer.writerow(('name','age'))
f.close()

f1 = open('test.csv','a',newline='')
writer1 = csv.writer(f1)
writer1.writerow(('alice','12'))
f1.close()