import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from ali1688.spider_main import SpiderMain


class HtmlParser(SpiderMain):
    def parse(self, content):
        #获取产品url列表
        if  content is None:
            return
        soup = BeautifulSoup(content,'html.parser',from_encoding='utf-8')
        return self.load_product_urls(soup)

    def load_product_urls(self, soup):
        new_urls = set()
        links = soup.find_all('a',class_="title-link")
        for link in links:
            url = link['href']
            new_urls.add(url)

        print("===========开始解析===================")
        return new_urls

    #详情页解析 只针对当前页面 返回一条数据
    def parseDetailPage(self, item_page_content):
        soup = BeautifulSoup( item_page_content , 'html.parser' , from_encoding='gbk' )
        res = {}

        #title
        title_node = soup.find('h1',class_="d-title")
        res['title'] = title_node.get_text()

        #price
        price_node = soup.select('.table-sku tr:nth-of-type(1) .price .value')
        res['price'] =  price_node.get_text()

        #shipping
        shipping_fee_node = soup.select('.cost-entries-type .value')
        res['shipping_fee'] = shipping_fee_node.get_text()

        #specifications

        color_nodes = soup.select



