# coding=utf-8

import datetime
import json
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

def getHtml(detail_page_url ,writer ):

    headers = {'User-Agent': ua.random}
    retry_count = 3

    proxy = get_proxy()

    try:
        print('======start detail craw %s======================\n' % (retry_count) )
        html = requests.get(detail_page_url, proxies={"http":"http://{}".format(proxy) } ,headers=headers )

        content = html.text

        #print(content)

        #filename = time.strftime("%Y%m%d-%H%M%S", time.localtime())

        reg = r'offer/(.*?).html'
        pattern = re.compile(reg)
        out = re.findall(pattern, detail_page_url)
        filename = out[0]

        # 将数据写入csv

        parse_detail( content,filename, detail_page_url , writer )
        get_main_pics(content, filename)
        get_description_pics(content,filename)

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

def parse_detail(content=None , filename=None ,detail_page_url=None ,writer=None ):
    #content = open(root_path+'/ali1688/files/detail.txt' ,encoding='utf-8' ).read()

    soup = BeautifulSoup(content, 'html.parser' )
    res = {}

    # title
    title_node = soup.find('h1', class_="d-title")
    print(title_node)
    if ( title_node is not None and  len(title_node) != 0):
        res['title'] = str_replace_new(title_node.get_text())

    # price
    price_node = soup.find('table',class_='table-sku').find('td',class_='price').find('em',class_='value')
    if( price_node is not None and len(price_node)!=0 ):
        res['price'] = price_node.get_text()
    else:
        price_node = soup.find('div',class_='price-discount-sku').find('span',class_='value')
        if( price_node is not None and len(price_node)!=0):
            res['price'] = price_node.get_text()
        else:
            res['price'] = 'null'
    #supplier
    supplier_node = soup.find('a',class_='company-name')
    res['supplier'] =  supplier_node.get_text()

    #shipping district
    res['delivery-addr'] = soup.find('span',class_='delivery-addr').get_text()

    #规格
    res['colors'] = []
    color_nodes = soup.find_all('div',class_='unit-detail-spec-operator')
    for div in color_nodes:
        color = json.loads( div.attrs['data-unit-config'] )['name']
        res['colors'].append( color  )
    res['colors'] = ','.join( res['colors'] )

    res['sizes'] = []
    size_nodes = soup.find('table', class_='table-sku').find_all('td', class_='name')
    for td in size_nodes:
        size_span = td.find('span')
        if( len(size_span) != 0 ):
            res['sizes'].append( size_span.get_text() )

    res['sizes'] = ','.join(res['sizes'])

    writer.writerow((
                     res['title'],
                     res['price'],
                     filename ,
                     res['supplier'] ,
                     res['colors'] ,
                     res['sizes'] ,
                     res['delivery-addr'],
                     detail_page_url,
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
def get_main_pics(html,filename):
    soup = BeautifulSoup(html, 'html.parser' )
    lis = soup.find('div',id='dt-tab').find_all('li',class_='tab-trigger')

    print('======主图列表====================\n')
    print( '主图数量 %s' % len( lis ) )
    #创建商品图片文件目录 以及详情图片文件夹

    os.makedirs(root_path+'/image/%s/400' % filename)
    os.makedirs(root_path+'/image/%s/800' % filename)

    count = 0
    for li in lis:
        count = count+1
        json_obj = json.loads( li.attrs['data-imgs'] )
        preview_url = json_obj['preview']
        original_url = json_obj['original']

        urlretrieve(preview_url, root_path+'/image/%s/400/%s.jpg' % (filename,count))
        urlretrieve(original_url, root_path+'/image/%s/800/%s.jpg' % (filename,count))


# 获取详情页描述的所有图片
def get_description_pics(html,filename):
    headers = {
        'User-Agent': ua.random
    }
    soup = BeautifulSoup(html,'html.parser' )
    imgs = soup.find('div',id='desc-lazyload-container')
    url_imgs = imgs.attrs['data-tfs-url']
    #详情页url
    print(imgs.attrs['data-tfs-url'])

    retry_count = 3

    proxy = get_proxy()
    try:
        print('========try=================================================')
        content = requests.get(url_imgs, proxies={"http": proxy } ,headers=headers ).content
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

        os.makedirs(root_path+'/image/%s/detail' % filename)
        i = 0
        for detail_img in temp:
            i = i + 1
            urlretrieve(detail_img, root_path+'/image/%s/detail/%s.jpg' % (filename, i))

        print('=====详情图片列表===================================\n')
        print(imgList)
        return imgList
    except error.URLError as e:
        print('===========error====================\n')
        err_file = open('error_list', 'w')
        err_file.write(imgs.attrs['data-tfs-url'] + '\n')
        print(e.errno, ":", e.reason , " url:" , imgs.attrs['data-tfs-url'] )
        retry_count -= 1

    delete_proxy(proxy)
    return None

#getHtml()