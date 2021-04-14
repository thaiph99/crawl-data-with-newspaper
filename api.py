__author__ = 'thaiph99'

from newspaper import Article
import numpy as np
import newspaper
from bs4 import BeautifulSoup
import requests
import re


class Keyword:
    def __init__(self):
        with open('keywords.txt', 'r') as f:
            self.list_keys = f.readlines()

    def standardized(self):
        self.list_keys = [key.replace('\n', '') for key in self.list_keys]
        self.list_keys = [key.replace(' ', '_') for key in self.list_keys]
        self.list_keys = [key.lower() for key in self.list_keys]


class Url:
    def __init__(self):
        with open('urls.txt', 'r') as f:
            self.list_url = f.readlines()

    def standardized(self):
        self.list_url = [url.replace('\n', '') for url in self.list_url]


class Category:
    def __init__(self):
        self.list_url_categorys = []

    def get_category_url_from_url(self, url_home):
        homepage = newspaper.build(url_home)
        self.list_url_categorys = homepage.category_urls()
        return self.list_url_categorys


class News:
    def __init__(self):
        self.list_url_news = []
        self.list_index_news = []
        self.list_text_news = []
        self.list_score_news = []

    def get_url_news_from_urls(self, url):

        def is_valid(url):
            return re.findall(r'\.[a-z]{3}', url) and re.search(r'https://', url)

        list_urls_tmp = []
        respone = requests.get(url)
        soup = BeautifulSoup(respone.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            news_link = a['href'].replace('#box_comment_vne', '')
            news_link = news_link.replace('#box_comment', '')
            news_link = news_link.replace('https://youtube.com', '')
            news_link = news_link.replace('https://facebook.com', '')

            if news_link not in list_urls_tmp and is_valid(news_link):
                list_urls_tmp.append(news_link)

        return list_urls_tmp

    
