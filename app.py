from time import time

from flask import Flask, render_template, request

from crawl.crawl_v2 import Keyword, News, Url

app = Flask(__name__)
result = {'number_urls': ['url0', 'url1', 'url2'],
          'number_keys': ['key0', 'key0', 'key2'], 'data': {}}


@app.route("/")
def home():
    return render_template("index.html", result=result)


def compare_and_remove(dict_ans):
    pass


def process(url, key):
    start = time()
    news = News()
    print(f'time1 : {time() - start}')
    news.load_urls(url, key)
    print(f'time2 : {time() - start}')
    url.standardized()
    key.standardized()
    news.load_text()
    print(f'time3 : {time() - start}')
    news.load_key()
    print(f'time4 : {time() - start}')
    news.load_score(key.list_keys)
    print(f'time5 : {time() - start}')
    print('list text ', len(news.list_text_news))
    print('list counter key ', len(news.list_counter_keys))
    print('list score ', len(news.list_score_news))
    print('list title ', len(news.list_title))
    print('list url ', len(news.list_url_news))
    list_ans = news.list_score_news


    list_index = [_ for _ in range(len(list_ans))]
    dict_ans = dict(zip(list_ans, list_index))
    dict_ans = dict(sorted(dict_ans.items(), key=lambda x: -x[0])[:20])
    print(dict_ans)

    dict_res = {}
    for _, i in dict_ans.items():
        if _ == 0:
            break
        dict_res[news.list_title[i]] = (
            news.list_url_news[i], news.list_title[i])
    # print(dict_res)
    print('total time : ', time() - start)
    return dict_res


@app.route("/", methods=["POST", "GET"])
def crawl():
    list_urls = []
    list_keys = []
    if request.form['crawl'] == 'Begin load':
        urlnum = request.form['urlnum']
        keynum = request.form['keynum']
        result['number_urls'] = ['url'+str(_) for _ in range(int(urlnum))]
        result['number_keys'] = ['key'+str(_) for _ in range(int(keynum))]
        print(type(request.form))
        print(request.form)
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

        print(list_urls)
        print(list_keys)
        print('len keys : ', len(list_keys))
        print('len urls : ', len(list_urls))
        urls = Url(list_urls)
        keys = Keyword(list_keys)

        result['data'] = process(urls, keys)
        print('number articles :', len(result['data'].keys()))
        print(*result['data'], sep='\n')
        # result = {'test1': 'pham hong thai', 'test2': 'thaiph99'}
        return render_template('index.html', result=result)


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=8020)
