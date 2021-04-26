import threading
import time
import urllib
import urllib3


class Post:

    def __init__(self, website, data, mode):
        self.website = website
        self.data = data

        # mode is either "Simple"(Simple POST) or "Multiple"(Multi-thread POST)
        self.mode = mode

    def post(self):

        # post data
        req = urllib3.Request(self.website)
        open_url = urllib3.urlopen(req, self.data)

        if self.mode == "Multiple":
            time.sleep(0.001)

        # read HTMLData
        HTMLData = open_url.read()

        print("OK")


if __name__ == "__main__":

    current_post = Post("http://forum.xda-developers.com/login.php", "vb_login_username=test&vb_login_password&securitytoken=guest&do=login",
                        "Simple")

    # save the time before post data
    origin_time = time.time()

    if(current_post.mode == "Multiple"):

        # multithreading POST

        for i in range(0, 10):
            thread = threading.Thread(target=current_post.post)
            thread.start()
            thread.join()

        # calculate the time interval
        time_interval = time.time() - origin_time

        print(time_interval)

    if(current_post.mode == "Simple"):

        # simple POST

        for i in range(0, 10):
            current_post.post()

        # calculate the time interval
        time_interval = time.time() - origin_time

        print(time_interval)
