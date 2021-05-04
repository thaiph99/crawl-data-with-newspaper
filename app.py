from flask import Flask, redirect, url_for, render_template, request, flash
from api import News
from api import Keyword
from api import Url
from api import Category
import time

app = Flask(__name__)
result = {}


@app.route("/")
def home():
    return render_template("index2.html", result=result)


def compare_and_remove(dict_ans):
    pass


def process(url, key):
    categorys = Category()
    list_category = []
    for url_home in url.list_url:
        list_category += categorys.get_category_url_from_url(url_home)
    list_category
    news = News()
    news.load_urls(list_category[:2])
    news.load_text()
    news.load_key()
    news.load_score(key.list_keys)
    print(len(news.list_text_news))
    print(len(news.list_counter_keys))
    print(len(news.list_score_news))
    print(len(news.list_title))
    print(len(news.list_url_news))
    list_ans = news.list_score_news
    print(list_ans)
    print(len(dict_ans))
    list_index = [_ for _ in range(len(list_ans))]
    dict_ans = dict(zip(list_ans, list_index))
    dict_ans = dict(sorted(dict_ans.items(), key=lambda x: -x[0]))
    print(dict_ans)
    
    dict_res = {}
    for _, i in dict_ans.items():
        dict_res[news.list_title[i]] = news.list_url_news[i]
    print(dict_res)
    return dict_res
    # list_score = []
    # for i in news.list_counter_keys:
    #     for j in news.list_counter_keys:
    #         list_score.append((news.compare(i, j), cnti, cntj))


@app.route("/", methods=["POST", "GET"])
def crawl():
    start = time.time()
    list_urls = [1, 2, 3]
    list_keys = [1, 2, 3]
    if request.method == 'POST':
        list_urls[0] = request.form['url0']
        list_urls[1] = request.form['url1']
        list_urls[2] = request.form['url2']
        list_keys[0] = request.form['key0']
        list_keys[1] = request.form['key1']
        list_keys[2] = request.form['key2']

        urls = Url(list_urls)
        urls.standardized()
        keys = Keyword(list_keys)
        keys.standardized()
        result = process(urls, keys)
        print(type(result))
        # result = {'test1': 'pham hong thai', 'test2': 'thaiph99'}
    print('total time : ', time.time()-start)
    return render_template('index2.html', result=result)


if __name__ == "__main__":
    app.run(debug=True)
