#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/4/15
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

from pytdx.reader import TdxDailyBarReader,TdxMinBarReader,TdxLCMinBarReader, TdxFileNotFoundException,BlockReader
import os
import pandas as pd
from struct import unpack
import chardet
import numpy as np

from stock_data import config
from tool import datatime_util

class TdxLocalHelper:
    BlockReader_TYPE_FLAT = 0
    BlockReader_TYPE_GROUP = 1

    def __init__(self):
        self.day_reader = TdxDailyBarReader()
        self.minline_reader = TdxLCMinBarReader()
        self.block_reader = BlockReader()

        # pandas数据显示设置
        pd.set_option('display.max_columns', None)  # 显示所有列
        #pd.set_option('display.max_rows', None)  # 显示所有行

    # 解析日线文件数据
    #返回值：date:open,high,low,close,amount,volume
    def read_tdx_local_day(self):
        #df = reader.get_df(config.tdx_local_sz_day + "sz000001.day")   sh000001.day
        df = self.day_reader.get_df(config.tdx_local_sh_day + "sh000001.day")
        print(df)

    # 解析1分钟和5分钟数据
    #返回值：date: ope,high,low,close,amount,volume
    def read_tdx_local_minline(self, full_path,filename=""):
        #df = reader.get_df(config.tdx_local_sz_minline1 + "sz399001.lc1")
        #df = reader.get_df(config.tdx_local_sz_minline5 + "sz399001.lc5")
        #df = self.minline_reader.get_df(config.tdx_local_sh_minline1 + "sh600300.lc1")
        ts_code = filename[2:8] + "." + filename[0:2].upper()
        code = filename[2:8]
        df = self.minline_reader.get_df(full_path)

        df.insert(0, 'trade_time', df.index)
        df.insert(0, 'trade_date', df.index.floor('D'))
        df.insert(0, 'ts_code', ts_code)
        df.insert(0, 'code', code)
        df.insert(0, 'trade_date_time', df.index)
        df.reset_index(drop=True,inplace=True)  #参考：https://zhuanlan.zhihu.com/p/110819220?from_voters_page=true
        df.insert(5, 'time_index', df.index)
        #df['trade_time'] = pd.to_datetime(df['trade_time'], infer_datetime_format=True).dt.normalize()  # strftime('%m/%d/%Y') # format='%m/%d/%Y').dt.date
        #df['trade_time'] = df['trade_time'].apply(lambda x: x.strftime('%H:%M:%S'))
        df['trade_time'] = pd.to_datetime(df['trade_time'], format='%H:%M:%S').dt.strftime('%H:%M:%S')
        df['time_index'] = df['trade_time'].apply(lambda x: datatime_util.stockTradeTime2Index(x))

        csv_filename = config.tdx_csv_minline1 + filename[2:8] + "." + filename[0:2].upper() + ".csv"
        if os.path.isfile(csv_filename):
            os.remove(csv_filename)
            df.to_csv(csv_filename, index=False, mode='w', header=True, sep=',', encoding="utf_8_sig")
        else:
            df.to_csv(csv_filename, index=False, mode='w', header=True, sep=',', encoding="utf_8_sig")

    # 解析板块数据
    #扁平格式返回值：blockname,block_type,code_index,code
    def read_tdx_local_block(self):
        ##指数板块 风格板块  概念板块  一般板块
        block_filename = ["block_zs.dat", "block_fg.dat", "block_gn.dat", "block.dat"]
        for block in block_filename:
            df = self.block_reader.get_df(config.tdx_local_block + block)   # 默认扁平格式
            df_group = self.block_reader.get_df(config.tdx_local_block + block, self.BlockReader_TYPE_GROUP)   #分组格式
            filename = config.tdx_csv_block + block[0:-4] + ".csv"
            filename_group = config.tdx_csv_block + block[0:-4] + "_group" + ".csv"
            if os.path.isfile(filename):
                df.to_csv(filename, index=False, mode='a', header=False, sep=',', encoding="utf_8_sig")
                df_group.to_csv(filename_group, index=False, mode='a', header=False, sep=',', encoding="utf_8_sig")
            else:
                df.to_csv(filename, index=False, mode='w', header=True, sep=',', encoding="utf_8_sig")
                df_group.to_csv(filename_group, index=False, mode='w', header=True, sep=',', encoding="utf_8_sig")

    # 解析分时图数据
    def read_tdx_local_fst(self):
        reader = TdxMinBarReader()  #这个reader不能解析分时图文件
        # df = reader.get_df(config.tdx_local_sz_minline + "sz399001.lc1")
        df = reader.get_df(config.tdx_local_fst + "sh20200417.tfz")
        print(df)

    # 解析分时图文件,没有解析出来
    """
    通达信的zst的数据记录是每6508个字节为一天的数据,
    每26个字节为一个分钟的记录,这26个字节是这样分配的,
    时间占两个字节化为十进制为570的话表示9:30分(570/60=9.5) 
    下一个是占四个字节的叫现价,
    再下四个字节叫均价,
    另外还有两个字节为该分钟成交量(现在有可能已经改为四个字节),
    剩下的14个字节是预留的,
    """
    def parse_fst_file(self):
        full_path = config.tdx_local_fst + "sh20200417.tfz"
        filesize = os.path.getsize(full_path)  # 文件字节数
        print("filesize为: %s" % (filesize))
        if filesize == 0: return

        #print(chardet.detect(open(full_path, mode='rb').read()))   #查看文件编码格式

        file = open(full_path, "rb")
        try:
            i = 0
            while True:
                print("游标位置：", file.tell())
                stock_date = file.read(2)
                cur_price = file.read(4)
                arr_price = file.read(4)
                vol = file.read(4)
                stock_reservation = file.read(12)
                stock_date = unpack("h", stock_date)
                cur_price = unpack("l", cur_price)
                arr_price = unpack("l", arr_price)
                vol = unpack("l", vol)
                #stock_reservation = unpack("s", stock_reservation)
                print(stock_date)
                print(cur_price)
                print(arr_price)
                print(vol)
                print(stock_reservation)
                i = i + 1
                if i == 2:break

            for line in file:
                result = chardet.detect(line)
                print("code: ", result)

                buf_size = len(line)
                rec_count = buf_size // 32
                begin = 0
                end = 32
                print("行内容：", line)
                print("buf_size：", buf_size)
                print("rec_count：", rec_count)
                a = unpack('IIIIIfII', line[begin:end])
                print("解码后的数据0: %s" % (str(a[0])))
                print("解码后的数据1: %s" % (str(a[1])))
                print("解码后的数据2: %s" % (str(a[2])))
                break
        finally:
            file.close()

if __name__ == '__main__':
    tdx = TdxLocalHelper()
    #tdx.read_tdx_local_minline(config.tdx_local_sz_minline1 + "sz000001.lc1","sz000001.lc1")