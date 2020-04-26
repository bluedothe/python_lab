#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/4/19
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import os
import datetime
import time
import pandas as pd
import chardet
import csv
from sqlalchemy import create_engine
from db.mysqlHelper import mysqlHelper
from stock_data import bluedothe
from stock_data import config
from stock_data.tdx_helper import TdxHelper
from stock_data.tdx_local_helper import TdxLocalHelper
from stock_data import mysql_script
from tool import printHelper
from tool import file_util
from tool import datatime_util

class TdxDataCollect:
    def __init__(self):
        #pandas数据显示设置
        pd.set_option('display.max_columns', None)  # 显示所有列
        pd.set_option('display.max_rows', None)   # 显示所有行

        # tushare对象
        self.tdxhelper = TdxHelper()
        self.tdx_local_helper = TdxLocalHelper()

        # mysql对象
        self.mysql = mysqlHelper(config.mysql_host, config.mysql_username, bluedothe.mysql_password,
                                 config.mysql_dbname)

        # pandas的mysql对象
        db_paras = {"host": config.mysql_host, "user": config.mysql_username, "passwd": bluedothe.mysql_password,
                    "dbname": config.mysql_dbname}
        # self.engine = create_engine('mysql+pymysql://{user}:{passwd}@{host}/{dbname}?charset=utf8'.format(**db_paras))
        self.engine = create_engine(
            f'mysql+pymysql://{config.mysql_username}:{bluedothe.mysql_password}@{config.mysql_host}/{config.mysql_dbname}?charset=utf8')

    def get_block(self):
        pass

    def append_minite1_all(self):
        data_type = 'tdx_minline1'
        today = datetime.datetime.now()
        today_str = today.strftime('%Y-%m-%d')

        last_data_end_date = self.mysql.select("select max(data_end_date) from collect_log where data_type = %s",data_type)
        if last_data_end_date[0][0] == None:
            start_date = today_str
        else:
            start_date = last_data_end_date[0][0] + datetime.timedelta(days=1)

        end_date = datetime.datetime.strptime(today_str, '%Y-%m-%d').date()
        if start_date > end_date:
            print("今天的数据已经更新完成，不必重复执行!")
            return

        records = self.mysql.select("select ts_code from stock_basic where list_status='L'")
        if len(records) == 0: return

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_type": data_type, "data_name": "tdx1分钟数据",
                 "data_source": "tdx", "collect_start_time": now, "collect_status": "R"}
        log_id = mysql_script.record_log(paras)

        market = {'SZ': 0, 'SH': 1}
        for stock in records:
            ts_code = stock[0]
            filename = config.tdx_csv_minline1_all + ts_code + ".csv"
            if os.path.isfile(filename):
                df = pd.read_csv(filename)
                last_file_end_date = df.max()['trade_date']
                if last_file_end_date >= int(str(end_date).replace('-', '')):break
                if last_file_end_date >= int(str(start_date).replace('-', '')):
                    fact_start_date = datetime.date(year=int((str(last_file_end_date))[0:4]), month=int((str(last_file_end_date))[4:6]), day=int((str(last_file_end_date))[6:8])) + datetime.timedelta(days=1)
                else:
                    fact_start_date = start_date
            else:
                fact_start_date = start_date
            self.tdxhelper.get_minute1_data(7, market[ts_code[7:9]],ts_code[0:6], str(fact_start_date), str(end_date))
        self.tdxhelper.close_connect()

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_end_date": str(end_date), "collect_end_time": now, "collect_log": f"一次性完成从{start_date}到{end_date}的数据采集", "collect_status": "S", "id": log_id}
        mysql_script.record_log(paras, False)

        print("--------追加tdx1分钟数据初始化完成------------")

    def append_minite1_simple(self):
        pass

    # 初始化分钟数据
    @printHelper.time_this_function
    def get_init_minite1_all(self):
        last_data_end_date = self.mysql.select("select max(data_end_date) from collect_log where data_type = %s",'tdx_minline1')
        if last_data_end_date[0][0] == None:
            start_date = datatime_util.str2date('2020-01-13')
        else:
            start_date = last_data_end_date[0][0] + datetime.timedelta(days=1)
        today = datetime.datetime.now()
        end_date = today.strftime('%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        if start_date > end_date:
            print("今天的数据已经更新完成，不必重复执行!")
            return

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_type": "tdx_minline1", "data_name": "tdx1分钟数据",
                 "data_source": "tdx_local", "collect_start_time": now, "collect_status": "R"}
        log_id = mysql_script.record_log(paras)

        file_util.traversal_dir(config.tdx_local_sh_minline1, self.tdx_local_helper.read_tdx_local_minline_all)
        file_util.traversal_dir(config.tdx_local_sz_minline1, self.tdx_local_helper.read_tdx_local_minline_all)

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_end_date": str(end_date), "collect_end_time": now,
                 "collect_log": f"一次性完成从{start_date}到{end_date}的数据采集", "collect_status": "S", "id": log_id}
        mysql_script.record_log(paras, False)

        print("--------tdx1分钟数据初始化完成------------")

    # 初始化分钟数据
    @printHelper.time_this_function
    def get_init_minite1_simple(self):
        last_data_end_date = self.mysql.select("select max(data_end_date) from collect_log where data_type = %s",'tdx_minline1_simple')
        if last_data_end_date[0][0] == None:
            start_date = datatime_util.str2date('2020-01-13')
        else:
            start_date = last_data_end_date[0][0] + datetime.timedelta(days=1)
        today = datetime.datetime.now()
        end_date = today.strftime('%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        if start_date > end_date:
            print("今天的数据已经更新完成，不必重复执行!")
            return

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_type": "tdx_minline1_simple", "data_name": "tdx1分钟数据",
                 "data_source": "tdx_local", "collect_start_time": now, "collect_status": "R"}
        log_id = mysql_script.record_log(paras)

        file_util.traversal_dir(config.tdx_local_sh_minline1, self.tdx_local_helper.read_tdx_local_minline_simple)
        file_util.traversal_dir(config.tdx_local_sz_minline1, self.tdx_local_helper.read_tdx_local_minline_simple)

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_end_date": str(end_date), "collect_end_time": now,
                 "collect_log": f"一次性完成从{start_date}到{end_date}的数据采集", "collect_status": "S", "id": log_id}
        mysql_script.record_log(paras, False)

        print("--------tdx1分钟数据初始化完成------------")

    #tdx指数基本信息入库，遍历分钟数据目录，文件名称在股票基本信息中的忽略，不再的加入指数信息表中
    def insert_tdx_index(self, full_path, filename):
        code = filename[0:6]
        ts_code = filename[0:9]
        market = filename[7:9].upper()

        select_sql = "select * from stock_basic where ts_code = '{}'"
        record = self.mysql.select(select_sql.format(ts_code))
        if len(record) == 0:
            paras = {'code':code,'ts_code':ts_code,'market':market,'name':''}
            self.mysql.insert_one(mysql_script.insert_index_basic.format(**paras))

    #遍历目录，插入指数数据
    @printHelper.time_this_function
    def execute_insert_tdx_index(self):
        file_util.traversal_dir(config.tdx_csv_minline1_all, self.insert_tdx_index)

    #删除无用的指数数据,临时执行一次
    def delete_index_file(self):
        select_sql = "SELECT ts_code from index_basic where LENGTH(name)=0"
        records = self.mysql.select(select_sql)
        for recode in records:
            path = config.tdx_csv_minline1_all + recode[0] + '.csv'
            os.remove(path)

    #每天批量执行更新数据
    def batch_execute_everyday(self):
        self.append_minite1_all()

if __name__ == '__main__':
    dc = TdxDataCollect()
    dc.batch_execute_everyday()
    #dc.execute_insert_tdx_index()