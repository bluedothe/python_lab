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

"""
if (dfn is not None) and (not dfn.empty):   #判断df是否为空

###重命名
df.rename(index=self.format_date, inplace=True)   #index重命名
df.rename(columns={'blockname': 'block_name'}, inplace=True)  #列名重命名

col_name = df.columns.tolist()  #获取列名list

df.reindex(columns=col_name)  #重建index

###改变列数据或新增列
dfpro.insert(0,'code',code)  #插入一列到第一列前
df['data_source'] = "tdx"   #改变列数据，列不存在则新增
df['ts_code'] = df['code'].apply(lambda x: x + ".SH" if x[0:1] == "6" else ".SZ")   #改变列数据，列不存在则新增
df['volume'] = df['volume'].apply(lambda x: int(x))  # 取整
df['block_type'] = df['block_type'].map(lambda x: str(x))  #数字类型转字符类型
df['block_type'] = df['block_category'].str.cat(df['block_type'], sep = ".")  #列拼接，可选参数sep指定分隔符
df.loc[df['amount'] == 5.877471754111438e-39, 'amount'] = 0  # 列值根据条件筛选后修改为0
df['new_date'] = (df.index)  #将index值赋给一列，列不存在则新建

df.drop(['year', 'month', 'day', 'hour', 'minute', 'datetime'], axis=1, inplace=True)   #删除列

#合并两个df数据
dfall = pd.merge(dfpro, df,how='left', left_on='trade_date',right_on='new_date',sort=False,copy=False)   #两个df关联横向合并
df = dfn.append(df,ignore_index=True)  #两个df纵向合并，即追加数据

###排序
newdf = dfall.sort_values(by ='trade_date', axis=0, ascending=True)  #按一列给行排序，升序
df = df[['code', 'ts_code', 'trade_date', 'trade_time', 'time_index', 'open', 'high', 'low', 'close', 'amount', 'volume']]  #所有列重排序，没有出现的列将删掉

dfg = df.groupby(by = 'trade_date').mean()  #分组统计信息
dfg = dfall.groupby(by=['data_source', 'block_category', 'block_type', 'block_name', 'block_code'],as_index=False).count()  # 分组求每组数量
data_start_date = df.min()['trade_date']   #取一列的最小值
data_end_date = df.max()['trade_date']  #取一列的最大值

for trade_date in dfg['trade_date'].values:   #遍历列值

###条件过滤数据
df = df.where(df.notnull(), "")  #如果有字段存在none值，转为空字符串
dfg = dfg[dfg.volume == 0]  #条件过滤，保留满足条件的数据
df = df[(df['trade_date'] != trade_date)]  # #条件过滤，每个条件要用括号()括起来
df = df[(df['trade_date'] >= str(init_start_date)) & (df['trade_date'] <= str(init_end_date))]  #过滤掉start_date, end_date之外的数据，每个条件要用括号()括起来
"""

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