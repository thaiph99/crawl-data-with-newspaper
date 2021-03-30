# !pip install newspaper3k
# !pip install nltk
# import nltk
# nltk.download('punkt')
'''
code test get summary from newspaper by thaiph99
'''

from newspaperedited import Article
# url = 'https://vnexpress.net/tiem-vaccine-covid-19-duoc-thuong-4254992.html'
url = 'https://vnexpress.net/chau-phi-thieu-hut-vaccine-covid-19-4253715.html'
article = Article(url)
article.download()
article.parse()
# print(article.html)

print('title : ', article.title)
print('content : ', article.text)
print('date : ', article.publish_date)

print('active nlp -----------')
article.nlp()
print('keywords : ', article.keywords)
print('len keywords : ', len(article.keywords))

print('sumary : \n', article.summary)
print('url article : ', article.url)
