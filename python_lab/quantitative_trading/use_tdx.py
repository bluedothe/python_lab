#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/2/14
    获取通达信的交易数据
    pytdx工具是在线获取交易数据的工具，开发文档：https://rainx.gitbooks.io/pytdx/content/pytdx_hq.html
'''

import os
from struct import unpack
import datetime
import time
import re
from pytdx.hq import TdxHq_API,TDXParams
from pytdx.reader import TdxDailyBarReader, TdxFileNotFoundException,BlockReader

__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"


# 将通达信的日线文件转换成CSV格式
def day2csv(source_dir, file_name, target_dir):
    # 以二进制方式打开源文件
    source_file = open(source_dir + os.sep + file_name, 'rb')
    buf = source_file.read()
    source_file.close()

    # 打开目标文件，后缀名为CSV
    target_file = open(target_dir + os.sep + file_name + '.csv', 'w')
    buf_size = len(buf)
    rec_count = buf_size // 32
    begin = 0
    end = 32
    header = str('date') + ', ' + str('open') + ', ' + str('high') + ', ' + str('low') + ', ' \
             + str('close') + ', ' + str('amount') + ', ' + str('vol') + ', ' + str('str07') + '\n'
    target_file.write(header)
    for i in range(rec_count):
        # 将字节流转换成Python数据格式
        # I: unsigned int
        # f: float
        a = unpack('IIIIIfII', buf[begin:end])
        line = str(a[0]) + ', ' + str(a[1] / 100.0) + ', ' + str(a[2] / 100.0) + ', ' \
               + str(a[3] / 100.0) + ', ' + str(a[4] / 100.0) + ', ' + str(a[5] / 10.0) + ', ' \
               + str(a[6]) + ', ' + str(a[7]) + ', ' + '\n'
        target_file.write(line)
        begin += 32
        end += 32
    target_file.close()

#读取通达信数据文件
def stock_csv(filepath, name):
    source = os.getcwd() + "/tdx_file/"
    data = []
    with open(filepath, 'rb') as f:
        file_object_path = source +  name +'.csv'
        file_object = open(file_object_path, 'w+')
        while True:
            stock_date = f.read(4)
            stock_open = f.read(4)
            stock_high = f.read(4)
            stock_low= f.read(4)
            stock_close = f.read(4)
            stock_amount = f.read(4)
            stock_vol = f.read(4)
            stock_reservation = f.read(4)

            # date,open,high,low,close,amount,vol,reservation

            if not stock_date:
                break
            stock_date = unpack("l", stock_date)     # 4字节 如20091229
            stock_open = unpack("l", stock_open)     #开盘价*100
            stock_high = unpack("l", stock_high)     #最高价*100
            stock_low= unpack("l", stock_low)        #最低价*100
            stock_close = unpack("l", stock_close)   #收盘价*100
            stock_amount = unpack("f", stock_amount) #成交额
            stock_vol = unpack("l", stock_vol)       #成交量
            stock_reservation = unpack("l", stock_reservation) #保留值

            date_format = datetime.datetime.strptime(str(stock_date[0]),'%Y%M%d') #格式化日期
            list= date_format.strftime('%Y-%M-%d')+","+str(stock_open[0]/100)+","+str(stock_high[0]/100.0)+","+str(stock_low[0]/100.0)+","+str(stock_close[0]/100.0)+","+str(stock_amount[0]/10.0)+","+str(stock_vol[0])+","+str(stock_reservation[0])+"\r\n"
            file_object.writelines(list)
        file_object.close()



#通过pytdx工具在线获取k线数据
"""
category,K线种类
0 5分钟K线 1 15分钟K线 2 30分钟K线 3 1小时K线 4 日K线
5 周K线
6 月K线
7 1分钟
8 1分钟K线 9 日K线
10 季K线
11 年K线
"""
def get_kline_data():
    api = TdxHq_API()
    if api.connect('119.147.212.81', 7709):
        data = api.get_security_bars(9, 0, '000001', 0, 10)  # 返回普通list,五个参数分别为：category（k线),市场代码(深市),股票代码,开始时间,记录条数
        print(data)
        data = api.to_df(api.get_security_bars(9, 0, '000001', 0, 10))  # 返回DataFrame
        print(data)
        api.disconnect()

#通过pytdx工具在线获取股票数量
# 市场代码,0 - 深圳， 1 - 上海
def get_stock_count():
    api = TdxHq_API()
    if api.connect('119.147.212.81', 7709):
        print(api.get_security_count(0))    #参数为市场代码
        print(api.get_security_list(0, 0))   #第一个参数为市场代码，第二个参数为起始位置
        print(api.get_security_count(1))
        print(api.get_security_list(1, 0))
        api.disconnect()

#查询公司信息目录
def get_company_info():
    api = TdxHq_API()
    if api.connect('119.147.212.81', 7709):
        print(api.get_company_info_category(TDXParams.MARKET_SZ, '000001'))   #查询公司信息目录,参数：市场代码， 股票代码
        api.get_company_info_content(0, '000001', os.getcwd() + "/tdx_file/" + '000001.txt', 0, 100)    #读取公司信息详情，参数文件路径不知干什么
        print(api.get_finance_info(0, '000001'))   #读取财务信息
        api.disconnect()

#获取板块信息,板块相关参数
""""BLOCK_SZ = "block_zs.dat"
BLOCK_FG = "block_fg.dat"
BLOCK_GN = "block_gn.dat"
BLOCK_DEFAULT = "block.dat"""""
def get_block_info():
    api = TdxHq_API()
    if api.connect('119.147.212.81', 7709):
        print(api.get_and_parse_block_info("block.dat"))  #一般板块
        print(api.get_and_parse_block_info("block_zs.dat"))  #指数板块
        print(api.get_and_parse_block_info("block_fg.dat"))  #风格板块
        print(api.get_and_parse_block_info("block_gn.dat"))  #概念板块
        api.disconnect()

#读取通达信软件下载的板块数据文件
def get_block_info2():
    # 默认扁平格式
    df = BlockReader().get_df(".../T0002/hq_cache/block_zs.dat")
    print(df)

#通过读取通达信的软件本地目录导出的数据
def read_tdx_file():
    source = os.getcwd() + "/tdx_file/"
    reader = TdxDailyBarReader()
    df = reader.get_df(source + "sz000001.day")
    print(df)
    df.to_csv(source + "/sz000001.csv")

def test():
    source = os.getcwd() + "/tdx_file/"
    target = os.getcwd() + "/tdx_file/"
    file_list = os.listdir(source)
    for f in file_list:
        day2csv(source, f, target)


if __name__ == '__main__':
    #test()
    #get_kline_data()
    #get_stock_count()
    #get_company_info()
    #get_block_info()
    #read_tdx_file()
    #stock_csv(os.getcwd() + "/tdx_file/sz000001.day","sz000001-2.csv")
    #get_block_info2()
    get_kline_data()