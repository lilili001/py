import redis
import re

class ProductUrlManager(object):
    def __init__(self,name ,redis):
        # self.item_urls = set()
        # self.crawed_item_urls = set()

        self.new_item_urls = name +'-new'
        self.old_item_urls = name +'-old'

        self.spidername = name
        self.r = redis


        # 1. sadd(name,value) 添加元素
        # 2. smembers(name) 查看所有元素
        # 3. scard(name) 获取name对应的集合中的元素个数
        # 4. sismember(name, value) #检查value是否是name对应的集合内的元素
        # 5. spop(name) #随机删除并返回指定集合的一个元素
        # 6. srem(name, value)  删除集合中的某个元素

        #self.r.spop(self.new_item_urls)

        # self.r.sadd('info','alice is a good girl')
        # self.r.sadd(self.new_item_urls,'alice is a good girl')

    def addUrls(self, urls):
        print( urls )
        print("========进入addUrls()方法============")
        print(urls)
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.addUrl(url)

    def addUrl(self, url):
        print("========进入addUrl()方法============")
        print(url)
        # f = open('files/product_urls','a')
        # if url not in self.item_urls and url not in self.crawed_item_urls:
        #     self.item_urls.add(url)
        #     f.write(url+'\n')
        # f.close()

        if self.r.sismember( self.old_item_urls , url ) == False and self.r.sismember( self.new_item_urls , url ) == False :
            self.r.sadd( self.new_item_urls , url )

        print( self.r.smembers( self.new_item_urls ) )


    def hasUrl(self):
        #return len(self.item_urls) > 0
        return self.r.scard( self.new_item_urls ) > 0

    def getUrl(self):
        # url = self.item_urls.pop()
        # self.crawed_item_urls.add(url)

        url = self.r.spop( self.new_item_urls )
        self.r.sadd( self.old_item_urls , url )

        return url

    def getAllUrls(self):
        print("========getAllUrls()方法============")
        urls = self.r.smembers( self.spidername + '-new' )
        print("=========最终有 %s 个产品url===========" % self.r.scard( self.new_item_urls ))

        print( self.r.smembers(self.new_item_urls) )
        return urls
