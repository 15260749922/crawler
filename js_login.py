#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from selenium import webdriver


class Robot(object):
    def login(self, u, p):
        driver = webdriver.Chrome()
        driver.get('http://www.jianshu.com')
        driver.find_element_by_link_text('登录').click()
        driver.find_element_by_class_name('qq').click()
        driver.switch_to_window(driver.window_handles[1])
        # 切换到QQ关联登陆框
        driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
        driver.find_element_by_id('switcher_plogin').click()
        driver.find_element_by_id('u').send_keys(u)
        driver.find_element_by_id('p').send_keys(p)
        driver.find_element_by_id('login_button').click()
        sleep(5)
        page = ['http://www.jianshu.com/p/c0d46925b4b0',
                'http://www.jianshu.com/p/d50394f0e575',
                'http://www.jianshu.com/p/3a15f212c6f5',
                'http://www.jianshu.com/p/3431944541eb',
                'http://www.jianshu.com/p/a3f74efb609e',
                'http://www.jianshu.com/p/2995c4cc1e93',
                'http://www.jianshu.com/p/008fab60af13',
                'http://www.jianshu.com/p/f603e922c455',
                'http://www.jianshu.com/p/c5f7238407ea',
                'http://www.jianshu.com/p/e6fb5ea65840',
                'http://www.jianshu.com/p/d5a07d21769f',
                'http://www.jianshu.com/p/fd584541d70e',
                'http://www.jianshu.com/p/1a834f1b2f9c',
                'http://www.jianshu.com/p/7d00f8833cf4',
                'http://www.jianshu.com/p/93bd7c64581f',
                'http://www.jianshu.com/p/9be919813fcd',
                'http://www.jianshu.com/p/cc205f345286',
                'http://www.jianshu.com/p/773862809093',
                'http://www.jianshu.com/p/ec9c3bbf9091',
                'http://www.jianshu.com/p/07c4950e0f7d',
                'http://www.jianshu.com/p/f9a58459fca2',
                ]
        for url in page:
            driver.get(url)
            sleep(1)
            driver.execute_script("window.scrollBy(0,document.body.scrollHeight)", "")
            sleep(1)
            driver.find_element_by_class_name('btn-like').click()
        driver.quit()


if __name__ == "__main__":
    with open('user.txt', 'r') as f:
        robot = Robot()
        for text in f:
            user = text.split(',')[0]
            psw = text.split(',')[1]
            driver = robot.login(user, psw)
            sleep(3)
            print(user, psw)
