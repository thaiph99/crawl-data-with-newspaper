from newspaper import Article
url = 'https://vnexpress.net/tiem-vaccine-covid-19-duoc-thuong-4254992.html'
article = Article(url)
article.download()
# print(article.html)
article.parse()
print(article.title)
print((article.text))
print('nlp : ',article.nlp())
print('keywords : ',article.keywords)
