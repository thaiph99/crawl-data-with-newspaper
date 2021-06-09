
from crawl.crawl_v2 import Keyword, News, Url


def process(url, key):
    news = News()
    news.load_urls(url, key)
    url.standardized()
    key.standardized()
    news.load_text()
    news.load_key()
    news.load_score(key.list_keys)
    list_ans = news.list_score_news
    list_index = [_ for _ in range(len(list_ans))]
    dict_ans = dict(zip(list_ans, list_index))
    dict_ans = dict(sorted(dict_ans.items(), key=lambda x: -x[0])[:20])
    dict_res = {}
    for _, i in dict_ans.items():
        if _ == 0:
            break
        dict_res[news.list_title[i]] = (
            news.list_url_news[i], news.list_title[i])
    return dict_res


list_urls = ['https://vnexpress.net/',
             'https://www.24h.com.vn/',
             'https://tuoitre.vn/']

list_keys = ['thủ tướng',
             'chính phủ',
             'Phạm Minh Chính']

urls = Url(list_urls)
keys = Keyword(list_keys)
answer = process(urls, keys)

for item in answer.items():
    print(item[0])
    print(item[1][0])
    print('-----------------------')
