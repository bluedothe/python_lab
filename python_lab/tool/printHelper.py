#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

'''
    module description
    date: 2020/1/30
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

def printStar(str=""):
    if str == "": print('\n{}\n'.format('*'*79))
    print('\n{}\n'.format('*'*79),str,'\n{}\n'.format('*'*79),)

def printLine(str="",cha='*'):
    print(f'{cha}' * 40,str, f'{cha}' * 40)

"""
Return the frame object for the caller's stack frame.
获取当前函数名称和执行行号，可以用于打印调试信息
"""
def get_cur_info():
    try:
        raise Exception
    except:
        f = sys.exc_info()[2].tb_frame.f_back
        return (f.f_code.co_name, f.f_lineno)

def callfunc():
    print(get_cur_info())

#获取当前函数名称和执行行号
def get_cur_info2():
    print(sys._getframe().f_code.co_name, sys._getframe().f_lineno)
    print(sys._getframe().f_back.f_code.co_name)

if __name__ == '__main__':
    printLine("abc","-")
    get_cur_info2()
    callfunc()