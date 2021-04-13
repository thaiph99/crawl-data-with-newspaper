from bs4 import BeautifulSoup
from newspaper import Article

import requests

import re


def is_valid(url):
    return re.findall(r'\.[a-z]{3}', url)


url_home = 'https://vnexpress.net/'

respone = requests.get(url_home)
soup = BeautifulSoup(respone.text, 'html.parser')

dict_url = {}
for a in soup.find_all('a', href=True):
    url = a['href']
    if url not in dict_url.keys() and is_valid(url):
        dict_url[url] = 1

print(*dict_url.keys(), sep='\n')

dict_title = {}

path = 'datacrawled/'
cnt = 0
for url in dict_url.keys():

    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    text = article.text.replace('\n', '.\n')
    title = article.title
    summary = article.summary
    url = article.url
    if title not in dict_title.keys():
        dict_title[title] = 1
        cnt += 1
        with open(path+'article'+str(cnt)+'.txt', 'w') as f:
            f.write(title+'\n')
            f.write(url+'\n')
            f.write(summary+'\n')
