#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/7/9
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import winsound

def alarm():
    duration = 1000  # millisecond
    freq = 440  # Hz
    winsound.Beep(freq, duration)  # 其中freq是频率(以赫兹为单位)表示声音大小，duration表示发生时长，1000为1秒

if __name__ == '__main__':
    pass