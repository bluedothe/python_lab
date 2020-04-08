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

import datetime
import time
import pandas as pd
from sqlalchemy import create_engine
from db.mysqlHelper import mysqlHelper
from stock_data import bluedothe
from stock_data import config
from stock_data.tushare_helper import TushareHelper
from stock_data import mysql_script
from tool import printHelper

class DataCollect:
    def __init__(self):
        #pandas数据显示设置
        pd.set_option('display.max_columns', None)  # 显示所有列
        pd.set_option('display.max_rows', None)   # 显示所有行

        #tushare对象
        self.tshelper = TushareHelper()

        # mysql对象
        self.mysql = mysqlHelper(config.mysql_host, config.mysql_username, bluedothe.mysql_password,
                                 config.mysql_dbname)

        # pandas的mysql对象
        db_paras = {"host": config.mysql_host, "user": config.mysql_username, "passwd": bluedothe.mysql_password,
                    "dbname": config.mysql_dbname}
        # self.engine = create_engine('mysql+pymysql://{user}:{passwd}@{host}/{dbname}?charset=utf8'.format(**db_paras))
        self.engine = create_engine(
            f'mysql+pymysql://{config.mysql_username}:{bluedothe.mysql_password}@{config.mysql_host}/{config.mysql_dbname}?charset=utf8')

    #通过tusharepro接口获取股票基本信息，使用pandas的to_sql入库，如果表存在则删除重建
    def get_stock_basic_pandas(self):
        self.tshelper.stock_basic_mysql_pandas("L","replace")
        self.tshelper.stock_basic_mysql_pandas("D")
        self.tshelper.stock_basic_mysql_pandas("P")

    # 通过tusharepro接口获取股票基本信息，使用pymysql入库，每次都需要先删除表后重新创建表
    def get_stock_basic_one(self):
        self.mysql.exec(mysql_script.drop_table_common.format("stock_basic"))
        self.mysql.exec(mysql_script.create_stock_basic)
        self.tshelper.stock_basic_mysql_one("L")
        self.tshelper.stock_basic_mysql_one("D")
        self.tshelper.stock_basic_mysql_one("P")

    #采集交易数据，tusharepro+tushare
    def get_stock_history(self):
        sql = "select ts_code from stock_basic"
        stock_basic_df = pd.read_sql(sql, self.engine, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None,chunksize=None)
        for ts_code in stock_basic_df['ts_code']:
            print(ts_code)
            self.tshelper.get_history_phase(ts_code)

    #采集交易数据，tusharepr
    def get_stock_history_pro(self):
        sql = "select ts_code from stock_basic"
        stock_basic_df = pd.read_sql(sql, self.engine, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None,chunksize=None)
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_type": "tushare_history_pro", "data_name": "tusharepro交易数据",
                 "data_source": "tusharepro", "collect_start_time": now, "collect_status": "R"}
        log_id = self.record_log(paras)

        for ts_code in stock_basic_df['ts_code']:
            time.sleep(0.5)
            self.tshelper.get_history_pro(ts_code)

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_end_date": "2020-04-03", "collect_end_time": now,
                 "collect_log": "一次完成到2020-04-03的所有交易数据", "collect_status": "S", "id": log_id}
        self.record_log(paras, False)

    def record_log(self,paras,is_insert = True):
        #paras = {"data_type":"tushare_history_all","data_name":"tushare交易数据，两个接口合并","data_source":"tusharepro+tushare","collect_start_time":"","collect_status":"R"}
        #paras = {"data_end_date":"","collect_end_time":"","collect_log":"sucess", "collect_status":"S","id":1}
        if is_insert:
            print(mysql_script.insert_collect_log.format(**paras))
            id = self.mysql.insert_one(mysql_script.insert_collect_log.format(**paras))
            return id
        else:
            self.mysql.exec(mysql_script.update_collect_log.format(**paras))

    #自动补齐交易历史数据
    @printHelper.time_this_function
    def get_history_by_date(self):
        # start_date = self.mysql.select("select max(data_end_date) from collect_log where data_type = 'tushare_history_all'")
        # start_date = self.mysql.select("select * from collect_log where data_type = %s",['tushare_history_all'])
        # start_date = self.mysql.select("select * from collect_log ")
        last_data_end_date = self.mysql.select("select max(data_end_date) from collect_log where data_type = %s",'tushare_history_all')
        start_date = last_data_end_date[0][0] + datetime.timedelta(days=1)
        today = datetime.datetime.now()
        end_date = today.strftime('%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_type": "tushare_history_all", "data_name": "tushare交易数据，两个接口合并",
                 "data_source": "tusharepro+tushare", "collect_start_time": now, "collect_status": "R"}
        log_id = self.record_log(paras)
        while start_date <= end_date:
            start_date_pro = start_date.strftime('%Y%m%d')
            #print(start_date_pro)
            self.tshelper.get_history_by_date(start_date_pro)
            start_date = start_date + datetime.timedelta(days=1)
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_end_date": str(end_date), "collect_end_time": now,
                 "collect_log": f"完成从{start_date}到{end_date}的数据采集", "collect_status": "S", "id": 3}
        self.record_log(paras, False)

    def test_record_log(self):
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        print(now)
        paras = {"data_type": "tushare_history_all", "data_name": "tushare交易数据，两个接口合并",
                 "data_source": "tusharepro+tushare", "collect_start_time": now, "collect_status": "R"}
        paras = {"data_end_date": "2020-04-03", "collect_end_time": now, "collect_log": "一次完成2017-10-09到2020-04-03的所有交易数据", "collect_status": "S", "id": 1}
        self.record_log(paras,False)

    #测试
    def string_format(self):
        paras = {"host":bluedothe.mysql_host, "user":bluedothe.mysql_username, "passwd":bluedothe.mysql_password, "dbname":bluedothe.mysql_dbname}
        str = 'mysql://{user}:{passwd}@{host}/{dbname}?charset=utf8'.format(**paras)
        print(str)
        print(datetime.now())

    # 测试
    def test(self):
        #sql="""INSERT INTO stock_basic(code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_date,delist_date,is_hs,create_time,update_time)
        #VALUES('688399.SH','688399','硕世生物','江苏','医疗保健','江苏硕世生物科技股份有限公司','Jiangsu Bioperfectus Technologies Co., Ltd.','科创板','SSE','CNY','20191205','None','N','2020-03-31 22:53:51','2020-03-31 22:53:51')"""
        values = []
        #sql = "INSERT INTO stock_basic(code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_date,delist_date,is_hs,create_time,update_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #values.append(('688399.SH','688399','硕世生物','江苏','医疗保健','江苏硕世生物科技股份有限公司','Jiangsu Bioperfectus Technologies Co., Ltd.','科创板','SSE','CNY','20191205','None','N','2020-03-31','2020-03-31'))
        #values.append(('688399.SH', '688399', '硕世生物', '江苏', '医疗保健', '江苏硕世生物科技股份有限公司','Jiangsu Bioperfectus Technologies Co., Ltd.', '科创板', 'SSE', 'CNY', '20191205', 'None', 'N','2020-03-31', '2020-03-31'))
        sql = "INSERT INTO stock_basic(code,symbol,area) VALUES ('688398.SH','688398','硕世生物'),('688398.SH','688398','硕世生物')"
        values.append(('688398.SH','688398','硕世生物'))
        values.append(('688399.SH','688399','硕世生物'))
        print(values)
        self.mysql.exec(sql)

if __name__ == '__main__':
    dc = DataCollect()
    #dc.get_stock_basic_pandas()
    #dc.get_stock_basic_one()
    #dc.test()
    #dc.get_stock_history()
    #dc.test_record_log()
    #dc.get_stock_history_pro()
    dc.get_history_by_date()