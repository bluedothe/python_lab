#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/2/23
'''

import numpy as np
import sys

__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

def test1():
    a = np.arange(15).reshape(3, 5)
    print(a)
    print(type(a)) #数组类型
    print(a.shape) #数组的维度。这是一个整数的元组
    print(a.ndim)  #轴（维度）的个数
    print(a.size)  #数组元素的总数。这等于 shape 的元素的乘积
    print(a.dtype.name)  #数组中元素类型
    print(a.itemsize)  #数组中每个元素的字节大小
    print(a.data) #该缓冲区包含数组的实际元素。通常，我们不需要使用此属性，因为我们将使用索引访问数组中的元素
    b = np.array([6, 7, 8])
    print(b)
    c = np.array([(1,2,3,4),(2,3,4,5),(3,4,5,6)],dtype=np.int32)   #dtype=complex,int32,.int16,float64
    print(c)
    d = np.zeros((3,4))
    print(d)
    e = np.ones((2,3,4), dtype=np.int16)
    print(e)
    f = np.empty((2,3))  #其初始内容是随机的
    print(f)
    g = np.arange(10, 30, 0.5).reshape(5, 8)  #arange返回数组而不是列表,第一个参数是起始值，第二个参数是上限，第三个参数是步长
    print(g)
    h = np.linspace(0, 2, 40).reshape(5, 8)  #linspace函数，第一个参数是起始值，第二个参数是最后一个值，第三个参数是元素的个数
    print(h)
    #np.set_printoptions(threshold=sys.maxsize)  #如果数组太大，默认定义输出四个角点的元素，此函数可以强制打印全部元素
    print("---")
    #i = np.fromfunction(f,(5,4),dtype=int)  #TypeError: 'numpy.ndarray' object is not callable
    #print(i)

def f(x,y):
    return 10 * x + y

if __name__ == '__main__':
    test1()