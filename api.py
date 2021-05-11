__author__ = 'thaiph99'

from newspaper import Article
import newspaper
from bs4 import BeautifulSoup
import requests
import re
from pyvi import ViTokenizer
from collections import Counter
import os
from scipy.spatial import distance
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor


class Keyword:
    def __init__(self, input_file):
        if isinstance(input_file, str):
            with open(input_file, 'r') as f:
                self.list_keys = f.readlines()
        else:
            self.list_keys = input_file

    def standardized(self):
        self.list_keys = [key.strip() for key in self.list_keys]
        self.list_keys = [key.replace('\n', '') for key in self.list_keys]
        self.list_keys = [key.replace(' ', '_') for key in self.list_keys]
        self.list_keys = [key.lower() for key in self.list_keys]


class Url:
    def __init__(self, input_file):
        if isinstance(input_file, str):
            with open(input_file, 'r') as f:
                self.list_url = f.readlines()
        else:
            self.list_url = input_file

    def standardized(self):
        self.list_url = [url.strip() for url in self.list_url]
        self.list_url = [url.replace('\n', '') for url in self.list_url]


class Category:
    def __init__(self):
        self.list_url_categories = []

    def get_category_url_from_url(self, url_home):
        homepage = newspaper.build(url_home)
        self.list_url_categories = homepage.category_urls()
        self.list_url_categories += [url_home]
        return self.list_url_categories


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

            list_remove = ['#box_comment_vne', '#box_comment',
                           'https://ai4vn.vnexpress.net/'
                           'https://youtube.com',
                           'https://twitter.com',
                           'https://facebook.com',
                           'https://www.facebook.com',
                           'https://www.twitter.com',
                           'https://www.youtube.com',
                           'https://www.24h.com.vn/magazine-c934.html',
                           'https://nhadat.tuoitre.vn/thi-truong.htm',
                           'https://www.24h.com.vn/tuyen-sinh-dh-cd-c365.html',
                           '#box_comment_vne', '#box_comment',
                           'ai4vn.vnexpress.net'
                           'youtube.com',
                           'twitter.com',
                           'facebook.com',
                           'www.facebook.com',
                           'www.twitter.com',
                           'www.youtube.com',
                           'www.24h.com.vn/magazine-c934.html',
                           'nhadat.tuoitre.vn/thi-truong.htm',
                           'www.24h.com.vn/tuyen-sinh-dh-cd-c365.html'
                           ]

            for removee in list_remove:
                news_link = news_link.replace(removee, '')

            if news_link not in self.list_url_news and is_valid(news_link):
                self.list_url_news.append(news_link)

    def __get_text_url(self, url, index):
        text = ''
        title = ''
        try:
            article = Article(url)
            article.download()
            article.parse()
        except:
            self.list_title[index] = title
            self.list_text_news[index] = text
            return
        title = article.title
        text = article.text.replace('\n', '.\n')
        self.list_title[index] = title
        self.list_text_news[index] = text
        # return title, text
        # print(title, text)

    @staticmethod
    def __get_keywords_from_text(text):
        tokens = ViTokenizer.tokenize(text)
        tokens = ViTokenizer.spacy_tokenize(tokens)[0]
        tokens = list(filter(lambda x: len(x) > 1, tokens))
        counter_tokens = Counter(tokens)
        counter_tokens = dict(counter_tokens)
        counter_tokens = dict(
            sorted(counter_tokens.items(), key=lambda x: -x[1]))
        return counter_tokens

    @staticmethod
    def get_important_score(counter_keys, keys):
        score = 0
        for key in counter_keys.keys():
            for k in keys:
                if k == key.lower():
                    score += counter_keys[key]
        return score

    def load_urls(self, categories):
        with ThreadPoolExecutor(max_workers=100) as executor:
            for category in categories:
                executor.submit(self.__get_urls_news_from_category, category)

    # def load_urls(self, categories):
    #     cnt = 0
    #     for category in categories:
    #         percent = round(cnt / (len(categories)), 2) * 100
    #         cnt += 1
    #         print(f'Loading {percent}%', end='\r')
    #         self.__get_urls_news_from_category(category)
    #     print('\nDone')
    #     return self.list_url_news

    # def load_text(self):
    #     cnt = 0
    #     for url in self.list_url_news:
    #         percent = round(cnt / (len(self.list_url_news)), 2) * 100
    #         cnt += 1
    #         print(f'Loading {percent}%', end='\r')
    #         self.__get_text_url(url)
    #         # print(len(self.list_text_news))
    #     print('\nDone')
    #     # return self.list_text_news

    def load_text(self):
        # muliple threading

        self.list_text_news = ['' for _ in range(len(self.list_url_news))]
        self.list_title = ['' for _ in range(len(self.list_url_news))]
        dict_index = {self.list_url_news[i]: i for i in range(
            len(self.list_url_news))}

        with ThreadPoolExecutor(max_workers=100) as executor:
            for url in self.list_url_news:
                executor.submit(self.__get_text_url, url, dict_index[url])

        # multiple processing
        # processes = []
        # list_tmp = self.list_url_news
        # with ProcessPoolExecutor(max_workers=6) as executor:
        #     for url in list_tmp:
        #         ex = executor.submit(self.__get_text_url, url)
        #         processes.append(ex)

        # self.list_title = []
        # self.list_text_news = []
        # for task in as_completed(processes):
        #     tup = task.result()
        #     self.list_counter_keys.append(tup[0])
        #     self.list_counter_keys.append(tup[1])

    def load_key(self):
        # multiple processing
        # with ProcessPoolExecutor(max_workers=6) as exercutor:
        #     processes = []
        #     for text in self.list_text_news:
        #         if text != '':
        #             ex = exercutor.submit(self.__get_keywords_from_text, text)
        #             processes.append(ex)

        # for task in as_completed(processes):
        #     self.list_counter_keys.append(task.result())
        # single processing
        for text in self.list_text_news:
            if text != '':
                self.list_counter_keys.append(
                    self.__get_keywords_from_text(text))
            else:
                self.list_counter_keys.append({'': 1})
        return self.list_counter_keys

    def load_score(self, keys):
        for counter_key1text in self.list_counter_keys:
            # print(keys)
            # print(counter_key1text)
            # print('------------------------------')
            self.list_score_news.append(
                self.get_important_score(counter_key1text, keys))

        return self.list_score_news

    @staticmethod
    def compare(bag1, bag2):
        if len(bag1.keys()) <= 100 or len(bag2.keys()) <= 100:
            return 0
        bag = list(bag1.keys()) + list(bag2.keys())
        bag = [word.lower() for word in bag]
        bag = set(bag)
        vecbag1 = []
        vecbag2 = []
        for feature in bag:
            if feature in bag1.keys():
                vecbag1.append(bag1[feature])
            else:
                vecbag1.append(0)
            if feature in bag2.keys():
                vecbag2.append(bag2[feature])
            else:
                vecbag2.append(0)
        return distance.euclidean(vecbag1, vecbag2)

    def write_data(self, filepath):
        n = len(self.list_text_news)
        for i in range(n):
            title = self.list_title[i]
            url = self.list_url_news[i]
            text = self.list_text_news[i]
            for c in ['>', '\n']:
                try:
                    text = text.replace(c, ' ')
                except:
                    continue
            with open(filepath + '/' + str(i) + '.txt', 'w') as f:
                f.write(str(title))
                f.write('\n')
                f.write(str(url))
                f.write('\n')
                f.write(str(text))
                f.write('\n')

    def load_data(self, filepath):
        pix = os.listdir(filepath)
        self.list_title = []
        self.list_url_news = []
        self.list_text_news = []
        self.list_score_news = []
        self.list_counter_keys = []
        for filename in pix:
            with open(filepath + '/' + filename, 'r') as f:
                title = f.readline()
                url = f.readline()
                text = f.readline()
            # print(title)
            self.list_title.append(title)
            self.list_url_news.append(url)
            self.list_text_news.append(text)
