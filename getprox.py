#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import multiprocessing
import tools


class GetProx(object):

    """Docstring for ProxCheck. """

    def __init__(self):
        """TODO: to be defined1. """
        self.header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64)\
    AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}

    def get_info(self, q):
        page = 1
        while True:
            url = 'http://www.xicidaili.com/nn/%d' % (page)
            req = requests.get(url, headers=self.header)
            soup = BeautifulSoup(req.text, 'lxml')
            trs = soup.find('table', id='ip_list').find_all('tr')
            for tr in trs[1:]:
                ip = tr.contents[3].text
                port = tr.contents[5].text
                procotol = tr.contents[11].text
                q.put((ip, port, procotol.lower()))
            page += 1

    def check(self, q, lock):
        while True:
            data = q.get()
            try:
                req = requests.get('http://www.baidu.com',
                                   proxies={'%s' % (data[2]): '%s://%s:%s'
                                            % (data[2], data[0], data[1])},
                                   timeout=2, headers=self.header,
                                   cookies=self.cookie)
                if req.status_code == 200:
                    lock.acquire()
                    print(data)
                    tools.i_ip(data)
                    lock.release()
                else:
                    print('not200', data)
            except Exception as e:
                print(e, 'erro', data)
                pass


q = multiprocessing.Queue(10)
lock = multiprocessing.Lock()
glock = multiprocessing.Lock()


if __name__ == "__main__":
    cker = GetProx()
    cheks = []
    getr = multiprocessing.Process(target=cker.get_info, args=(q, ))
    getr.start()
    for i in range(10):
        p = multiprocessing.Process(target=cker.check, args=(q, lock))
        cheks.append(p)
    for i in range(10):
        cheks[i].start()
