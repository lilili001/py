## 函数式编程
###1.能够接受函数作为参数的函数叫做高阶函数
    def add(x,y,f):
        return f(x)+f(y)
    add(5,9,abs)  
###2. map(fn,arr)
map()是 Python 内置的高阶函数，它接收一个函数 f 和一个 list，并通过把函数 f 依次作用在 list 的每个元素上，得到一个新的 list 并返回。
    
    def f(x):
        return x*x
    print map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    
输出结果：[1, 4, 9, 10, 25, 36, 49, 64, 81]  
###3. reduce函数
reduce()函数也是Python内置的一个高阶函数。reduce()函数接收的参数和 map()类似，一个函数 f，一个list，但行为和 map()不同，reduce()传入的函数 f 必须接收两个参数，reduce()对list的每个元素反复调用函数f，并返回最终结果值。

例如，编写一个f函数，接收x和y，返回x和y的和：      
    
    def f(x, y):
        return x + y
调用 reduce(f, [1, 3, 5, 7, 9])时，reduce函数将做如下计算：
+ 先计算头两个元素：f(1, 3)，结果为4；
+ 再把结果和第3个元素计算：f(4, 5)，结果为9；
+ 再把结果和第4个元素计算：f(9, 7)，结果为16；
+ 再把结果和第5个元素计算：f(16, 9)，结果为25；
+ 由于没有更多的元素了，计算结束，返回结果25。

reduce()还可以接收第3个可选参数，作为计算的初始值。如果把初始值设为100，计算：
        
    reduce(f, [1, 3, 5, 7, 9], 100)

###4. filter函数
filter()函数是 Python 内置的另一个有用的高阶函数，filter()函数接收一个函数 f 和一个list，这个函数 f 的作用是对每个元素进行判断，返回 True或 False，filter()根据判断结果自动过滤掉不符合条件的元素，返回由符合条件元素组成的新list。

例如，要从一个list [1, 4, 6, 7, 9, 12, 17]中删除偶数，保留奇数，首先，要编写一个判断奇数的函数：
    
    def is_odd(x):
        return x % 2 == 1
然后，利用filter()过滤掉偶数
    
    filter(is_odd, [1, 4, 6, 7, 9, 12, 17])
利用filter()，可以完成很多有用的功能，例如，删除 None 或者空字符串：
    
    def is_not_empty(s):
        return s and len(s.strip()) > 0
    filter(is_not_empty, ['test', None, '', 'str', '  ', 'END'])
结果：['test', 'str', 'END']
注意: s.strip(rm) 删除 s 字符串中开头、结尾处的 rm 序列的字符。

当rm为空时，默认删除空白符（包括'\n', '\r', '\t', ' ')，如下：
    
    a = '     123'
    a.strip()
结果： '123'
    
    a='\t\t123\r\n'
    a.strip()
结果：'123'

###5.sorted()排序
    sorted([36, 5, 12, 9, 21])
[5, 9, 12, 21, 36]

但 sorted()也是一个高阶函数，它可以接收一个比较函数来实现自定义排序，比较函数的定义是，传入两个待比较的元素 x, y，如果 x 应该排在 y 的前面，返回 -1，如果 x 应该排在 y 的后面，返回 1。如果 x 和 y 相等，返回 0。

因此，如果我们要实现倒序排序，只需要编写一个reversed_cmp函数：

    def reversed_cmp(x, y):
        if x > y:
            return -1
        if x < y:
            return 1
        return 0
这样，调用 sorted() 并传入 reversed_cmp 就可以实现倒序排序：

    sorted([36, 5, 12, 9, 21], reversed_cmp)
[36, 21, 12, 9, 5]

###6.python中返回函数
    def f():
        print 'call f()...'
        # 定义函数g:
        def g():
            print 'call g()...'
        # 返回函数g:
        return g
###7. 通过高阶函数返回新函数

    def f1(x):
        return x*x
    def new_fn(f):
        def fn(x):
            print('call'+f.name++'()')
            return f(x)
        return fn
调用方法：

    g = new_fn(f1)
    g(5)
    
#### 7.1 python中编写无参数decorator
Python的 decorator 本质上就是一个高阶函数，它接收一个函数作为参数，然后，返回一个新函数。

使用 decorator 用Python提供的 @ 语法，这样可以避免手动编写 f = decorate(f) 这样的代码。

考察一个@log的定义：

    def log(f):
        def fn(x):
            print 'call ' + f.__name__ + '()...'
            return f(x)
        return fn
对于阶乘函数，@log工作得很好：

    @log
    def factorial(n):
        return reduce(lambda x,y: x*y, range(1, n+1))
    print factorial(10)
    
# 网页下载器
urllib2

网页下载器方法一：

    import urllib2
    #直接请求
    response = urllib2.urlopen('http://www.baidu.com')
    #获取返回状态吗
    print response.getCode()
    #读取内容
    cont = response.read()
 
网页下载器方法二：
 添加header , data 给urllib2.Request
 urllib2.urlopen(request)
 
    import urllib2
    #创建request对象
    request = urllib2.Request(url)
    #添加数据
    request.add_data('a',1)
    #添加http的header
    request.add_header('User-Agent','Mozilla/5.0')
    #发送请求获取结果
    response = urllib2.urlopen(request)

网页下载器方法三：
+ HTTPCookieProcessor 需要登陆的情况 要获取cookie
+ ProxyHandler
+ HTTPSHandler
+ HTTPRedirectHandler

all => urllib2.build_opener(handler)
urllib2.install_opener(opener)
urllib2.urlopen(request)

    import urllib2,cookielib
    #创建cookie容器
    cj = cookielib.CookieJar()
    #创建一个opener
    opener = urllib2.build_opener( urllib2.HTTPCookieProcessor(cj) )
    #给urllib2安装opener
    urllib2.install_opener(opener)
    #使用带有cookie的urllib2访问网页
    response = urllib2.urlopen("http://www.baidu.com")

或者:
    ua = UserAgent()
    proxy = detail_craw.get_proxy()
    proxy_handler = request.ProxyHandler({"http":"http://{}".format(proxy)})
    opener = request.build_opener(proxy_handler)
    req = request.Request(url)
    req.add_header('User-Agent',ua.random)
    r = opener.open(req)


网页下载器之requests:
    html = requests.get(detail_page_url, proxies={"http":"http://{}".format(proxy) } ,headers=headers )
    content = html.text


# 网页解析器
+ 正则:模糊匹配
+ html.parser：结构化解析 
+ Beautiful Soap：结构化解析
+ Ixml：结构化解析

网页解析器 Beautifulsoup语法

+ 创建BeautifulSoup对象
    soup = BeautifulSoup(html_doc,'html.parser',from_encoding='utf8')

+ 搜索节点 find,find_all

find_all(name,attrs,string)

 查找所有标签为a的节点： soup.find_all('a')
 soup.find_all('a',href="***")
 soup.find_all('a',href=re.compile(r'/view/\d+\.html'))

 soup.find_all('a',class='abc',string='目标文字')

实例：抓取百度百科python词条页面以及相关页面的数据

快速引入模块 和 创建类  alt+enter

## 多线程

threading.active_count() //当前激活的线程数量
threading.enumerate() //查看当程是哪几个
threading.current_thread() //查看当前运行的是哪个进程

创建一个进程

import threading

def thread_job():
    print('This is a new thread, thread name is %s' % threading.current_thread() )

new_thread = threading.Thread(target=thread_job,name="T1")
new_thread.start()
new_thread.join() //进程本身都是同时进行的，如果想要后续程序在当前进程完成后运行 则需要 join()

lock的作用是 当多个进程同时进行的时候 让进程按顺序执行 这样不会乱

## 计算时间差

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


    start = datetime.datetime.now()
    time.sleep(5)
    end = datetime.datetime.now()
    end2 = start + datetime.timedelta(hours=10.5)

    used_time = (end2-start)
    alltime = used_time.seconds
    print(changeTime(alltime))

# 使用模块
googletrans,datetime

# csv 文件读取
    r = csv.reader(open('files/data.csv')) # 返回列表

  文件写入
    new_csv = open('files/data_new.csv','w')
    writer = csv.writer(new_csv)
    writer.writerows(lines)
    new_csv.close()

# tesseract-ocr windows
    tesseract-ocr windows 安装方法：
    https://blog.csdn.net/wei_ai_ni/article/details/76163856

    然后环境变量的设置：
    https://www.cnblogs.com/jianqingwang/p/6978724.html

    不需要visualstudio

# 正则替换
    str = "促销 女装背带性感伴娘晚礼服 交叉露背亮片Wish连衣裙"
    reg = r'[促销|wish]'
    pattern = re.compile(reg,re.IGNORECASE)
    out = re.sub(pattern , '',str )
    print(out) #女装背带性感伴娘晚礼服 交叉露背亮片连衣裙