import queue
import threading
import time
from api import News
from api import Keyword
from api import Url
from api import Category
from newspaper import Article

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
    print('Done')
    return text


list_text = []

# end -------------------------------


exitFlag = 0


class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print("Starting " + self.name)
        process_data(self.name, self.q)
        print("Exiting " + self.name)


def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            url = q.get()
            # processing
            text = get_text_url(url)
            list_text.append(text)
            queueLock.release()
            print("%s processing %s" % (threadName, url))
        else:   
            queueLock.release()


threadList = ["Thread-"+str(_) for _ in range(1, 15)]
# nameList = [_ for _ in range(0, 100)]
queueLock = threading.Lock()
workQueue = queue.Queue(10000)
threads = []
threadID = 1

# Create new threads
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# Fill the queue
queueLock.acquire()
for word in news.list_url_news[:100]:
    workQueue.put(word)
queueLock.release()

# Wait for queue to empty
while not workQueue.empty():
    pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
    t.join()
print("Exiting Main Thread")
print(len(list_text))
print(list_text)
