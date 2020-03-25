#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/3/25
    注解学习
'''
from functools import wraps

def log1(func):
    @wraps(func)    #如果不加该句，使用log注解后，print(test.__name__)结果为wrapper
    def wrapper():
        print('log开始 ...',func.__name__)
        func()
        print('log结束 ...',func.__name__)
    return wrapper

@log1
def test1():
    print('test1 ..')

def log2(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('log开始 ...', func.__name__)
        ret = func(*args, **kwargs)
        print('log结束 ...', func.__name__)
        return ret
    return wrapper

@log2
def test21(s):
    print('test21 ..', s)
    return s

@log2
def test22(s1, s2):
    print('test22 ..', s1, s2)
    return s1 + s2

def log3(arg):
    def _log(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('log开始 ...', func.__name__, arg)
            ret = func(*args, **kwargs)
            print('log结束 ...', func.__name__, arg)
            return ret
        return wrapper
    return _log


@log3('module1')
def test31(s):
    print('test31 ..', s)
    return s


@log3('module2')
def test32(s1, s2):
    print('test32 ..', s1, s2)
    return s1 + s2

if __name__ == '__main__':
    test1()
    print(test1.__name__)
    test21('a')
    test22('a', 'bc')
    test31('a')
    test32('a', 'bc')