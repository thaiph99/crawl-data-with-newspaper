from newspaperedited import Article
import numpy as np  
import newspaper

''' get urls and keywords from file '''

with open('urls.txt', 'r') as f:
    urls = f.readlines()
urls = [url.replace('\n', '') for url in urls]
print(urls)


with open('keywords.txt', 'r') as f:
    keywords = f.readlines()
keywords = [key.replace('\n', '') for key in keywords]

''' standardize keywords '''

keywords = [key.replace(' ', '_') for key in keywords]
keywords = [key.lower() for key in keywords]

print(keywords)


from bs4 import BeautifulSoup
import requests
import re  

def is_valid(url):
    return re.findall(r'\.[a-z]{3}', url)

# global dict
dict_url = {}

''' crawl function '''

def get_link_articles_from_url(url):
    respone = requests.get(url)
    soup = BeautifulSoup(respone.text, 'html.parser')
    
    for a in soup.find_all('a', href=True):
        articles_link = a['href']
        if articles_link not in dict_url.keys() and is_valid(articles_link):
            dict_url[articles_link] = 1

    return list(dict_url.keys())

# test 
print(*get_link_articles_from_url(urls[0])[:5], sep='\n')

import newspaperedited

def get_category(url_home):
    home = newspaperedited.build(url_home)
    category_urls = home.category_urls()
    return category_urls

print('------crawling category --------')
list_cate = [get_category(url) for url in urls]
list_categorys = []
for i in list_cate:
    list_categorys += i  
list_categorys[:5]
print('------done ---------------------')
