#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/5/1
    拼音与汉字转换
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import pypinyin
from pypinyin import lazy_pinyin

# 不带声调的(style=pypinyin.NORMAL)
def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s

#设置拼音风格
def ss(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.INITIALS):
        s = s + ''.join(i) + " "
    return s

# 带声调的(默认)
def yinjie(word):
    s = ''
    # heteronym=True开启多音字
    for i in pypinyin.pinyin(word, heteronym=True):
        s = s + ''.join(i) + " "
    return s

#不考虑多音字
def yy(word):
    return lazy_pinyin(word)
if __name__ == "__main__":
    print(pinyin("忠厚传家久"))
    print(yinjie("诗书继世长"))
    print(yy(u"诗书继世长"))
    print(pinyin(u"中心"))
    print(ss(u"中心"))
    print(yy(u"中心"))