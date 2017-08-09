#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
from random import randint  # noqa
import tools
from time import sleep
import multiprocessing as mp
import passwd


class Info(object):
    def __init__(self):
        self.user_domain = ''
        self.user_sex = ''
        self.user_area = ''
        self.user_birth = ''
        self.header = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686)\
                       AppleWebKit/537.36 (KHTML, like Gecko) TGUbuntu\
                       Chromium/59.0.3071109 Chrome/59.0.3071.109\
                       Safari/537.36',
                       'referers': 'https://weibo.cn/search/?pos=search',
                       'accept': 'text/html,application/xhtml+xml,application/\
                       xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                       'accept-encoding': 'gzip, deflate, br',
                       'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
                       'Connection': 'keep-alive',
                       'Host': 'weibo.cn',
                       'Upgrade-Insecure-Requests': '1',
                       }
        self.cookie = passwd.cookie
        self.cg_id = 0

    def set_num(self, q):
        global num

        while True:
            q.put(num)
            print(num, 'put')
            num += 1

    def get_sab(self, q):
        while True:
            global lock
            lock.acquire()
            num = q.get()
            self.user_domain = tools.s_domain(num)
            soup = self.get_page(self.user_domain, num)
            try:
                self.user_sex = re.findall(r'性别:(.*?)<br', str(soup))[0]
                self.user_area = re.findall(r'地区:(.*?)<br', str(soup))[0]
                self.user_birth = re.findall(r'生日:(.*?)<br', str(soup))[0]
            except Exception as e:
                self.user_birth = 'none'
            print(mp.current_process().name, num, self.user_area,
                  self.cg_id)
            tools.i_sab((self.user_sex, self.user_area, self.user_birth,
                         num))
            lock.release()
<<<<<<< HEAD
            sleep(randint(3, 5))
=======
            sleep(randint(3, 7))
>>>>>>> 11c055c6fa8d8669eefaaaaf29d13085ad3e300f

    def get_page(self, domain, num):
            if num % 20 == 0:
                self.cg_id = randint(0, 2)
            url = 'https://weibo.cn/{}/info'.format(domain)
            print(url)
            try:
                req = requests.get(url, headers=self.header, timeout=5,
<<<<<<< HEAD
                                   cookies=self.cookie[self.cg_id],)
=======
                                   cookies=self.cookie[cg_id],)
>>>>>>> 11c055c6fa8d8669eefaaaaf29d13085ad3e300f
                soup = BeautifulSoup(req.text, 'lxml')
                if req.status_code == 200:
                    return soup
                else:
                    print(req.status_code)
                    url = 'https://weibo.cn/{}'.format(domain)
                    req = requests.get(url, timeout=5,
                                       cookies=self.cookie[self.cg_id],
                                       headers=self.header)
                    soup = BeautifulSoup(req.text, 'lxml')
                    domain = re.compile(r'/(\d+)/info').\
                        findall(str(soup))[0]
                    return self.get_page(domain, num)
            except Exception as e:
                print(e, num, self.cg_id)
                self.cg_id = randint(0, 2)
                return self.get_page(domain, num)


q = mp.Queue(maxsize=5)
lock = mp.Lock()
num = 140048


if __name__ == "__main__":
    info = Info()
    pros = []
    n = mp.Process(target=info.set_num, args=(q,))
    n.start()
    for i in range(1):
        p = mp.Process(target=info.get_sab, args=(q,))
        pros.append(p)
    for i in range(1):
        pros[i].start()
    for i in range(1):
        pros[i].join()
    n.join()
