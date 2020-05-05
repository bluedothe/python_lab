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

def create_null_df():
    df = pd.DataFrame(columns=["block_type","block_name","member_count"])
    print(df)

#创建dataframe对象，第一种： 用Python中的字典生成,必须放到数组里
def create_df1():
    data_dict1 = {"block_type":"tdx.gn","block_name":"稀土","member_count":35}
    data = [data_dict1]
    df = pd.DataFrame(data)
    print(df)

    data_dict1 = {"block_type": "tdx.gn", "block_name": "稀土", "member_count": 35}
    data_dict2 = {"block_type": "tdx.gn", "block_name": "特高压", "member_count": 20}
    data = [data_dict1, data_dict2]
    df = pd.DataFrame(data)
    print(df)

    data_dict1 = {"block_type": "tdx.gn", "block_name": ["稀土", "特高压"]}
    df = pd.DataFrame(data_dict1)
    print(df)

    data_dict1 = {"block_type": "tdx.gn", "block_name": ["稀土", "特高压"], "member_count":[35,20]}
    df = pd.DataFrame(data_dict1)
    print(df)

    data = {'A': 1.,
            'B': pd.Timestamp('20130102'),
            'C': pd.Series(1, index=list(range(4)), dtype='float32'),
            'D': np.array([3] * 4, dtype='int32'),
            'E': pd.Categorical(["test", "train", "test", "train"]),
            'F': 'foo'}
    df = pd.DataFrame(data)
    print(df)

    data = {
        "a": [1, 2, 3],
        "b": [4, 5, 6],
        "c": [7, 8, 9]
    }
    df = pd.DataFrame(data, index = ["a","b","c"])
    print(df)

    data = {
        "one": np.random.rand(3),
        "two": np.random.rand(3)  # 这里尝试“two”：np.random.rand（4）会报错，
    }
    df = pd.DataFrame(data)
    print(df)

    data = {
        "Jack": {"math": 90, "english": 89, "art": 78},
        "Marry": {"math": 82, "english": 95, "art": 96},
        "Tom": {"math": 85, "english": 94}
    }
    df = pd.DataFrame(data)
    df = pd.DataFrame(data, columns=["Jack", "Tom", "Bob"])
    df = pd.DataFrame(data, index=["a", "b", "c"], columns=["Jack", "Tom", "Bob"])
    df = pd.DataFrame(data, index=["art", "math", "english"], columns=["Jack", "Tom", "Bob"])
    print(df)


#创建dataframe对象，第二种： 利用指定的列内容、索引以及数据
def create_df2():
    columns = ["block_type", "block_name", "member_count"]
    data = [['tdx.gn','abc',4],['tdx.gn','xyz',5]]
    dates = pd.date_range('2020-05-01',periods=2)
    df = pd.DataFrame(data=data,columns=columns,index=dates)
    print(df)

#创建dataframe对象，通过读取文件，可以是json,csv,excel等等，如果用excel请先安装xlrd这个包。
def create_df3():
    df = pd.read_excel("")
    df = pd.read_csv("")
    df = pd.read_json("")
    df = pd.read_html("")
    df = pd.read_sql("")

#创建dataframe对象，第四种：用numpy中的array生成
def create_df4():
    data = np.arange(15).reshape(3,5)  #生成0-14共15个数，分成3行5列的二维数组
    df = pd.DataFrame(data)
    print(df)

    df = pd.DataFrame(np.random.randn(6, 4), columns=list('ABCD'))   #6行4列的随机数，列名分别为ABCD
    print(df)

    index = pd.date_range('1/1/2000', periods=8)
    df = pd.DataFrame(np.random.randn(8, 3), index=index, columns=['A', 'B', 'C'])
    print(df)

#创建dataframe对象，第五种： 用numpy中的array，但是行和列名都是从numpy数据中来的
def create_df5():
    pass

#创建dataframe对象，第六种： 利用tuple合并数据
def create_df6():
    block_type = ['tdx.gn','tdx.gn','tdx.gn']
    block_name = ['稀土', '特高压', '5G']
    member_count = [35,20,44]
    list_tuples = list(zip(block_type,block_name,member_count))
    df = pd.DataFrame(list_tuples,columns=['block_type','block_name','member_count'])  #,columns=[]
    print(df)

#创建dataframe对象，第七种： 利用pandas的series
def create_df7():
    dates = pd.date_range('2020-05-01', periods=3)
    df = pd.DataFrame.from_dict({"block_type":pd.Series(['tdx.gn','tdx.gn','tdx.gn'],index=dates),
                                 "block_name": pd.Series(['稀土', '特高压', '5G'],index=dates),
                                 "member_count": pd.Series([35, 20, 44],index=dates)
                                 })
    print(df)

    df = pd.DataFrame({
        'one': pd.Series(np.random.randn(3), index=['a', 'b', 'c']),
        'two': pd.Series(np.random.randn(4), index=['a', 'b', 'c', 'd']),
        'three': pd.Series(np.random.randn(3), index=['b', 'c', 'd'])})
    print(df)

    data = {'水果': pd.Series(['苹果', '梨', '草莓']),
            '数量': pd.Series([3, 2, 5]),
            '价格': pd.Series([10, 9, 8])}
    df = pd.DataFrame(data)
    print(df)

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

def test4():
    s = pd.Series(np.random.randn(5), index=['a', 'b', 'c', 'd', 'e'])
    print(s)
    print(s.array)
    print(s.index.array)

def test5():
    long_series = pd.Series(np.random.randn(1000))
    print(long_series.head())  # 默认头5条
    print(long_series.tail(3))

def test7():
    df = pd.DataFrame(np.random.randn(6,4),columns=list('ABCD'))  #6行4列的随机数，列名分别为ABCD
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
    create_df4()