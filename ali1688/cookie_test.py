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
LOGIN_URL = 'https://login.taobao.com/member/login.jhtml?style=b2b&amp;css_style=b2b&amp;from=b2b&amp;newMini2=true&amp;full_redirect=true&amp;redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253Dhttps%25253A%25252F%25252Fsec.1688.com%25252Fquery.htm%25253Faction%25253DQueryAction%252526event_submit_do_login%25253Dok%252526smApp%25253Dlaputa%252526smPolicy%25253Dlaputa-detail_1688_com_page-anti_Spider-html-checklogin%252526smCharset%25253DGBK%252526smTag%25253DMTY0LjUyLjEyLjYwLCwwYmI3NTZhZTQ5ZTQ0MzFiOTJlM2Y2MTAzZDMxOTc4Ng%2525253D%2525253D%252526smReturn%25253Dhttps%2525253A%2525252F%2525252Fdetail.1688.com%2525252Foffer%2525252F540424293523.html%252526smSign%25253Dfm5KGuL84uX%2525252BXLVOYC4V9Q%2525253D%2525253D&amp;reg=http%3A%2F%2Fmember.1688.com%2Fmember%2Fjoin%2Fenterprise_join.htm%3Flead%3Dhttps%253A%252F%252Fsec.1688.com%252Fquery.htm%253Faction%253DQueryAction%2526event_submit_do_login%253Dok%2526smApp%253Dlaputa%2526smPolicy%253Dlaputa-detail_1688_com_page-anti_Spider-html-checklogin%2526smCharset%253DGBK%2526smTag%253DMTY0LjUyLjEyLjYwLCwwYmI3NTZhZTQ5ZTQ0MzFiOTJlM2Y2MTAzZDMxOTc4Ng%25253D%25253D%2526smReturn%253Dhttps%25253A%25252F%25252Fdetail.1688.com%25252Foffer%25252F540424293523.html%2526smSign%253Dfm5KGuL84uX%25252BXLVOYC4V9Q%25253D%25253D%26leadUrl%3Dhttps%253A%252F%252Fsec.1688.com%252Fquery.htm%253Faction%253DQueryAction%2526event_submit_do_login%253Dok%2526smApp%253Dlaputa%2526smPolicy%253Dlaputa-detail_1688_com_page-anti_Spider-html-checklogin%2526smCharset%253DGBK%2526smTag%253DMTY0LjUyLjEyLjYwLCwwYmI3NTZhZTQ5ZTQ0MzFiOTJlM2Y2MTAzZDMxOTc4Ng%25253D%25253D%2526smReturn%253Dhttps%25253A%25252F%25252Fdetail.1688.com%25252Foffer%25252F540424293523.html%2526smSign%253Dfm5KGuL84uX%25252BXLVOYC4V9Q%25253D%25253D%26tracelog%3Dnotracelog_s_reg'
values = {'TPL_username':'miyaye3344@gmail.com','TPL_password':'5vjwLdf4'}
postdata = parse.urlencode(values).encode()
headers = {
            'User-Agent':ua.random  ,'Connection':'keep-alive'
           }

cookie_filename = 'files/cookie.txt'
cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
handler = request.HTTPCookieProcessor(cookie)
opener = request.build_opener(handler)

proxy_hander = request.ProxyHandler({'http': get_random_ip() })

opener.add_handler(proxy_hander)

try:
    req0 = request.Request(LOGIN_URL, postdata, headers)
    response = opener.open(req0)
    page = response.read().decode('gbk')
    print('=====================login page===========')
    print(page)
except error.URLError as e:
    print(e.errno,":",e.reason)

exit()

cookie.save( ignore_discard=True, ignore_expires=True ) # 保存cookie到cookie.txt中
print(cookie)

for item in cookie:
    print('Name = ' + item.name)
    print('Value = ' + item.value)

soup = BeautifulSoup(page,'html.parser')
imgurl = soup.select('#checkcodeImg')
imgurl = 'https:'+imgurl[0].attrs['src']
print(imgurl)

print('=======================开始详情页咯。。。')
if imgurl is not None:
    mysession = requests.Session()
    checkcode = mysession.get(imgurl,timeout=60*4)

    with open('checkcode.png','wb') as f:
        f.write(checkcode.content)

    picture = Image.open('checkcode.png')
    action = 'https://sec.1688.com/query.htm'
    params = {}
    params["captcha"]=pytesseract.image_to_string(picture)
    #验证码验证请求
    response=opener.open(action, parse.urlencode(params).encode('utf-8'))

    try:
        #请求详情页
        headers_detail = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'User-Agent': ua.random,
            'Connection': 'keep-alive',
            'Referer': 'https://shop1440003101082.1688.com/page/offerlist.htm'
        }

        get_url = 'https://detail.1688.com/offer/552059954042.html'  # 利用cookie请求訪问还有一个网址
        get_request = request.Request(get_url, None, headers=headers_detail)
        get_response = opener.open(get_request)
        response_detail = get_response.read()
        print( response_detail )
    except error.URLError as e:
        print(e.errno, ":", e.reason)
