from time import time

from flask import Flask, render_template, request

from crawl.crawl_v2 import Keyword, News, Url

app = Flask(__name__)
result = {'number_urls': ['url0', 'url1', 'url2'],
          'number_keys': ['key0', 'key0', 'key2'], 'data': {}}


def init():
    result['number_urls'] = ['url0', 'url1', 'url2']
    result['number_keys'] = ['key0', 'key0', 'key2']
    result['data'] = {}


@app.route("/")
def home():
    # reload and clean data
    init()
    return render_template("index.html", result=result)


def compare_and_remove(dict_ans):
    pass


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
    dict_ans = dict(sorted(dict_ans.items(), key=lambda x: -x[0])[:30])
    dict_res = {}
    for _, i in dict_ans.items():
        if _ == 0:
            break
        dict_res[news.list_title[i]] = (
            news.list_url_news[i], news.list_title[i])
    return dict_res


@app.route("/", methods=["POST", "GET"])
def crawl():
    list_urls = []
    list_keys = []
    if request.form['crawl'] == 'Begin load':
        urlnum = request.form['urlnum']
        keynum = request.form['keynum']
        result['number_urls'] = ['url' + str(_) for _ in range(int(urlnum))]
        result['number_keys'] = ['key' + str(_) for _ in range(int(keynum))]
        result['data'] = {}
        print(type(request.form))
        print(request.form)
        # init()
        return render_template('index.html', result=result)
    if request.form['crawl'] == 'Begin crawl':
        print(type(request.form))
        print(request.form)
        a = [request.form[_] for _ in result['number_urls']]
        b = [request.form[_] for _ in result['number_keys']]

        for i in a:
            ii = i.strip()
            if ii != '':
                list_urls.append(ii)

        for i in b:
            ii = i.strip()
            if ii != '':
                list_keys.append(ii)

        print('URL: ', list_urls)
        print('keys: ', list_keys)
        urls = Url(list_urls)
        keys = Keyword(list_keys)
        start = time()
        result['data'] = process(urls, keys)
        print('total time : ', time()-start)
        print('number articles :', len(result['data'].keys()))
        print(*result['data'], sep='\n')
        return render_template('index.html', result=result)


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=8020)
