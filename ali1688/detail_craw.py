# coding=utf-8

import datetime
import json
import re
import socket
import time
from urllib.request import urlretrieve

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from urllib import error, request
import os
import csv

from ali1688.helper import str_replace_new

root_path = os.path.abspath('.')
ua = UserAgent()

################################################################################################################
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

# your spider code

# csvfile = open(root_path + '/files/data.csv', 'w', newline='')
# writer = csv.writer(csvfile)
# writer.writerow(('title', 'price', 'filedir' ,'supplier' , 'colors' , 'sizes' , 'delivery-addr' ))

def getHtml(detail_page_url ,writer , spidername ):

    retry_count = 5

    proxy = get_proxy()
    #proxy = '124.230.66.109:13641'
    print('[proxy]{}=====' ,proxy)
    headers = {
        'User-Agent': ua.random
    }
    try:
        print('======start detail craw %s======================\n' % (retry_count) )
        #html = requests.get(detail_page_url, proxies={"http":"http://{}".format(proxy) } ,headers=headers )
        #html = requests.get(detail_page_url, headers=headers )

        proxy_handler = request.ProxyHandler({"http": "http://{}".format(proxy)})
        opener = request.build_opener(proxy_handler)
        req = request.Request(detail_page_url)
        req.add_header('User-Agent', ua.random)
        r = opener.open(req)
        content = r.read().decode()
        r.close()

        #content = html.text

        print(content)

        #filename = time.strftime("%Y%m%d-%H%M%S", time.localtime())

        reg =  re.compile(r'(\d*).html')
        pattern = re.compile(reg)
        out = re.findall(pattern, detail_page_url)

        filename = out[0]

        # 将数据写入csv
        soup = BeautifulSoup(content,'html.parser')
        if soup.find('input',id="login-home-new") !=None:
            print('本次要求登陆！')
            raise Exception('肯定报错啦')
            exit()
        parse_detail(content,filename, detail_page_url, writer)
        #get_main_pics(content, filename ,spidername )
        #get_description_pics(content,filename ,spidername )



        # 使用代理访问
        return content
    except error.URLError as e:
        print('===========error====================\n')

        err_file = open('error_list','w')
        err_file.write( detail_page_url+'\n' )
        print(e)
        print(e.errno, ":", e.reason)

        retry_count -= 1
    # 出错5次, 删除代理池中代理
    print(retry_count)
    delete_proxy(proxy)
    return None

def parse_detail(content , filename=None ,detail_page_url=None ,writer=None ):
    #content = open(root_path+'/ali1688/files/detail.txt' ,encoding='utf-8' ).read()

    soup = BeautifulSoup(content, 'html.parser' )
    res = {}

    # title
    title_node=soup.find('h1', class_="product-name")
    res['title']=title_node.get_text()

    # price
    price_node=soup.find('span', class_='p-price')
    res['price']=price_node.get_text()
    if soup.find('span', itemprop="highPrice") == None:
        res['price']=price_node.get_text()

    # colors
    res['colors'] = []
    img_lis=soup.find_all('li', class_="item-sku-image")
    for color_li in img_lis:
        color=color_li.find('a')
        print('(color 来了)====================')
        bigpic = color.find('img').attrs['bigpic']

        d = {"color":color.attrs['title'],"pic":bigpic}
        res['colors'].append(d)
    #res['colors']=','.join(res['colors'])

    print('[colors]==============')
    print(res['colors'])

    # sizes
    res['sizes'] = []
    size_spans=soup.find('ul', id="j-sku-list-2").find_all('span')
    for size_span in size_spans:
        size=size_span.get_text()
        res['sizes'].append(size)
    #res['sizes']=','.join(res['sizes'])

    # sizechart
    pattern=re.compile(r'"sizeAttr":{(.*?)}')
    sizechart=pattern.findall(content)
    res['sizechart'] = sizechart

    # images
    img_pattern=re.compile(r'window.runParams.imageBigViewURL=[(.*?)]')
    res['images']=img_pattern.findall(content)
    print(res['images'])

    # specifications
    res['specs'] = []
    property_items=soup.find('ul', class_='product-property-list').find_all('li')
    for property_item in property_items:
        d={"title": '', "value": ''}
        d['title']=property_item.find('span', class_="propery-title").get_text()
        d['value']=property_item.find('span', class_="propery-des").get_text()
        res['specs'].append(d)

    # supplier
    res['supplier'] = ''
    supplier=soup.find('a', class_="store-lnk")
    print('(supplier 来咯============)')
    print(supplier)
    if supplier != None:
        res['supplier']={"store": supplier.get_text(), "store_link": supplier.attrs['href']}

    # store address
    res['supplier_address'] = ''
    if soup.find('dd', class_="store-address") != None:
        res["supplier_address"]=soup.find('dd', class_="store-address").get_text()

    # page id
    res['supplier_detail_id'] = filename
    res['detail_page_url'] = detail_page_url
    writer.writerow((
                     res['title'],
                     res['price'],
                     res['colors'] ,
                     res['sizes'] ,
                     res['sizechart'],
                     res['images'],
                     res['specs'],
                     res['supplier'],
                     res['supplier_address'],
                     res['supplier_detail_id'],
                     res['detail_page_url']
     ))

    print(res)
    return res

#通过正则获取图片
def getImg(html):
    reg = r'src="(.*?\.jpg)" alt'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    return imglist

#获取详情页主图图片
def get_main_pics(html,filename,spidername):

    soup = BeautifulSoup(html, 'html.parser' )
    lis = soup.find('div',id='dt-tab').find_all('li',class_='tab-trigger')

    print('======主图列表====================\n')
    print( '主图数量 %s' % len( lis ) )
    #创建商品图片文件目录 以及详情图片文件夹

    if os.path.exists( root_path+'/%s/%s/400' % ( spidername ,filename ) ) == False:
        os.makedirs(root_path+'/%s/%s/400' % ( spidername ,filename ) )

    if os.path.exists(root_path + '/%s/%s/800' % (spidername, filename)) == False:
        os.makedirs(root_path+'/%s/%s/800' % ( spidername ,filename ))

    count = 0
    for li in lis:
        count = count+1
        json_obj = json.loads( li.attrs['data-imgs'] )
        preview_url = json_obj['preview']
        original_url = json_obj['original']

        # if  os.path.isfile(root_path+'/%s/%s/400/%s.jpg' % ( spidername, filename,count)) == False:
        #     urlretrieve(preview_url, root_path+'/%s/%s/400/%s.jpg' % ( spidername, filename,count))

        if os.path.isfile(root_path + '/%s/%s/800/%s.jpg' % (spidername, filename, count)) == False:
            urlretrieve(original_url, root_path+'/%s/%s/800/%s.jpg' % ( spidername,filename,count))


# 获取详情页描述的所有图片
def get_description_pics(html,filename, spidername):

    headers = {
        'User-Agent': ua.random
    }
    soup = BeautifulSoup(html,'html.parser' )
    imgs = soup.find('div',id='desc-lazyload-container')
    url_imgs = imgs.attrs['data-tfs-url']
    #详情页url
    print(imgs.attrs['data-tfs-url'])

    retry_count = 3

    #proxy = get_proxy()
    try:
        print('========try=================================================')
        #content = requests.get(url_imgs, proxies={"http": proxy } ,headers=headers ).content
        content = requests.get(url_imgs,  headers=headers ).content
        print('========detail content=====================================================')
        print(content)
        # content = open( root_path+'/ali1688/files/detail_pics.txt' , 'rb' ).read()
        content = content.decode('gbk')
        content = content.split('var offer_details=')[1]

        soup = BeautifulSoup(content, 'html.parser')
        imgList = soup.find_all('img', src=re.compile(r'jpg'))

        temp = []
        for img in imgList:
            url = img.attrs['src'].replace('\\', '')
            url = url.replace('\"', '')
            temp.append(url)

        print('========img list=====================================================')
        print(temp)

        os.makedirs(root_path+'/%s/%s/detail' % (spidername,filename))
        i = 0
        for detail_img in temp:
            i = i + 1
            if os.path.isfile(root_path+'/%s/%s/detail/%s.jpg' % ( spidername,filename, i)) == False:
                urlretrieve(detail_img, root_path+'/%s/%s/detail/%s.jpg' % ( spidername,filename, i))

        print('=====详情图片列表===================================\n')
        print(imgList)
        return imgList
    except error.URLError as e:
        print('===========error====================\n')
        err_file = open('error_list', 'w')
        err_file.write(imgs.attrs['data-tfs-url'] + '\n')
        print(e.errno, ":", e.reason , " url:" , imgs.attrs['data-tfs-url'] )
        retry_count -= 1

    #delete_proxy(proxy)
    return None

#getHtml()