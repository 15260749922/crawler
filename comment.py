#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from time import sleep
import queue
import re
import requests
import random
import tools
import passwd


class Comment:
    def __init__(self):
        #  需要获取的信息
        self.user_domain = ''
        self.user_name = ''
        self.user_comment = ''
        self.header = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686)\
                       AppleWebKit/537.36 (KHTML, like Gecko) TGUbuntu\
                       Chromium/59.0.3071109 Chrome/59.0.3071.109\
                       Safari/537.36',
                       'referers': 'https://weibo.cn/comment/FcnGmhbjL?\
                       uid=1537790411&rl=0',
                       'accept': 'text/html,application/xhtml+xml,application/\
                       xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                       'accept-encoding': 'gzip, deflate, br',
                       'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
                       'Connection': 'keep-alive',
                       'Host': 'weibo.cn',
                       'Upgrade-Insecure-Requests': '1',
                       }
        #  应对反爬虫
        self.cookie = passwd.cookie
    def get_comment(self):
        page = 1
        cg_login = random.randint(0, 2)
        while True:
            url = 'https://weibo.cn/comment/FcnGmhbjL?uid=1537790411&rl=0\
                &page=%d' % (page)
            if page % 20 == 0:
                print('cg_login')
                cg_login = random.randint(0, 2)
            try:
                req = requests.get(url, cookies=self.cookie[cg_login],
                                   headers=self.header, timeout=5,)
                if req.status_code != 200:
                    raise(req.status_code, cg_login)
            except Exception as e:
                print(e, 'here')
                continue
            print(page, '-------', cg_login,)
            soup = BeautifulSoup(req.content, 'lxml')
            tags = soup.find_all('div', class_='c', id=re.compile(r'C_.+'))
            #  TODO: 2017-07-28 matianhe #
            """
                遍历每一页代码,匹配每个用户的域名，用户名，评论。
                调用tools实现加入数据库
            """
            for tag in tags:
                try:
                    self.user_domain = re.sub(r'.*/', '', tag.a['href'])
                    self.user_name = tag.a.text
                    self.user_comment = tag.find_all('span', 'ctt')[0].text
                except Exception as e:
                    print('break------', self.user_domain, self.user_name,
                          self.user_comment)
                tools.add_inc((self.user_domain, self.user_name,
                               self.user_comment))
                print(self.user_name,)

            page += 1
            sleep(random.randint(1, 4))


if __name__ == "__main__":
    com = Comment()
    com.get_comment()
