__author__ = 'thaiph99'

from newspaper import Article
import numpy as np
import newspaper
from bs4 import BeautifulSoup
import requests
import re
from pyvi import ViTokenizer
from collections import Counter
import sys


class Keyword:
    def __init__(self, keywords_filename):
        with open('keywords.txt', 'r') as f:
            self.list_keys = f.readlines()

    def standardized(self):
        self.list_keys = [key.replace('\n', '') for key in self.list_keys]
        self.list_keys = [key.replace(' ', '_') for key in self.list_keys]
        self.list_keys = [key.lower() for key in self.list_keys]


class Url:
    def __init__(self, urls_filename):
        with open(urls_filename, 'r') as f:
            self.list_url = f.readlines()

    def standardized(self):
        self.list_url = [url.replace('\n', '') for url in self.list_url]


class Category:
    def __init__(self):
        self.list_url_categorys = []

    def get_category_url_from_url(self, url_home):
        homepage = newspaper.build(url_home)
        self.list_url_categorys = homepage.category_urls()
        self.list_url_categorys += [url_home]
        return self.list_url_categorys


class News:
    def __init__(self):
        self.list_title = []
        self.list_url_news = []
        self.list_text_news = []
        self.list_score_news = []
        self.list_counter_keys = []

    def __get_urls_news_from_category(self, category):

        def is_valid(url):
            return re.findall(r'\.[a-z]{3}', url) and re.search(r'https://', url)

        respone = requests.get(category)
        soup = BeautifulSoup(respone.text, 'html.parser')
        found = soup.find_all('a', href=True)
        for a in found:
            news_link = a['href']
            news_link = news_link.replace('#box_comment_vne', '')
            news_link = news_link.replace('#box_comment', '')
            news_link = news_link.replace('https://youtube.com', '')
            news_link = news_link.replace('https://facebook.com', '')
            if news_link not in self.list_url_news and is_valid(news_link):
                self.list_url_news.append(news_link)

    def __get_text_url(self, url):
        text = ''
        try:
            article = Article(url)
            article.download()
            article.parse()
        except:
            return text
        self.list_title.append(article.title)
        text = article.text.replace('\n', '.\n')
        return text

    def __get_keywords_from_text(self, text):
        tokens = ViTokenizer.tokenize(text)
        tokens = ViTokenizer.spacy_tokenize(tokens)[0]
        tokens = list(filter(lambda x: len(x) > 1, tokens))
        counter_tokens = Counter(tokens)
        counter_tokens = dict(counter_tokens)
        counter_tokens = dict(
            sorted(counter_tokens.items(), key=lambda x: -x[1]))
        return counter_tokens

    def __get_important_score(self, couter_keys, keys):
        score = 0
        for key in couter_keys.keys():
            for k in keys:
                if k == key.lower():
                    score += couter_keys[key]
        return score

    def load_urls(self, categorys):
        cnt = 0
        for category in categorys:
            percent = round(cnt/(len(categorys)), 2)*100
            cnt += 1
            print(f'Loading {percent}%', end='\r')
            self.__get_urls_news_from_category(category)
        print('\nDone')
        return self.list_url_news

    def load_text(self):
        cnt = 0
        for url in self.list_url_news:
            percent = round(cnt/(len(self.list_url_news)), 2)*100
            cnt += 1
            print(f'Loading {percent}%', end='\r')
            self.list_text_news.append(self.__get_text_url(url))
        print('\nDone')
        return self.list_text_news

    def load_key(self):
        for text in self.list_text_news:
            self.list_counter_keys.append(self.__get_keywords_from_text(text))
        return self.list_counter_keys

    def load_score(self, keys):
        for counter_key1text in self.list_counter_keys:
            self.list_score_news.append(
                self.__get_important_score(couter_keys, keys))

        return self.list_text_news

    def compare(self, bag1, bag2):
        bag=bag1.keys() + bag2.keys()
        bag=set(bag)
        pass

    def write_data(self, filepath):
        n=len(self.list_url_news)

        with open(path, 'w') as f:
            for i in range(n):
                f.write(self.list_title[i])
                f.write(self.list_url_news[i])
                f.write(self.list_text_news[i])

    def load_data(self, filepath):
        pass
