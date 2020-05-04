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
            f'mysql+mysqlconnector://{config.mysql_username}:{bluedothe.mysql_password}@{config.mysql_host}/{config.mysql_dbname}?charset=utf8')

    def tdx_close_connect(self):
        self.tdxhelper.close_connect()

    #获取板块成分股数据，直接通过pd插入数据库，每次插入前要清掉tdx相关的数据
    def update_block_member(self):
        data_type = 'tdx_block_member'
        today = datetime.datetime.now()
        today_str = today.strftime('%Y-%m-%d')

        last_data_end_date_record = self.mysql.select("select max(data_end_date) from collect_log where data_type = %s",data_type)
        last_data_end_date = last_data_end_date_record[0][0]  # last_data_end_date是日期类型
        if last_data_end_date == None:
            last_data_end_date = datatime_util.str2date(today_str) - datetime.timedelta(days=1)

        end_date = datetime.datetime.strptime(today_str, '%Y-%m-%d').date()  # end_date是日期类型
        if last_data_end_date >= end_date:  # 日志记录的
            print("今天的数据已经更新完成，不必重复执行!")
            return

        if self.tdxhelper.update_block_member():
            now = time.strftime("%Y-%m-%d %H:%M:%S")  # now是字符串
            today = time.strftime("%Y-%m-%d")
            paras = {"data_type": data_type, "data_name": "tdx板块成分股", "data_source": "tdx", "collect_start_time": now,
                     "data_end_date": today, "collect_end_time": now,  "collect_log": f"完成{data_type}的数据采集", "collect_status": "S"}
            print(paras)
            mysql_script.record_log(paras)
        else:
            print("=======没有要更新的板块成分股========")

    #增加分钟数据
    #第一个参数，如果没有数据库日志记录，也就是本函数第一次执行，需要制定默认开始时间；第二个参数指定一个时间，对这个时间之后更新的文件不处理
    #两个参数的格式都为'%Y-%m-%d'字符串格式,last_file_modify_time不指定则不校验
    def append_minite1_all(self,default_start_date = "", file_modify_time_flag = ""):
        data_type = 'tdx_minline1'
        today = datetime.datetime.now()
        today_str = today.strftime('%Y-%m-%d')

        last_data_end_date_record = self.mysql.select("select max(data_end_date) from collect_log where data_type = %s",data_type)
        last_data_end_date = last_data_end_date_record[0][0]   #last_data_end_date是日期类型
        if last_data_end_date == None:
            last_data_end_date = datatime_util.str2date(default_start_date) - datetime.timedelta(days=1)

        end_date = datetime.datetime.strptime(today_str, '%Y-%m-%d').date()  #end_date是日期类型
        if last_data_end_date >= end_date:    #日志记录的
            print("今天的数据已经更新完成，不必重复执行!")
            return

        records = self.mysql.select("select ts_code from stock_basic where list_status='L'")
        if len(records) == 0: return

        now = time.strftime("%Y-%m-%d %H:%M:%S")      #now是字符串
        paras = {"data_type": data_type, "data_name": "tdx1分钟数据",
                 "data_source": "tdx", "collect_start_time": now, "collect_status": "R"}
        log_id = mysql_script.record_log(paras, flag = 'before')

        market = {'SZ': 0, 'SH': 1}
        for stock in records:
            ts_code = stock[0]
            filename = config.tdx_csv_minline1_all + ts_code + ".csv"
            if os.path.isfile(filename):
                #获取文件更新时间，更新时间在某个时间之后的忽略
                if len(file_modify_time_flag) > 0:
                    mtime = os.stat(filename).st_mtime
                    file_modify_time = time.strftime('%Y-%m-%d', time.localtime(mtime))  #file_modify_time是字符串
                    if file_modify_time > file_modify_time_flag:continue

                #获取csv文件中数据的最后日期，如果该日期大于或等于end_date则说明数据已经完成采集，忽略该文件；
                #如果csv文件中数据的最后日期大于从数据库日志中获取的上次更新日期last_data_end_date，则修改last_data_end_date为文件中的最后日期
                df = pd.read_csv(filename)
                last_file_end_date = df.max()['trade_date']  #last_file_end_date是int类型
                if last_file_end_date >= int(str(end_date).replace('-', '')):continue
                if last_file_end_date >= int(str(last_data_end_date).replace('-', '')):
                    start_date = datetime.date(year=int((str(last_file_end_date))[0:4]), month=int((str(last_file_end_date))[4:6]), day=int((str(last_file_end_date))[6:8])) + datetime.timedelta(days=1)
                else:
                    start_date = last_data_end_date + datetime.timedelta(days=1)
            else:
                start_date = last_data_end_date + datetime.timedelta(days=1)
            self.tdxhelper.get_minute1_data(7, market[ts_code[7:9]],ts_code[0:6], str(start_date), str(end_date))

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_end_date": str(end_date), "collect_end_time": now, "collect_log": f"完成{end_date}的数据采集", "collect_status": "S", "id": log_id}
        mysql_script.record_log(paras, flag = 'after')

        print("--------追加tdx1分钟数据初始化完成------------")

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
        log_id = mysql_script.record_log(paras, flag = 'before')

        file_util.traversal_dir(config.tdx_local_sh_minline1, self.tdx_local_helper.read_tdx_local_minline_all)
        file_util.traversal_dir(config.tdx_local_sz_minline1, self.tdx_local_helper.read_tdx_local_minline_all)

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_end_date": str(end_date), "collect_end_time": now,
                 "collect_log": f"一次性完成从{start_date}到{end_date}的数据采集", "collect_status": "S", "id": log_id}
        mysql_script.record_log(paras, flag = 'after')

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
        log_id = mysql_script.record_log(paras, flag = 'before')

        file_util.traversal_dir(config.tdx_local_sh_minline1, self.tdx_local_helper.read_tdx_local_minline_simple)
        file_util.traversal_dir(config.tdx_local_sz_minline1, self.tdx_local_helper.read_tdx_local_minline_simple)

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_end_date": str(end_date), "collect_end_time": now,
                 "collect_log": f"一次性完成从{start_date}到{end_date}的数据采集", "collect_status": "S", "id": log_id}
        mysql_script.record_log(paras, flag = 'after')

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
        self.append_minite1_all(default_start_date = "2020-01-12", file_modify_time_flag = "")
        self.update_block_member()   #更新板块成分股和板块基本信息两张表

if __name__ == '__main__':
    dc = TdxDataCollect()
    #dc.batch_execute_everyday()
    #dc.execute_insert_tdx_index()
    dc.update_block_member()
    dc.tdx_close_connect()