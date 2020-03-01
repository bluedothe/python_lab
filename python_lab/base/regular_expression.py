#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2019/11/3
    正则表达式练习
'''

import re

__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2019"

def re_test1():
    pattern = re.compile('\d+')
    str1 = 'Tom is 8 years old, Serry is 24 years old.'
    result = pattern.findall(str1)
    print(result)

if __name__ == '__main__':
    re_test1()