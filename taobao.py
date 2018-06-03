from urllib.parse import urlencode
from urllib.request import ProxyHandler, HTTPCookieProcessor, build_opener, HTTPHandler, Request, urlopen

from requests import HTTPError

from ali1688.helper import get_proxy

from http import cookiejar

__author__ = 'CQC'
# -*- coding:utf-8 -*-

import urllib
import re
import webbrowser
import tool
from fake_useragent import UserAgent

#模拟登录淘宝类
class Taobao:

    #初始化方法
    def __init__(self):
        self.ua = UserAgent()
        #登录的URL
        self.loginURL = "https://login.taobao.com/member/login.jhtml"
        #代理IP地址，防止自己的IP被封禁
        self.proxyURL = get_proxy()
        #登录POST数据时发送的头部信息
        self.loginHeaders =  {
            'Host':'login.taobao.com',
            'User-Agent' : (self.ua).random,
            'Referer' : 'https://login.taobao.com/member/login.jhtml',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection' : 'Keep-Alive'
        }
        #用户名
        self.username = 'miyaye3344@gmail.com'
        #ua字符串，经过淘宝ua算法计算得出，包含了时间戳,浏览器,屏幕分辨率,随机数,鼠标移动,鼠标点击,其实还有键盘输入记录,鼠标移动的记录、点击的记录等等的信息
        self.ua='108%23Yq%2F%2F1%2FFl%2FYpRH0wWcbUwDWExOPijcLd8nA3JIfmdP3p%2FhLFH0dYaVqWeE7B%2F0jdA5Q9m9W1MJLFSvb1v1pcnht3Uz%2BwJ17spFHNdJwgqE%2FpFh%2FtqxHWpDx9pHLttvdQ9MQPEqvQiLtJqMmjFXMG39TLN7PhgYk1FUwk2UjgxJkiXCxSVJhXNY9VMoDxfa322TeTKPmcqerhU9ApkGYKohQ20XanrcLPyrw4nwLNPWMc6B2TVv%2FSv%2FmvDDwYQ8Mjvvu7G0J%2BWvctzCkvWX897RoD3MNapt1eM7SXZEPT2Jo5qq2BE%2Fjio7prdHG%2Fb%2Bf3zQc8PMaYw8ax5MQ5FTUebvmqqZyBRXXWGhIHIYIEhCmLGUX5k2xwi1g8ihrTEHLMiG5lcm3dnva0x1F3ZAF3bxo%2FzDg1DkbEHpq%2BefWkUzSdqblykfoMTIMuB5yOat6qaMnFQLunDs2lgcKHOQXEkFc17Yaupq0rhIyJqzwUtfiU%2FKZKMQWnuUyNHQBnMkTWP42%2FIMLxfKbwI%2F5nayOjZuVzfu2t4daSappYFafkc7rb91eiWbbOIpmb4huZvddtepzXrB6uptQc5nyHOynGu9QOMrX38wGCCGYFXb5C5H%2BdRJCb0TTa7kJAgcRirsVlRpJIkKTNciXtwbXyqeP7rQ7gnhWfp8KpAL%2FSuxaaDbtkJzKyDXUHR62WhNJp1ge8RdUlVD%2BOgG16DWs4hk%2Ff3jP1EqNDAduB7Iss81rawvCsqH%2BbN%2BIVmAP02h51BvjE3AIhkkbAtGhSHIWZbOkvjW4UjjFON4JmpRm6cRIunTgNGJY1wGTa5%2B%2FUKi2v7mIG5kw6gQF24F7lW1r3G%2FJJmAG9GAn9a%2FG89v5a5dGKOQMlro1LL5Pu31NydPdzYN3HFi%2Bai2aqx%2B98MGdCoO9vyVCAGJJxZ3WnvAKAmEtIzfcoCbQnid7AEU9y%2B6rB8ISS4mcrx5UzFqzXe9sO3jcBlMpdvel05dTP1K%2Fji75MLMH03lB2wJhFJNkBOnQqVhABsr2og0bcWn7cb4tgSF4trI0R0f5fErk%2B8zFVn7qbqARv%2FQOam%2B6kdLgO7d3dQTFT%2BYFwLPbKNhKNJzH2O36FAc5MP8%2B6%2F5SHN1kaCRtEZf86g2LdR82KsWUc1zKkl%2BPbyIw1skYglRePJ3tXtRpSI'

        #密码，在这里不能输入真实密码，淘宝对此密码进行了加密处理，256位，此处为加密后的密码
        self.password2 = '9a39c3fefeadf3d194850ef3a1d707dfa7bec0609a60bfcc7fe4ce2c615908b9599c8911e800aff684f804413324dc6d9f982f437e95ad60327d221a00a2575324263477e4f6a15e3b56a315e0434266e092b2dd5a496d109cb15875256c73a2f0237c5332de28388693c643c8764f137e28e8220437f05b7659f58c4df94685'
        self.post = post = {
            'ua':self.ua,
            'TPL_username': self.username,
            'TPL_password':'5vjwLdf4',
            'TPL_redirect_url':'https://i.taobao.com/my_taobao.htm',
            'gvfdcre':'68747470733A2F2F6C6F67696E2E74616F62616F2E636F6D2F6D656D6265722F6C6F676F75742E6A68746D6C3F73706D3D61317A30322E312E3735343839343433372E372E35383464373832646B775673334926663D746F70266F75743D7472756526726564697265637455524C3D6874747073253341253246253246692E74616F62616F2E636F6D2532466D795F74616F62616F2E68746D',
            'lang' : 'zh_CN',
            'loginsite' : '0',
            'from' : 'tb',
            'fc' : 'default',
            'style' : 'default',
            'loginType' : '3',
            'gvfdcname' : '10',
            'loginASR' : '1',
            'loginASRSuc' : '0',
            'oslanguage' : 'zh_CN',
            'sr' : '1440*900',
            'osVer' : 'macos|10.134',
            'naviVer' : 'chrome|66.03359181',
            'osACN' : 'Mozilla',
            'osAV' : '5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'appkey' : '00000000',



        }
        #将POST的数据进行编码转换
        self.postData = urlencode(self.post).encode('utf-8')
        #设置代理
        self.proxy = ProxyHandler({'http':self.proxyURL})
        #设置cookie
        self.cookie =  cookiejar.MozillaCookieJar()
        #设置cookie处理器
        self.cookieHandler = HTTPCookieProcessor(self.cookie)
        #设置登录时用到的opener，它的open方法相当于urlopen
        self.opener = build_opener(self.cookieHandler,self.proxy,HTTPHandler)
        #赋值J_HToken
        self.J_HToken = ''
        #登录成功时，需要的Cookie
        self.newCookie = cookiejar.MozillaCookieJar()
        #登陆成功时，需要的一个新的opener
        self.newOpener = build_opener(HTTPCookieProcessor(self.newCookie))
        #引入工具类
        self.tool = tool.Tool()

    #得到是否需要输入验证码，这次请求的相应有时会不同，有时需要验证有时不需要
    def needCheckCode(self):
        #第一次登录获取验证码尝试，构建request
        request = Request(self.loginURL,self.postData,self.loginHeaders)
        #得到第一次登录尝试的相应
        response = self.opener.open(request)
        #获取其中的内容
        content = response.read().decode('gbk')
        #获取状态吗
        status = response.getcode()
        #状态码为200，获取成功
        if status == 200:
            print(u"获取请求成功")
            #\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801这六个字是请输入验证码的utf-8编码
            pattern = re.compile(u'\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801',re.S)
            result = re.search(pattern,content)
            #如果找到该字符，代表需要输入验证码
            if result:
                print(u"此次安全验证异常，您需要输入验证码")
                return content
            #否则不需要
            else:
                #返回结果直接带有J_HToken字样，表明直接验证通过
                tokenPattern = re.compile('id="J_HToken" value="(.*?)"')
                tokenMatch = re.search(tokenPattern,content)
                if tokenMatch:
                    self.J_HToken = tokenMatch.group(1)
                    print(u"此次安全验证通过，您这次不需要输入验证码")
                    return False
        else:
            print(u"获取请求失败")
            return None

    #得到验证码图片
    def getCheckCode(self,page):
        #print(page)
        #得到验证码的图片
        pattern = re.compile('<img id="J_StandardCode_m.*?data-src="(.*?)"',re.S)
        #匹配的结果
        matchResult = re.search(pattern,page)
        #已经匹配得到内容，并且验证码图片链接不为空
        if matchResult and matchResult.group(1):
            return matchResult.group(1)
        else:
            print(u"没有找到验证码内容")
            return False

    #输入验证码，重新请求，如果验证成功，则返回J_HToken
    def loginWithCheckCode(self):
        #提示用户输入验证码
        checkcode = input('请输入验证码:')
        #将验证码重新添加到post的数据中
        self.post['TPL_checkcode'] = checkcode
        #对post数据重新进行编码
        self.postData = urlencode(self.post)
        try:
            #再次构建请求，加入验证码之后的第二次登录尝试
            request = Request(self.loginURL,self.postData,self.loginHeaders)
            #得到第一次登录尝试的相应
            response = self.opener.open(request)
            #获取其中的内容
            content = response.read().decode('gbk')
            #检测验证码错误的正则表达式，\u9a8c\u8bc1\u7801\u9519\u8bef 是验证码错误五个字的编码
            pattern = re.compile(u'\u9a8c\u8bc1\u7801\u9519\u8bef',re.S)
            result = re.search(pattern,content)
            #如果返回页面包括了，验证码错误五个字
            if result:
                print(u"验证码输入错误")
                return False
            else:
                #返回结果直接带有J_HToken字样，说明验证码输入成功，成功跳转到了获取HToken的界面
                tokenPattern = re.compile('id="J_HToken" value="(.*?)"')
                tokenMatch = re.search(tokenPattern,content)
                #如果匹配成功，找到了J_HToken
                if tokenMatch:
                    print(u"验证码输入正确")
                    self.J_HToken = tokenMatch.group(1)
                    return tokenMatch.group(1)
                else:
                    #匹配失败，J_Token获取失败
                    print(u"J_Token获取失败")
                    return False
        except HTTPError as e:
            print(u"连接服务器出错，错误原因",e.response)
            return False

    #通过token获得st
    def getSTbyToken(self,token):
        tokenURL = 'https://passport.alipay.com/mini_apply_st.js?site=0&token=%s&callback=stCallback6' % token
        request = Request(tokenURL)
        response = urlopen(request)
        #处理st，获得用户淘宝主页的登录地址
        pattern = re.compile('{"st":"(.*?)"}',re.S)
        result = re.search(pattern,response.read())
        #如果成功匹配
        if result:
            print(u"成功获取st码")
            #获取st的值
            st = result.group(1)
            return st
        else:
            print(u"未匹配到st")
            return False

    #利用st码进行登录,获取重定向网址
    def loginByST(self,st,username):
        stURL = 'https://login.taobao.com/member/vst.htm?st=%s&TPL_username=%s' % (st,username)
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
            'Host':'login.taobao.com',
            'Connection' : 'Keep-Alive'
        }
        request = Request(stURL,headers = headers)
        response = self.newOpener.open(request)
        content =  response.read().decode('gbk')
        #检测结果，看是否登录成功
        pattern = re.compile('top.location = "(.*?)"',re.S)
        match = re.search(pattern,content)
        if match:
            print(u"登录网址成功")
            location = match.group(1)
            return True
        else:
            print("登录失败") 
            return False

    #获得已买到的宝贝页面
    def getGoodsPage(self,pageIndex):
        goodsURL = 'http://buyer.trade.taobao.com/trade/itemlist/listBoughtItems.htm?action=itemlist/QueryAction&event_submit_do_query=1' + '&pageNum=' + str(pageIndex)
        response = self.newOpener.open(goodsURL)
        page =  response.read().decode('gbk')
        return page

    #获取所有已买到的宝贝信息
    def getAllGoods(self,pageNum):
        print(u"获取到的商品列表如下")
        for x in range(1,int(pageNum)+1):
            page = self.getGoodsPage(x)
            self.tool.getGoodsInfo(page)

    #程序运行主干
    def main(self):
        #是否需要验证码，是则得到页面内容，不是则返回False
        needResult = self.needCheckCode()
        #请求获取失败，得到的结果是None
        if not needResult ==None:
            if not needResult == False:
                print(u"您需要手动输入验证码")
                checkCode = self.getCheckCode(needResult)
                #得到了验证码的链接
                if not checkCode == False:
                    print(u"验证码获取成功")
                    print(u"请在浏览器中输入您看到的验证码")
                    webbrowser.open_new_tab(checkCode)
                    self.loginWithCheckCode()
                #验证码链接为空，无效验证码
                else:
                    print(u"验证码获取失败，请重试")
            else:
                print(u"不需要输入验证码")
        else:
            print(u"请求登录页面失败，无法确认是否需要验证码")

        #判断token是否正常获取到
        if not self.J_HToken:
            print( "获取Token失败，请重试")
            return
        #获取st码
        st = self.getSTbyToken(self.J_HToken)
        #利用st进行登录
        result = self.loginByST(st,self.username)
        if result:
            #获得所有宝贝的页面
            page = self.getGoodsPage(1)
            pageNum = self.tool.getPageNum(page)
            self.getAllGoods(pageNum)
        else:
            print(u"登录失败")

taobao = Taobao()
taobao.main()