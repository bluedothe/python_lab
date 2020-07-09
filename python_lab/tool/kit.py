#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/7/9
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import winsound

#freq是频率(以赫兹为单位)表示声音大小，duration表示发生时长，单位毫秒，1000为1秒
def bebe(freq, duration):
    winsound.Beep(freq, duration)

def alarm(times=1, freq = 440, duration = 1000):
    for i in range(times):
        bebe(freq, duration)  # 其中freq是频率(以赫兹为单位)表示声音大小，duration表示发生时长，1000为1秒
        bebe(300, 500)

if __name__ == '__main__':
    alarm(3)