#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/4/15
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

from pytdx.reader import TdxDailyBarReader, TdxFileNotFoundException,BlockReader
import os

class TdxLocalHelper:
    def __init__(self):
        pass

    # 通过读取通达信的软件本地目录导出的数据
    def read_tdx_file(self):
        source = os.getcwd() + "/tdx_file/"
        reader = TdxDailyBarReader()
        df = reader.get_df(source + "sz000001.day")
        print(df)
        df.to_csv(source + "/sz000001.csv")

if __name__ == '__main__':
    pass