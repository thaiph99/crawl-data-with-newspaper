from api import News
from api import Keyword
from api import Url
from api import Category

url = Url('urls.txt')
key = Keyword('keywords.txt')
categorys = Category()

print('Load category')

list_category = []
for url_home in url.list_url:
    list_category += categorys.get_category_url_from_url(url_home)
list_category

news = News()
print('Load url')
news.load_urls(list_category)
len(news.list_url_news)

print('Load text')
news.load_text()
