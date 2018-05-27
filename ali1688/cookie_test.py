import random
import re
from urllib import request,parse,error
import http.cookiejar

import requests
from fake_useragent import UserAgent

from ali1688.proxy_ip import get_data_from_file
from bs4 import BeautifulSoup

from PIL import Image
import pytesseract


def get_random_ip():
    ips=get_data_from_file()
    return random.choice(ips)

ua = UserAgent()
LOGIN_URL = 'https://login.taobao.com/member/login.jhtml?style=b2b&css_style=b2b&from=b2b&newMini2=true&full_redirect=true&redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253Dhttp%25253A%25252F%25252Fmember.1688.com%25252Fmember%25252Foperations%25252Fmember_operations_jump_engine.htm%25253Ftracelog%25253Dlogin%252526operSceneId%25253Dafter_pass_from_taobao_new%252526defaultTarget%25253Dhttp%2525253A%2525252F%2525252Fwork.1688.com%2525252F%2525253Ftracelog%2525253Dlogin_target_is_blank_1688&reg=http%3A%2F%2Fmember.1688.com%2Fmember%2Fjoin%2Fenterprise_join.htm%3Flead%3Dhttp%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252Fmember_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253Dafter_pass_from_taobao_new%2526defaultTarget%253Dhttp%25253A%25252F%25252Fwork.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688%26leadUrl%3Dhttp%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252Fmember_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253Dafter_pass_from_taobao_new%2526defaultTarget%253Dhttp%25253A%25252F%25252Fwork.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688%26tracelog%3Daccount_verify_s_reg'
values = {'TPL_username':'miyaye3344@gmail.com','TPL_password':'5vjwLdf4'}
postdata = parse.urlencode(values).encode()
headers = {'User-Agent':ua.random  ,'Connection':'keep-alive'}

cookie_filename = 'files/cookie.txt'
cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
handler = request.HTTPCookieProcessor(cookie)
opener = request.build_opener(handler)

proxy_hander = request.ProxyHandler({'http': get_random_ip() })

opener.add_handler(proxy_hander)

req0 = request.Request(LOGIN_URL,postdata,headers)

try:
    response = opener.open(req0)
    page = response.read()
    print('=====================login page===========')
    print(page)
except error.URLError as e:
    print(e.errno,":",e.reason)

cookie.save( ignore_discard=True, ignore_expires=True ) # 保存cookie到cookie.txt中
print(cookie)

for item in cookie:
    print('Name = ' + item.name)
    print('Value = ' + item.value)

print('=======================开始详情页咯。。。')
get_url = 'https://detail.1688.com/offer/540424293523.html'  # 利用cookie请求訪问还有一个网址
get_request = request.Request(get_url, headers=headers)
get_response = opener.open(get_request)

html = get_response.read()

mysession = requests.Session()

soup = BeautifulSoup(html,'html.parser')
imgurl = soup.select('#checkcodeImg')

imgurl = 'https:'+imgurl[0].attrs['src']
print(imgurl)

checkcode = mysession.get(imgurl,timeout=60*4)

with open('checkcode.png','wb') as f:
    f.write(checkcode.content)

picture = Image.open('checkcode.png')
action = 'https://sec.1688.com/query.htm'
params = {}
params["captcha"]=pytesseract.image_to_string(picture)

response=opener.open(action, parse.urlencode(params).encode('utf-8'))
print( response )
