from bs4 import BeautifulSoup
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

for url in dict_url.keys():
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    text = article.text.replace('\n', '.\n')
    title = article.title
    summary = article.sumary
    url = article.url
    with open(path+title+'txt', 'r') as f:
        f.write

