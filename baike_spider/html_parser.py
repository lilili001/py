import re
import urllib

#from anaconda_project.requirements_registry.network_util import urlparse
from urllib.parse import urljoin

from bs4 import BeautifulSoup


class HtmlParser(object):

    def parse(self, page_url, html_cont): #从url中解析出两个东西 新的url列表和数据

        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url,soup)
        new_data = self._get_new_data(page_url,soup)

        return new_urls,new_data

    def _get_new_urls(self, page_url, soup):

        new_urls = set()
        links = soup.find_all('a',href=re.compile(r"/item(/[\s\S]*)+"))
        for link in links:
            new_url = link['href']
            new_full_url =  urljoin(page_url,new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        res_data = {}

        #获取url
        res_data['url'] = page_url

        #获取标题
        title_node = soup.find('dd',class_='lemmaWgt-lemmaTitle-title').find('h1')
        res_data['title'] = title_node.get_text()

        #获取描述
        summery_node = soup.find('div',class_='lemma-summary')
        res_data['summary'] = summery_node.get_text()

        return res_data