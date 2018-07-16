import json
import time
from urllib.request import urlretrieve

import requests
from bs4 import BeautifulSoup
import re
import os
from fake_useragent import UserAgent
from urllib import error, request
ua = UserAgent()
root_path = os.path.abspath('.')
headers={
            'User-Agent': ua.random
        }

def get_main_pics( detail_page_url ,spidername):
    html=requests.get(detail_page_url, headers=headers)
    html=html.text
    print(html)
    soup = BeautifulSoup(html, 'html.parser' )
    lis = soup.find('div',id='dt-tab').find_all('li',class_='tab-trigger')

    print('======主图列表====================\n')
    print( '主图数量 %s' % len( lis ) )
    #创建商品图片文件目录 以及详情图片文件夹

    reg=r'offer/(.*?).html'
    pattern=re.compile(reg)
    out=re.findall(pattern, detail_page_url)
    filename=time.strftime("%Y%m%d-%H%M%S", time.localtime()) +'-'+ out[0]

    if os.path.exists(root_path + '/%s/%s/800' % (spidername, filename)) == False:
        os.makedirs(root_path+'/%s/%s/800' % ( spidername ,filename ))

    count = 0
    for li in lis:
        count = count+1
        json_obj = json.loads( li.attrs['data-imgs'] )
        preview_url = json_obj['preview']
        original_url = json_obj['original']

        if os.path.isfile(root_path + '/%s/%s/800/%s.jpg' % (spidername, filename, count)) == False:
            urlretrieve(original_url, root_path+'/%s/%s/800/%s.jpg' % ( spidername,filename,count))

def download(url_imgs , filename, spidername ):
    try:
        print('========try=================================================')
        # content = requests.get(url_imgs, proxies={"http": proxy } ,headers=headers ).content

        content=requests.get(url_imgs, headers=headers).content
        print('========detail content=====================================================')
        print(content)
        # content = open( root_path+'/ali1688/files/detail_pics.txt' , 'rb' ).read()
        content=content.decode('gbk')
        content=content.split('var offer_details=')[1]

        soup=BeautifulSoup(content, 'html.parser')
        imgList=soup.find_all('img', src=re.compile(r'jpg'))

        temp=[]
        for img in imgList:
            url=img.attrs['src'].replace('\\', '')
            url=url.replace('\"', '')
            temp.append(url)

        print('========img list=====================================================')
        print(temp)


        os.makedirs(root_path + '/%s/%s/detail' % (spidername, filename))
        i=0
        for detail_img in temp:
            i=i + 1
            if os.path.isfile(root_path + '/%s/%s/detail/%s.jpg' % (spidername, filename, i)) == False:
                urlretrieve(detail_img, root_path + '/%s/%s/detail/%s.jpg' % (spidername, filename, i))

        print('=====详情图片列表===================================\n')
        print(imgList)
        return imgList
    except error.URLError as e:
        print('===========error====================\n')
        err_file=open('error_list', 'w')
        print(e.errno, ":", e.reason)


# img_url = ''
# filename = ''
# download( img_url , filename, 'mens_clothes'  )

get_main_pics(   'https://detail.1688.com/offer/565798857434.html' , 'mens_clothes' )