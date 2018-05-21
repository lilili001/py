class UrlManager(object):
    def __init__(self):
        self.new_urls = set() #待爬取的 url
        self.old_urls = set() #爬取过的 url

    def add_new_url(self, url):
        if url is None:
            return

        if url not in self.new_urls and url not in self.old_urls: #如果是全新的url则添加进new_url
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def has_new_url(self):#待爬取的是否有值
        return len(self.new_urls) != 0

    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

