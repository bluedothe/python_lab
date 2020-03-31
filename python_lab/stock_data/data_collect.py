#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/3/28
    参考资料：http://blog.sina.com.cn/s/blog_154861eae0102xc8d.html
    https://www.jianshu.com/p/5065aa3b3026
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

from _datetime import datetime
import time
import pandas as pd
from sqlalchemy import create_engine
from db.mysqlHelper import mysqlHelper
from stock_data import bluedothe
from stock_data.tushare_helper import TushareHelper

class DataCollect:
    def __init__(self):
        # 显示所有列
        pd.set_option('display.max_columns', None)
        # 显示所有行
        pd.set_option('display.max_rows', None)
        self.mysql = mysqlHelper(bluedothe.mysql_host, bluedothe.mysql_username, bluedothe.mysql_password, bluedothe.mysql_dbname)
        db_paras = {"host": bluedothe.mysql_host, "user": bluedothe.mysql_username, "passwd": bluedothe.mysql_password,
                    "dbname": bluedothe.mysql_dbname}
        self.engine = create_engine('mysql+pymysql://{user}:{passwd}@{host}/{dbname}?charset=utf8'.format(**db_paras))
        self.tshelper = TushareHelper()

    def get_stock_basic(self):
        df = self.tshelper.get_stock_basic()

        # 存入数据库
        #df.to_sql('stock_basic_pd', self.engine)
        # 追加数据到现有表
        #df.to_sql('stock_basic_pd', self.engine, if_exists='append')

        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = "INSERT INTO stock_basic(code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_date,delist_date,is_hs,create_time,update_time) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"
        for index, row in df.iterrows():
            self.mysql.exec(sql.format(row["ts_code"],row["symbol"],row["name"],row["area"],row["industry"],row["fullname"],row["enname"],row["market"],row["exchange"],row["curr_type"],row["list_date"],row["delist_date"],row["is_hs"],cur_time,cur_time))
            #self.mysql.exec("INSERT INTO stock_basic('code','symbol','name','area','industry','fullname','enname','market','exchange','curr_type','list_date','delist_date','is_hs','create_time','update_time') VALUES(row['ts_code'],row['symbol'],row['name'],row['area'],row['industry'],row['fullname'],row['enname'],row['market'],row['exchange'],row['curr_type'],row['list_date'],row['delist_date'],row['is_hs'],datetime.now(),datetime.now())")
            print("已完成插入{}条数据".format(index))

    def string_format(self):
        paras = {"host":bluedothe.mysql_host, "user":bluedothe.mysql_username, "passwd":bluedothe.mysql_password, "dbname":bluedothe.mysql_dbname}
        str = 'mysql://{user}:{passwd}@{host}/{dbname}?charset=utf8'.format(**paras)
        print(str)
        print(datetime.now())

    def test(self):
        sql="""INSERT INTO stock_basic(code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_date,delist_date,is_hs,create_time,update_time)
        VALUES('688399.SH','688399','硕世生物','江苏','医疗保健','江苏硕世生物科技股份有限公司','Jiangsu Bioperfectus Technologies Co., Ltd.','科创板','SSE','CNY','20191205','None','N','2020-03-31 22:53:51','2020-03-31 22:53:51')"""
        self.mysql.exec(sql)

if __name__ == '__main__':
    dc = DataCollect()
    dc.get_stock_basic()
    #dc.string_format()
    #dc.test()