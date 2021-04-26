import queue
import threading
import time
from api import News
from api import Keyword
from api import Url
from api import Category
from newspaper import Article
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
from time import time

# create list link -----------------
url = Url('urls.txt')
key = Keyword('keywords.txt')
categorys = Category()
list_category = []
for url_home in url.list_url:
    list_category += categorys.get_category_url_from_url(url_home)
list_category
news = News()
news.load_urls(list_category)
len(news.list_url_news)
print('end pre processing')

list_text = []


def get_text_url(url):
    text = ''
    title = ''
    try:
        article = Article(url)
        article.download()
        article.parse()
    except:
        return text
    title = article.title
    text = article.text.replace('\n', '.\n')
    list_text.append(text)
    # print(text)
    print('------------------------------------------------')
    print(len(list_text))
    return text


# end -------------------------------
# processing multi thread
start = time()

processes = []
# with ThreadPoolExecutor(max_workers=1000) as executor:
#     for url in news.list_url_news:
#         a = executor.submit(get_text_url, url)
# print(as_completed(a))

with ProcessPoolExecutor(max_workers=6) as executor:
    for url in news.list_url_news:
        processes.append(executor.submit(get_text_url, url))


for task in as_completed(processes):
    print(task.result())

print(f'Time taken: {time() - start}')
print(len(list_text))
print(len(processes))
