#!/usr/bin/env python3
# -*- coding: utf-8 -*-


with open('city.txt', 'r+') as f:
    text = f.read()
    word = text.split(r'、')
    for w in word:
        f.write(str(w) +'\n')
