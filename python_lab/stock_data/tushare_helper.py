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
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, Float, Integer

from db.mysqlHelper import mysqlHelper
from stock_data import bluedothe
from tool import printHelper

class TushareHelper:
    def __init__(self):
        self.pro = ts.pro_api(bluedothe.tushare_token)

        # pandas数据显示设置
        pd.set_option('display.max_columns', None)  # 显示所有列
        pd.set_option('display.max_rows', None)  # 显示所有行

        # mysql对象
        self.mysql = mysqlHelper(bluedothe.mysql_host, bluedothe.mysql_username, bluedothe.mysql_password,
                                 bluedothe.mysql_dbname)

        # pandas的mysql对象
        db_paras = {"host": bluedothe.mysql_host, "user": bluedothe.mysql_username, "passwd": bluedothe.mysql_password,
                    "dbname": bluedothe.mysql_dbname}
        #self.engine = create_engine('mysql+pymysql://{user}:{passwd}@{host}/{dbname}?charset=utf8'.format(**db_paras))
        self.engine = create_engine(f'mysql+pymysql://{bluedothe.mysql_username}:{bluedothe.mysql_password}@{bluedothe.mysql_host}/{bluedothe.mysql_dbname}?charset=utf8')

    #将pandas.DataFrame中列名和预指定的类型映射
    # 此方法对VARCHAR的长度不能灵活定义，不具体通用性
    def mapping_df_types(df):
        dtypedict = {}
        for i, j in zip(df.columns, df.dtypes):
            if "object" in str(j):
                dtypedict.update({i: NVARCHAR(length=255)})
            if "float" in str(j):
                dtypedict.update({i: Float(precision=2, asdecimal=True)})
            if "int" in str(j):
                dtypedict.update({i: Integer()})
        return dtypedict

    # 基础数据：获取股票列表
    def get_stock_basic(self):
        # data = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        data = self.pro.query('stock_basic', exchange='', list_status='L',
                         fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_date,delist_date,is_hs')
        #print(data)
        return data

    #通过pandas入库
    def stock_basic_mysql_pandas(self):
        df = self.get_stock_basic()
        dtypedict = {
            'str': NVARCHAR(length=255),
            'int': Integer(),
            'float': Float(),
            'code': NVARCHAR(length=16), 'symbol': NVARCHAR(length=16), 'name': NVARCHAR(length=16), 'area': NVARCHAR(length=16), 'industry': NVARCHAR(length=16), 'fullname': NVARCHAR(length=16), 'enname': NVARCHAR(length=16), 'market': NVARCHAR(length=16), 'exchange': NVARCHAR(length=16), 'curr_type': NVARCHAR(length=16), 'list_date': NVARCHAR(length=16), 'delist_date': NVARCHAR(length=16), 'is_hs': NVARCHAR(length=16), 'create_time': NVARCHAR(length=16), 'update_time': NVARCHAR(length=255)
        }
        # dtypedict =self.mapping_df_types(df)   #此方法对VARCHAR的长度不能灵活定义，不具体通用性
        # df.to_sql('stock_basic_pd', self.engine)    # 存入数据库
        df.to_sql('stock_basic_pd', self.engine, if_exists='append', index=False, dtype=dtypedict)   # 追加数据到现有表

    #单条记录入库,存在none值的时候不能拼接字符串
    def stock_basic_mysql_one(self):
        df = self.get_stock_basic()
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = "INSERT INTO stock_basic(code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_date,delist_date,is_hs,create_time,update_time) VALUES" #('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"
        values = ""
        for index, row in df.iterrows():
            values.join("(" + row["ts_code"] + "," + row["symbol"] + "," + row["name"] + "," + row["area"] + "," + row["industry"] + "," + row["fullname"] + "," + row["enname"] + "," + row["market"] + "," + \
                           row["exchange"] + "," + row["curr_type"] + "," + row["list_date"] + "," + row["delist_date"] + "," + row["is_hs"] + "," + cur_time + "," + cur_time + "),")
        self.mysql.exec(sql.join(values))
        print("已完成插入{}条数据".format(len(values)))

    # 多条记录批量入库,执行报错：not enough arguments for format string
    @printHelper.time_this_function
    def stock_basic_mysql_many(self):
        df = self.get_stock_basic()
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        values = []
        sql = "INSERT INTO stock_basic(code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_date,delist_date,is_hs,create_time,update_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for index, row in df.iterrows():
            values.append((row["ts_code"], row["symbol"], row["name"], row["area"], row["industry"], row["fullname"], row["enname"], row["market"],
                           row["exchange"], row["curr_type"], row["list_date"], row["delist_date"], row["is_hs"], cur_time, cur_time))
        self.mysql.exec(sql,values)
        print("已完成插入{}条数据".format(len(values)))

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
    #tshelper.get_trade_cal()
    #tshelper.is_trade_day("20200125")
    tshelper.stock_basic_mysql_many()
