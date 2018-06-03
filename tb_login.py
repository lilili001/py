import urllib
from urllib.parse import urlencode

import re
import webbrowser
from urllib.request import ProxyHandler, HTTPHandler, build_opener, install_opener, Request, urlopen

from selenium import webdriver
from http import cookiejar

#登录地址
from ali1688.helper import get_proxy
from fake_useragent import UserAgent


login_url = "https://login.taobao.com/member/login.jhtml"
proxy_url = get_proxy()
#post请求头部
headers = {
    'Host':'login.taobao.com',
    'User-Agent' : UserAgent().random,
    'Referer' : 'https://login.taobao.com/member/login.jhtml',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection' : 'Keep-Alive'
        }
#用户名，密码
username = input("请输入账号: ") #此处不需要密码，因为经过淘宝加密算法后，在下面的ua中已经包含了账号和密码，所以很安全
#所以每个用户的ua都是不一样的
#请求数据包,这三个都是动态生成的，但是不用担心，只要选取其中一组就可以，只要你的用户名和密码不变就可以
ua = '108%23Yq%2F%2F1%2FFl%2FYpRH0wWcbUwDWExOPijcLd8nA3JIfmdP3p%2FhLFH0dYaVqWeE7B%2F0jdA5Q9m9W1MJLFSvb1v1pcnht3Uz%2BwJ17spFHNdJwgqE%2FpFh%2FtqxHWpDx9pHLttvdQ9MQPEqvQiLtJqMmjFXMG39TLN7PhgYk1FUwk2UjgxJkiXCxSVJhXNY9VMoDxfa322TeTKPmcqerhU9ApkGYKohQ20XanrcLPyrw4nwLNPWMc6B2TVv%2FSv%2FmvDDwYQ8Mjvvu7G0J%2BWvctzCkvWX897RoD3MNapt1eM7SXZEPT2Jo5qq2BE%2Fjio7prdHG%2Fb%2Bf3zQc8PMaYw8ax5MQ5FTUebvmqqZyBRXXWGhIHIYIEhCmLGUX5k2xwi1g8ihrTEHLMiG5lcm3dnva0x1F3ZAF3bxo%2FzDg1DkbEHpq%2BefWkUzSdqblykfoMTIMuB5yOat6qaMnFQLunDs2lgcKHOQXEkFc17Yaupq0rhIyJqzwUtfiU%2FKZKMQWnuUyNHQBnMkTWP42%2FIMLxfKbwI%2F5nayOjZuVzfu2t4daSappYFafkc7rb91eiWbbOIpmb4huZvddtepzXrB6uptQc5nyHOynGu9QOMrX38wGCCGYFXb5C5H%2BdRJCb0TTa7kJAgcRirsVlRpJIkKTNciXtwbXyqeP7rQ7gnhWfp8KpAL%2FSuxaaDbtkJzKyDXUHR62WhNJp1ge8RdUlVD%2BOgG16DWs4hk%2Ff3jP1EqNDAduB7Iss81rawvCsqH%2BbN%2BIVmAP02h51BvjE3AIhkkbAtGhSHIWZbOkvjW4UjjFON4JmpRm6cRIunTgNGJY1wGTa5%2B%2FUKi2v7mIG5kw6gQF24F7lW1r3G%2FJJmAG9GAn9a%2FG89v5a5dGKOQMlro1LL5Pu31NydPdzYN3HFi%2Bai2aqx%2B98MGdCoO9vyVCAGJJxZ3WnvAKAmEtIzfcoCbQnid7AEU9y%2B6rB8ISS4mcrx5UzFqzXe9sO3jcBlMpdvel05dTP1K%2Fji75MLMH03lB2wJhFJNkBOnQqVhABsr2og0bcWn7cb4tgSF4trI0R0f5fErk%2B8zFVn7qbqARv%2FQOam%2B6kdLgO7d3dQTFT%2BYFwLPbKNhKNJzH2O36FAc5MP8%2B6%2F5SHN1kaCRtEZf86g2LdR82KsWUc1zKkl%2BPbyIw1skYglRePJ3tXtRpSI'#因为ua，gr,password2都太长了所以省略了很多
gr = '68747470733A2F2F6C6F67696E2E74616F62616F2E636F6D2F6D656D6265722F6C6F676F75742E6A68746D6C3F73706D3D61317A30322E312E3735343839343433372E372E35383464373832646B775673334926663D746F70266F75743D7472756526726564697265637455524C3D6874747073253341253246253246692E74616F62616F2E636F6D2532466D795F74616F62616F2E68746D'
password2 = ''


post = {   'ua':ua,
        'TPL_checkcode':'',
        'TPL_password':'5vjwLdf4',
        'TPL_redirect_url':'http://i.taobao.com/my_taobao.htm?nekot=udm8087E1424147022443',
        'TPL_username':username,
        'loginsite':'0',
        'newlogin':'0',
        'from':'tb',
        'fc':'default',
        'style':'default',
        'css_style':'',
        'tid':'',
        'loginType':'3',
        'minititle':'',
        'minipara':'',
        'umto':'NaN',
        'pstrong':'3',
        'llnick':'',
        'sign':'',
        'need_sign':'',
        'isIgnore':'',
        'full_redirect':'',
        'popid':'',
        'callback':'',
        'guf':'',
        'not_duplite_str':'',
        'need_user_id':'',
        'poy':'',
        'gvfdcname':'10',
        'gvfdcre':gr,
        'from_encoding	':'',
        'sub':'',
        'TPL_password_2':password2,
        'loginASR':'1',
        'loginASRSuc':'1',
        'allp':'',
        'oslanguage':'zh-CN',
        'sr':'1366*768',
        'osVer':'windows|6.1',
        'naviVer':'firefox|35'
        }
postData = urlencode(post).encode('utf-8')
proxy = ProxyHandler({'http':proxy_url})  #设置代理，防止自己的IP被封
cookieJar = cookiejar.MozillaCookieJar()
cookie= urllib.request.HTTPCookieProcessor(cookieJar)  #智能处理cookie
opener = build_opener(cookie,proxy,HTTPHandler)
install_opener(opener)
req = Request(login_url,postData,headers)
taobao = urlopen(req)
read = taobao.read().decode('gbk')
staus = taobao.getcode()
if staus == 200:
    print('获取服务器请求成功!')
    #处理验证码，获取token
    pattern = re.compile(r'(?<=<img id="J_StandardCode_m" src="https://s.tbcdn.cn/apps/login/static/img/blank.gif" data-src=").[^<]*?(?=")')
    checkCodeUrlList = re.findall(pattern, read)
    print(read)
    if len(checkCodeUrlList) != 0:
        webbrowser.open_new_tab(checkCodeUrlList[0])  #这里和下面的[0]，只是为了提取列表中的值
        print('到浏览器看验证码图片')
        checkcode = input('请输入验证码:')
        post['TPL_checkcode'] = checkcode
        postData = urlencode(post)
        req = Request(login_url,postData,headers)
        taobao = urlopen(req)
        read_token = taobao.read()
        #处理token，获得st
        pattern_token = re.compile(r'(?<=<input type="hidden" id="J_HToken" value=").[^<]*?(?=")')
        token = re.findall(pattern_token,read_token)
        token_url = 'https://passport.alipay.com/mini_apply_st.js?site=0&token=%s&callback=stCallback6' % token[0]
        req_token = Request(token_url)
        response_token = urlopen(req_token).read()
        #处理st，获得用户淘宝主页的登录地址
        pattern_st = re.compile(r'(?<="st":").[^<]*?(?=")')
        st = re.findall(pattern_st,response_token)
        st_url = 'https://login.taobao.com/member/vst.htm?st=%s&TPL_username=%s' % (st[0],username)
        req_st = Request(st_url)
        response_st = urlopen(req_st).read()
        print(response_st)
        pattern_end = re.compile(r'(?<=top.location = ").[^<]*?(?=";)')
        end = re.findall(pattern_end,response_st)
        end_url = '%s' % end[0]
        req_end = Request(end_url)
        response_end = urlopen(req_end).read()
        print(response_end)
