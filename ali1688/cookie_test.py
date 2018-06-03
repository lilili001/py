import random
import re
from urllib import request,parse,error
import http.cookiejar

import requests
from fake_useragent import UserAgent

from ali1688.helper import get_proxy
from ali1688.proxy_ip import get_data_from_file
from bs4 import BeautifulSoup

from PIL import Image
import pytesseract
from selenium import webdriver


def get_random_ip():
    ips=get_data_from_file()
    return random.choice(ips)

ua = UserAgent()
LOGIN_URL = 'https://login.taobao.com/member/login.jhtml'
values = {
    'TPL_username':'miyaye3344@gmail.com',
    'TPL_password':'5vjwLdf4',
    'TPL_password_2':'',
     '':'9a39c3fefeadf3d194850ef3a1d707dfa7bec0609a60bfcc7fe4ce2c615908b9599c8911e800aff684f804413324dc6d9f982f437e95ad60327d221a00a2575324263477e4f6a15e3b56a315e0434266e092b2dd5a496d109cb15875256c73a2f0237c5332de28388693c643c8764f137e28e8220437f05b7659f58c4df94685',
    'TPL_checkcode':'',
    'CtrlVersion': '1,0,0,7',
    'TPL_redirect_url':'',
    'allp' : '',
    'callback':'',
    'css_style':'',
    'fc':'default',
    'from':'tb',
    'from_encoding':'',
    'full_redirect':'',
    'guf':'',
    'gvfdcname':'',
    'gvfdcre':'',
    'isIgnore':'',
    'loginASR':'1',
    'loginASRSuc':'0',
    'loginType':'3',
    'loginsite':'3',
    'minipara':'',
    'minititle':'',
    'naviVer':'',
    'ncoSessionid':'',
    'ncoSig':'',
    'ncoToken':"44aff0190a0f2de81d924e135059cbb688d2b5ef",
    'need_sign':'',
    'need_user_id':'',
    'newlogin':'',
    'not_duplite_str':'',
    'osVer':'',
    'oslanguage':'',
    'popid':'',
    'poy':'',
    'pstrong':'',
    'sign':'',
    'slideCodeShow':'false',
    'sr':'',
    'style':'b2b',
    'sub':'',
    'um_token':'HV01PAAZ0b8bda7674e3dda45b129fac00af69bc'
}
postdata = parse.urlencode(values).encode('utf-8')
headers = {
            'User-Agent':ua.random  ,
            'Connection':'keep-alive'
           }

cookie_filename = 'files/cookie.txt'
cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
handler = request.HTTPCookieProcessor(cookie)
opener = request.build_opener(handler)
opener.add_handler(request.ProxyHandler({'http': get_proxy() }))
cookie.save( ignore_discard=True, ignore_expires=True ) # 保存cookie到cookie.txt中


try:
    req0 = request.Request(LOGIN_URL, postdata, headers)
    response = opener.open(req0)
    page = response.read().decode('gbk')
    print('=====================login page===========')
    print(page)

    for item in cookie:
        print('Name = ' + item.name)
        print('Value = ' + item.value)

    #exit()
    headers={
        'User-Agent': ua.random
    }


    content=requests.get('https://detail.1688.com/offer/563993845735.html', proxies={"http": get_proxy()},
                         headers=headers).content
    content=content.decode('gbk')
    print(content)

    soup=BeautifulSoup(page, 'html.parser')
    imgurl=soup.select('#checkcodeImg')

    print(imgurl)

    if imgurl is not None and len( imgurl ) > 0:
        imgurl='https:' + imgurl[0].attrs['src']
        print(imgurl)

        print('=======================开始详情页咯。。。')
        if imgurl is not None:
            mysession=requests.Session()
            checkcode=mysession.get(imgurl, timeout=60 * 4)

            with open('checkcode.png', 'wb') as f:
                f.write(checkcode.content)

            picture=Image.open('checkcode.png')
            action='https://sec.1688.com/query.htm'
            params={}
            params["captcha"]=pytesseract.image_to_string(picture)
            # 验证码验证请求
            response=opener.open(action, parse.urlencode(params).encode('utf-8'))

            try:
                # 请求详情页
                headers_detail={
                    'Accept': '*/*',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Cache-Control': 'max-age=0',
                    'User-Agent': ua.random,
                    'Connection': 'keep-alive',

                }

                get_url='https://detail.1688.com/offer/552059954042.html'  # 利用cookie请求訪问还有一个网址
                get_request=request.Request(get_url, None, headers=headers_detail )
                get_response=opener.open(get_request)
                response_detail=get_response.read()
                print(response_detail)
            except error.URLError as e:
                print(e.errno, ":", e.reason)

except error.URLError as e:
    print(e.errno,":",e.reason)




