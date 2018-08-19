# -*- coding: utf-8 -*-  
#手机归属地批量查询
import urllib
import urllib2
import threading
import re

iphones = []
url = "https://tcc.taobao.com/cc/json/mobile_tel_segment.htm?tel="
phone = raw_input('15983**6811:')
lock = threading.RLock()


def get_phone(iphone):
    for i in iphone:
        urls = urllib2.urlopen(url + str(i))
        page = urls.read()
        reg = r"carrier:'(.*)'"
        wordreg = re.compile(reg)
        wordreglist = re.findall(wordreg, page)
        lock.acquire()
        print (str(i) + "-----" + " ".join(wordreglist) + "\n")
        lock.release()


def get_nubmber(iphones):
    asterisk_num = phone.count('*')
    for i in range(0, 10**asterisk_num):
        iphones.append(phone.replace(
            '*' * asterisk_num, ("%0" + str(asterisk_num) + "d") % i))
    return iphones


if __name__ == "__main__":
    iphone = get_nubmber(iphones)
    dist = len(iphones) // 10
    for i in range(dist):
        t = threading.Thread(target=get_phone, args=(
            iphone[i * 10:(i + 1) * 10],))
        t.start()
