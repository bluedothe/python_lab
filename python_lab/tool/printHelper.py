#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
from functools import wraps

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

# 装饰器，计算函数执行需要的时间
# 使用说明：在需要计算时间的函数上使用注解@timer
def timer(func):
    def decor(*args):
        start_time = time.time()
        func(*args)
        end_time = time.time()
        d_time = end_time - start_time
        print("the running time is : ", d_time)
    return decor

def time_this_function(func):
    #作为装饰器使用，返回函数执行需要花费的时间
    @wraps(func)
    def wrapper(*args,**kwargs):
        start=time.time()
        result=func(*args,**kwargs)
        end=time.time()
        print(func.__name__,end-start)
        return result
    return wrapper

@time_this_function
def test_timer(n):
    while n > 0:
        time.sleep(0.1)
        n += -1

if __name__ == '__main__':
    printLine("abc","-")
    get_cur_info2()
    callfunc()
    test_timer(10)