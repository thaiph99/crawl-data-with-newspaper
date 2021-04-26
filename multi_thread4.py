import requests
import threading

class Crawler:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def crawl(self):
        page = self.session.get(url)
        # Do your crawling here

with open('urls.txt', 'r') as f: # Assuming you use a file with a list of URLs
    for url in f:
        while(threading.active_count() > 20): # Use 20 threads
            time.sleep(0.1)
        c = Crawler(url)
        t = threading.Thread(target = c.crawl())