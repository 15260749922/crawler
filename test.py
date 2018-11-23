#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import passwd
import jieba
import re

class JiebaTest(unittest.TestCase):
    def test_cut(self):
        # sql = "select user_area from luhan_sab limit 1000;"
        # sql = "select user_area from luhan_sab where user_area like '%大连%';"
        sql = "select user_comment from luhan_inc limit 10;"

        with passwd.connect() as cur:
            jieba.load_userdict = 'source/userdict.txt'
            cur.execute(sql)
            result = cur.fetchall()
            pattern = re.compile(r'[\u4e00-\u9fa5_a-zA-Z0-9]+')
            re_words = re.findall(pattern, str(result))
            words = ' '.join(re_words)
            cut_words = jieba.lcut(words)
            print(cut_words)


if __name__ == "__main__":
    unittest.main()
