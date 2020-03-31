#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/3/28
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import pandas as pd
import tushare as ts
import datetime
import time
from stock_data import bluedothe

class TushareHelper:
    def __init__(self):
        self.pro = ts.pro_api(bluedothe.tushare_token)
        # 显示所有列
        pd.set_option('display.max_columns', None)
        # 显示所有行
        pd.set_option('display.max_rows', None)

    # 基础数据：获取股票列表
    def get_stock_basic(self):
        # data = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        data = self.pro.query('stock_basic', exchange='', list_status='L',
                         fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_date,delist_date,is_hs')
        #print(data)
        return data

    # 基础数据：交易日历
    # 1990年12月19日 上海证券交易所开市交易
    # 1991年07月03日 深圳证券交易所开市交易
    def get_trade_cal(self):
        #data = self.pro.trade_cal(exchange='SZSE', start_date='19901219')
        data = self.pro.query('trade_cal', start_date='20181201', end_date='20181231', fields='exchange,cal_date,is_open,pretrade_date')
        #print(data)
        for index, row in data.iterrows():
            print(index,"==",row["cal_date"])

    #判断某天是否为交易日
    def is_trade_day(self,datestr):
        date_str = "{}-{}-{}".format(datestr[0:4], datestr[4:6], datestr[6:8])
        y, m, d = date_str.split("-")
        my_date = datetime.date(int(y), int(m), int(d))
        result = True
        if ts.is_holiday(datetime.date.strftime(my_date, "%Y-%m-%d")):
            print(my_date,"不是交易日")
            result = False
        else:
            # 是交易日
            print(my_date,"是交易日")
        return result

if __name__ == '__main__':
    tshelper = TushareHelper()
    #tshelper.get_stock_basic()
    tshelper.get_trade_cal()
    #tshelper.is_trade_day("20200125")
