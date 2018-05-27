class ListUrlManager(object):
    def __init__(self):
        self.list_urls = set()
        self.crawed_list_urls = set()

    def hasUrl(self):
        return len(self.list_urls) > 0

    def getUrl(self):
        url = self.list_urls.pop()
        self.crawed_list_urls.add(url)
        return url

    def addUrls(self, urls):
        if urls is None or len(urls)==0:
            return

        for url in urls:
            self.addUrl(url)

    def addUrl(self,url):
        if url not in self.crawed_list_urls and url not in self.list_urls:
            self.list_urls.add(url)