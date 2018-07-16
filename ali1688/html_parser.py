import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from ali1688.spider_main import SpiderMain


class HtmlParser(SpiderMain):
    def parse(self, content):
        #获取产品url列表
        if  content is None:
            return
        print(content)
        soup = BeautifulSoup(content,'html.parser',from_encoding='utf-8')
        return self.load_product_urls(soup)

    def load_product_urls(self, soup):
        new_urls = set()
        links = soup.find_all('a',class_="pic-rind")
        print('links')
        print(links)
        for link in links:
            url = link['href']
            print(url)
            new_urls.add(url)

        print("===========开始解析===================")
        print(new_urls)
        return new_urls

    #详情页解析 只针对当前页面 返回一条数据
    def parseDetailPage(self, item_page_content):
        soup = BeautifulSoup( item_page_content , 'html.parser' , from_encoding='gbk' )
        res = {}

        #title
        title_node = soup.find('h1',class_="product-name")
        res['title'] = title_node.get_text()

        #price
        price_node = soup.find('span',class_='p-price')
        res['price'] = price_node.get_text()
        if soup.find('span',itemprop="highPrice") == None:
            res['price'] =  price_node.get_text()

        #colors
        img_lis = soup.find_all('li',class_="item-sku-image")
        for color_li in img_lis:
            color = color_li.find('a').attrs['title']
            res['colors'].append(color)
        res['colors'] = ','.join(res['colors'])

        #sizes
        size_spans = soup.find('ul',id="j-sku-list-2").find_all('span')
        for size_span in size_spans:
            size = size_span.get_text()
            res['sizes'].append(size)
        res['sizes']=','.join(res['sizes'])

        #sizechart
        pattern = re.compile(r'"sizeAttr":{(.*?)}')
        sizechart = pattern.find(item_page_content)
        print(sizechart)

        #images
        img_pattern = re.compile(r'window.runParams.imageBigViewURL=[(.*?)]]')
        res['images'] = img_pattern.find(item_page_content)

        #specifications
        property_items = soup.find('ul',class_='product-property-list').find_all('li')
        for property_item in property_items:
            d={"title":'',"value":''}
            d['title'] = property_item.find('span',class_="propery-title").get_text()
            d['value'] = property_item.find('span',class_="propery-des").get_text()
            res['specs'].append(d)

        #supplier
        supplier = soup.find('a',class_="store-lnk")
        res['supplier'] = { "store":supplier.get_text(),  "store_link":supplier.attrs['href'] }

        #store address
        res["supplier_address"] = soup.find('dd',class_="store-address").get_text()