#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/2/13
'''

import pandas as pd
import numpy as np
import os

__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

def test1():
    animals = pd.DataFrame({'kind': ['cat', 'dog', 'cat', 'dog'],
                            'height': [9.1, 6.0, 9.5, 34.0],
                            'weight': [7.9, 7.5, 9.9, 198.0]})
    print(animals)
    a = animals.groupby("kind").agg(
                                min_height = pd.NamedAgg(column='height', aggfunc='min'),
                                max_height = pd.NamedAgg(column='height', aggfunc='max'),
                                average_weight = pd.NamedAgg(column='weight', aggfunc=np.mean),
                                )
    print(a)

def test2():
    s = pd.Series([1, 3, 5, np.nan, 6, 8])
    print(s)

    dates = pd.date_range('20130101', periods=6)
    print(dates)
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
    print(df)
    print(df.head())   #查看头部数据,默认头5条
    print(df.tail(3))  #查看尾部数据
    print(df.index)    #行标签
    print(df.columns)   #列标签
    print(df.sort_index(axis=1, ascending=False))   #按轴排序
    print(df.sort_values(by='B'))  #按值排序

    df2 = pd.DataFrame({'A': 1.,
                        'B': pd.Timestamp('20130102'),
                        'C': pd.Series(1, index=list(range(4)), dtype='float32'),
                        'D': np.array([3] * 4, dtype='int32'),
                        'E': pd.Categorical(["test", "train", "test", "train"]),
                        'F': 'foo'})
    print(df2)
    print(df2.T)   #转置数据
    print(df.describe())    #查看数据的统计摘要

def test3():
    index = pd.date_range('1/1/2000', periods=8)
    df = pd.DataFrame(np.random.randn(8, 3), index=index,columns=['A', 'B', 'C'])
    print(df)

def test4():
    s = pd.Series(np.random.randn(5), index=['a', 'b', 'c', 'd', 'e'])
    print(s)
    print(s.array)
    print(s.index.array)

def test5():
    long_series = pd.Series(np.random.randn(1000))
    print(long_series.head())  # 默认头5条
    print(long_series.tail(3))

def test6():
    df = pd.DataFrame({
        'one': pd.Series(np.random.randn(3), index=['a', 'b', 'c']),
        'two': pd.Series(np.random.randn(4), index=['a', 'b', 'c', 'd']),
        'three': pd.Series(np.random.randn(3), index=['b', 'c', 'd'])})
    print(df)

def test7():
    df = pd.DataFrame(np.random.randn(6,4),columns=list('ABCD'))
    filename = "D:/Temp/" + 'my_csv.csv'
    print(df)
    if os.path.isfile(filename):
        df1 = df.loc[df['A'] > 0.5]
        print(df1)
        df1.to_csv(filename, mode='a', header=False,sep=',')
    else:
        df2 = df.loc[df['A']>0.5]
        print(df2)
        df2.to_csv(filename, mode='w', header=True, sep=',')

if __name__ == '__main__':
    #test1()
    #test2()
    #test3()
    #test4()
    #test6()
    test7()