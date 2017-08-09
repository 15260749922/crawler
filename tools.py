#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re  # noqa
import requests  # noqa
import random  # noqa
import queue  # noqa
import passwd


def get_oneproxie():
    sql = 'select * from ip_list limit 10'
    with passwd.connect() as cur:
        cur.execute(sql)
        res = cur.fetchall()
        one = random.choice(res)
        proxie = {one[2]: one[2] + '://' +
                  one[0] + ':' + one[1]}
    return proxie


def get_proxies():
    proxies = []
    sql = 'select * from ip_list'
    with passwd.connect() as cur:
        cur.execute(sql)
        res = cur.fetchall()
        for procotol, ip, port in res:
            proxie = {res[2]: res[2] + '://' +
                      res[0] + ':' + res[1]}
        proxies.append(proxie)
    return proxies


def c_table_luhan_inc():
    sql = 'create table luhan_inc(user_domain varchar(16),\
        user_name varchar(32), user_comment varchar(512))'
    with passwd.connect() as cur:
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)


def c_table_luhan_sab():
    sql = 'create table luhan_sab(num int unique auto_increment,user_domain\
            varchar(16) unique, user_sex char(4), user_area varchar(32),\
            user_birth varchar(16))'
    with passwd.connect() as cur:
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)


def c_table_ip_list():
    sql = 'create table ip_list(id int unique auto_increment,\
        ip varchar(16) primary key, port varchar(8) not null,\
        procotol varchar(8) not null)'
    with passwd.connect() as cur:
        try:
            cur.execute(sql)
            print('成功创建')
        except Exception:
            print('表已经存在，可继续操作，或者删除表后重新运行。')


def i_ip(data, many=0):
    print('i_ip')
    sql = 'insert into ip_list(ip, port, procotol) values\
        (%s, %s, %s)'
    try:
        with passwd.connect() as cur:
            if many != 0:
                cur.executemany(sql, data)
            else:
                cur.execute(sql, data)
    except Exception as e:
        print(e)


def i_inc(data):
    with passwd.connect() as cur:
        try:
            sql = ('insert into luhan_inc(user_domain, user_name,\
                user_comment) values (%s, %s, %s)')
            cur.execute(sql, data)
        except Exception as e:
            print(e, 'error')


def i_sab(data):
    sql = 'update luhan_sab set user_sex=%s, user_area=%s, user_birth=%s\
           where num = %s'
    with passwd.connect() as cur:
        cur.execute(sql, data)


def rm_ip():
    sql = 'delete from ip_list'
    with passwd.connect() as cur:
        cur.execute(sql)


def s_domain(data):
    sql = 'select user_domain from luhan_sab where num=%s'
    with passwd.connect() as cur:
        cur.execute(sql, data)
        domain = cur.fetchone()
    return domain[0]


if __name__ == "__main__":
    c_table_ip_list()
