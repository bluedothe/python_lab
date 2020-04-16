#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/3/28
    通过通达信接口获取股票数据，参考资料：https://rainx.gitbooks.io/pytdx/content/pytdx_reader.html
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import os
import pandas as pd

from pytdx.hq import TdxHq_API,TDXParams
from pytdx.exhq import TdxExHq_API
from pytdx.config.hosts import hq_hosts
from sqlalchemy import create_engine

from db.mysqlHelper import mysqlHelper
from stock_data import bluedothe
from stock_data import config
from tool import printHelper
from tool import datatime_util

class TdxHelper:
    ip_list = [{'ip': '119.147.212.81', 'port': 7709},{'ip': '60.12.136.250', 'port': 7709}]

    def __init__(self):
        self.api = TdxHq_API()

        # pandas数据显示设置
        pd.set_option('display.max_columns', None)  # 显示所有列
        pd.set_option('display.max_rows', None)  # 显示所有行

        # mysql对象
        self.mysql = mysqlHelper(config.mysql_host, config.mysql_username, bluedothe.mysql_password,
                                 config.mysql_dbname)

        # pandas的mysql对象
        self.engine = create_engine(f'mysql+pymysql://{config.mysql_username}:{bluedothe.mysql_password}@{config.mysql_host}/{config.mysql_dbname}?charset=utf8')

    #获取k线
    def get_security_bars(self):
        if self.api.connect('119.147.212.81', 7709):
            #df = self.api.get_security_bars(9, 0, '000001', 0, 10)  # 返回普通list,五个参数分别为：category（k线),市场代码(深市),股票代码,开始时间,记录条数
            df = self.api.to_df(self.api.get_security_bars(9, 0, '000001', 0, 10))  # 返回DataFrame
            print(df)
            self.api.disconnect()

    #可以获取多只股票的行情信息
    def get_security_quotes(self):
        if self.api.connect('119.147.212.81', 7709):
            df = self.api.to_df(self.api.get_security_quotes([(0, '000001'), (1, '600300')]))
            print(df)
            self.api.disconnect()

    # 获取市场股票数量
    def get_security_count(self):
        if self.api.connect('119.147.212.81', 7709):
            df = self.api.to_df(self.api.get_security_count(0))  #0 - 深圳， 1 - 上海
            print(df)
            self.api.disconnect()

    # 获取股票列表
    def get_security_list(self):
        if self.api.connect('119.147.212.81', 7709):
            df = self.api.to_df(self.api.get_security_list(1, 0))  # 市场代码, 起始位置 如： 0,0 或 1,100
            print(df)
            self.api.disconnect()

    # 获取指数k线
    def get_index_bars(self):
        if self.api.connect('119.147.212.81', 7709):
            df = self.api.to_df(self.api.get_index_bars(9,1, '000001', 1, 2))
            print(df)
            self.api.disconnect()

    # 查询分时行情
    def get_minute_time_data(self):
        if self.api.connect('119.147.212.81', 7709):
            df = self.api.to_df(self.api.get_minute_time_data(1, '600300'))  #市场代码， 股票代码
            print(df)
            self.api.disconnect()

    # 查询历史分时行情
    def get_history_minute_time_data(self):
        if self.api.connect('119.147.212.81', 7709):
            df = self.api.to_df(self.api.get_history_minute_time_data(TDXParams.MARKET_SH, '600300', 20161209))  #市场代码， 股票代码，时间
            print(df)
            self.api.disconnect()

    # 查询分笔成交
    def get_transaction_data(self):
        if self.api.connect('119.147.212.81', 7709):
            df = self.api.to_df(self.api.get_transaction_data(TDXParams.MARKET_SZ, '000001', 0, 30))  #市场代码， 股票代码，起始位置， 数量
            print(df)
            self.api.disconnect()

    # 查询历史分笔成交
    def get_history_transaction_data(self):
        if self.api.connect('119.147.212.81', 7709):
            df = self.api.to_df(self.api.get_history_transaction_data(TDXParams.MARKET_SZ, '000001', 0, 10, 20170209))  #市场代码， 股票代码，起始位置，日期 数量
            print(df)
            self.api.disconnect()

    # 查询公司信息目录
    def get_company_info_category(self):
        if self.api.connect('119.147.212.81', 7709):
            df = self.api.to_df(self.api.get_company_info_category(TDXParams.MARKET_SZ, '000001'))  #市场代码， 股票代码
            print(df)
            self.api.disconnect()

    # 读取公司信息详情
    def get_company_info_content(self):
        if self.api.connect('119.147.212.81', 7709):
            df = self.api.to_df(self.api.get_company_info_content(0, '000001', '000001.txt', 0, 100))  #市场代码， 股票代码, 文件名, 起始位置， 数量
            print(df)
            self.api.disconnect()

    # 读取除权除息信息
    def get_xdxr_info(self):
        if self.api.connect('119.147.212.81', 7709):
            df = self.api.to_df(self.api.get_xdxr_info(1, '600300'))  #市场代码， 股票代码
            print(df)
            self.api.disconnect()

    # 读取财务信息
    def get_finance_info(self):
        if self.api.connect('119.147.212.81', 7709):
            df = self.api.to_df(self.api.get_finance_info(1, '600300'))  #市场代码， 股票代码
            print(df)
            self.api.disconnect()

    # 读取k线信息
    def get_k_data(self):
        if self.api.connect('119.147.212.81', 7709):
            df = self.api.to_df(self.api.get_k_data('000001','2017-07-03','2017-07-10'))  #股票代码， 开始时间， 结束时间
            print(df)
            self.api.disconnect()

    # 读取板块信息
    """   BLOCK_SZ = "block_zs.dat";BLOCK_FG = "block_fg.dat";BLOCK_GN = "block_gn.dat";BLOCK_DEFAULT = "block.dat"  """
    def get_and_parse_block_info(self):
        if self.api.connect('119.147.212.81', 7709):
            df = self.api.to_df(self.api.get_and_parse_block_info(TDXParams.BLOCK_DEFAULT))  #板块文件名称
            print(df)
            self.api.disconnect()

if __name__ == '__main__':
    tdx = TdxHelper()
    tdx.get_and_parse_block_info()