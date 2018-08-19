# -*- coding: utf-8 -*-  
#爬浏览器手机的ua头
import threading
import Queue
import requests
from lxml import etree

lock = threading.RLock()
class uasspider(threading.Thread):
        def __init__(self,urls_queue,uas_queue):
                threading.Thread.__init__(self)
                self.uas_queue = uas_queue
                self.urls_queue = urls_queue
        def run(self):
                while True:
                        url = self.urls_queue.get()
                        self.get_uas(url)
        def get_uas(self,url):
                        req = requests.get(url)
                        text = req.text
                        html = etree.HTML(text)
                        uas = html.xpath("/html/body/div[2]/table/tr/td[4]/text()")
                        uas.pop(0)
                        lock.acquire()
                        for ua in uas:
                                print ua
                        lock.release()
def main():
        urls_queue = Queue.Queue()
        uas_queue = Queue.Queue()
        for i in range(1,5):
                url = "http://www.fynas.com/ua/search?d=&b=&k=1&page=%s" %i
                urls_queue.put(url)
        for i in range(2):
                t = uasspider(urls_queue, uas_queue)
                t.start()
if __name__ == '__main__':
	main()
