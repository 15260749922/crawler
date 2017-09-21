#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
import jieba
from passwd import connect
import numpy as np
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from scipy.misc import imread


class Analyse(object):
    def __init__(self,):
        jieba.load_userdict("source/dict.txt")

    def cut_zh(self, sql, cut=False):
        with connect() as cur:
            cur.execute(sql)
            result = cur.fetchall()
            words = map(lambda word: word[0], result)
            words = list(words)
        if cut:
            pattern = re.compile(r'[\u4e00-\u9fa5_a-zA-Z0-9]+')
            words = re.findall(pattern, str(result))
            words = ' '.join(words)
            jieba.load_userdict("source/dict.txt")
            words = jieba.cut(words)
            words = filter(lambda word: word != ' ', words)
            words = list(words)
        return words

    def make_df(self, words, stopword=None):
        my_df = pd.DataFrame({'segment': words})
        if stopword:
            stopwords = pd.read_csv(stopword, names=['stopword'],
                                    encoding='utf-8')
            my_df = my_df[~my_df.segment.isin(stopwords.stopword)]
        my_df = my_df.groupby(['segment'])['segment'].agg({'count': np.size})
        my_df = my_df.reset_index().sort_values(['count'], ascending=False)
        return my_df

    def draw_wc(self, words, stopword=None, title=''):
        if stopword:
            data = self.make_df(words, stopword)
        else:
            data = self.make_df(words)
        bg_pic = imread('source/luhan.jpg')
        wordcloud = WordCloud(background_color='black', max_font_size=110,
                              mask=bg_pic, min_font_size=10, mode='RGBA',
                              font_path='source/simhei.ttf')
        word_frequence = {x[0]: x[1] for x in data.values}
        wordcloud = wordcloud.fit_words(word_frequence)
        plt.title(title, fontsize=16)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()

    def draw_pie(self, words, stopword=None, title=''):
        if stopword:
            data = self.make_df(words, stopword)
        else:
            data = self.make_df(words)
        data = data[0:10].values
        x = [count[1] for count in data]
        y = [name[0] for name in data]
        expl = list(0 for i in range(len(x)))
        expl[0] = 0.1
        plt.title(title, fontsize=16)
        plt.pie(x, labels=y, autopct='%1.0f%%', pctdistance=0.8, shadow=True,
                startangle=60, explode=expl)
        plt.axis('equal')
        plt.legend()
        plt.show()

    def draw_bar(self, words, stopword=None, title=''):
        if stopword:
            data = self.make_df(words, stopword)
        else:
            data = self.make_df(words)
        data = data[0:30].values
        x = range(len(data))
        y = [count[1] for count in data]
        label = [name[0] for name in data]
        plt.bar(x, y, tick_label=label, color='rgbycmk', alpha=0.3)
        plt.xticks(rotation=30)
        plt.title(title, fontsize=16)
        for a, b in zip(x, y):
            plt.text(a, b+0.05, '%.0f' % b, ha='center', fontsize=10)
        plt.show()

    def draw_barh(self, words, stopword=None, title=''):
        if stopword:
            data = self.make_df(words, stopword)
        else:
            data = self.make_df(words)
        data = data[0:30].values
        x = range(len(data))
        y = [count[1] for count in data]
        label = [name[0] for name in data]
        plt.barh(x, y, tick_label=label, color='rgbycmk', alpha=0.2)
        plt.title(title, fontsize=16)
        plt.xlabel('人数', fontsize=12)
        for a, b in zip(x, y):
            plt.text(b, a, '%.0f' % b, ha='left', va='center', fontsize=10)
        plt.show()

    def draw_plot_birth(self, words, stopword=None, title=''):
        """TODO: Docstring for draw_plot.

        :words: TODO
        :stopword: TODO
        :title: TODO
        :returns: TODO

        """
        if stopword:
            data = self.make_df(words, stopword)
        else:
            data = self.make_df(words)
        x_sort = data.sort_values('segment').values[42:110]
        x = range(len(x_sort))
        y = [name[1] for name in x_sort]
        plt.plot(x, y, 'b--')
        plt.title(title)
        plt.xlabel('年份', fontsize=14)
        plt.ylabel('数量', fontsize=14)
        plt.xticks(x, [i[0] for i in x_sort], rotation=90)
        plt.show()

    def draw_plot(self, words, stopword=None, title=''):
        """TODO: Docstring for draw_plot.

        :words: TODO
        :stopword: TODO
        :title: TODO
        :returns: TODO

        """
        if stopword:
            data = self.make_df(words, stopword)
        else:
            data = self.make_df(words)
        words = data.sort_values('count', ascending=False).values
        x = range(len(words))
        y = [name[1] for name in words]
        plt.plot(x, y, 'b--')
        plt.xlabel('粉丝序号')
        plt.ylabel('每个人的评论数')
        plt.title(title)
        plt.show()

    def cut_year(self, sql):
        with connect() as cur:
            cur.execute(sql)
            result = cur.fetchall()
        pattern = re.compile(r'\d{4}')
        words = re.findall(pattern, str(result))
        return words

    def draw_bar_bylabel(self, words, stopword=None, title=''):
        if stopword:
            data = self.make_df(words, stopword)
        else:
            data = self.make_df(words)
        data = data.head(10)
        year = [year for year in data['segment'].values]
        x = range(len(year))
        y = data['count']
        plt.bar(x, y, color='rgbyckm', alpha=0.6)
        plt.xticks(x, year, rotation=0)
        plt.title(title, fontsize=16)
        plt.xlabel('生日/年', fontsize=12)
        plt.ylabel('评论数', fontsize=12)
        for a, b in zip(x, y):
            plt.text(a, b+1, '%.0f' % b, ha='center', va='bottom', fontsize=16)
        plt.show()


if __name__ == "__main__":
    area = 'select user_area from luhan_sab'
    birth = 'select user_birth from luhan_sab'
    name = 'select user_name from luhan_inc'
    sex = 'select user_sex from luhan_sab'
    comment = 'select user_comment from luhan_inc'
    pro_stop = 'source/province.txt'
    com_stop = 'source/com.txt'
    analyse = Analyse()
    # words = analyse.cut_zh(comment, True)
    words = analyse.cut_zh(name)
    # words = analyse.cut_year(birth)
    analyse.draw_wc(words, None, '昵称分析词云')
    # analyse.draw_barh(words, None, '评论数前30')
    # analyse.draw_plot_birth(words, None, '年龄分布折线图')
    # analyse.draw_bar_bylabel(words, None, '1th-10th分布统计')
    # analyse.draw_wc(words, com_stop, '评论分析词云')
    # analyse.draw_barh(words, pro_stop, '城市分布柱状图')
    # analyse.draw_pie(words, None, '性别分布图')
