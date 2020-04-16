#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/4/15
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

from pytdx.reader import TdxDailyBarReader,TdxLCMinBarReader, TdxFileNotFoundException,BlockReader
from pytdx import BlockReader_TYPE_GROUP
import os
import pandas as pd

from stock_data import config

class TdxLocalHelper:
    def __init__(self):
        # pandas数据显示设置
        pd.set_option('display.max_columns', None)  # 显示所有列
        pd.set_option('display.max_rows', None)  # 显示所有行

    # 通过读取通达信的软件本地目录导出的数据
    def read_tdx_local_sz_day(self):
        reader = TdxDailyBarReader()
        df = reader.get_df(config.tdx_local_sz_day + "sz000001.day")
        print(df)

    # 通过读取通达信的软件本地目录导出的数据
    def read_tdx_local_sz_minline(self):
        reader = TdxLCMinBarReader()
        df = reader.get_df(config.tdx_local_sz_minline + "sz000001.lc1")
        print(df)

    # 通过读取通达信的软件本地目录导出的数据
    def read_tdx_local_sz_minline(self):
        df = BlockReader().get_df(config.tdx_local_block + "block_zs.dat")   # 默认扁平格式
        df2 = BlockReader().get_df("/Users/rainx/tmp/block_zs.dat", BlockReader_TYPE_GROUP)   #分组格式
        print(df)

if __name__ == '__main__':
    tdx = TdxLocalHelper()
    tdx.read_tdx_local_sz_minline()