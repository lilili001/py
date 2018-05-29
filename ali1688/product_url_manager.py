class ProductUrlManager(object):
    def __init__(self):
        self.item_urls = set()
        self.crawed_item_urls = set()

    def addUrls(self, urls):
        print("========进入addUrls()方法============")
        print(urls)
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.addUrl(url)

    def addUrl(self, url):
        print("========进入addUrl()方法============")
        print(url)
        if url not in self.item_urls and url not in self.crawed_item_urls:
            self.item_urls.add(url)

    def hasUrl(self):
        return len(self.item_urls) > 0

    def getUrl(self):
        url = self.item_urls.pop()
        self.crawed_item_urls.add(url)
        return url

    def getAllUrls(self):
        print("========getAllUrls()方法============")
        print(self.item_urls)

        return self.item_urls