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

    def get_minite(self):
        pass

    # 初始化分钟数据
    @printHelper.time_this_function
    def get_init_minite(self):
        last_data_end_date = self.mysql.select("select max(data_end_date) from collect_log where data_type = %s",
                                               'tdx_minline1')
        if last_data_end_date[0][0] == None:
            start_date = datatime_util.str2date("2020-01-13")
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

        file_util.traversal_dir(config.tdx_local_sh_minline1, self.tdx_local_helper.read_tdx_local_minline)
        file_util.traversal_dir(config.tdx_local_sz_minline1, self.tdx_local_helper.read_tdx_local_minline)

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_end_date": str(end_date), "collect_end_time": now,
                 "collect_log": f"一次性完成从{start_date}到{end_date}的数据采集", "collect_status": "S", "id": log_id}
        mysql_script.record_log(paras, False)

        print("--------tushare_index大盘指数追加完成------------")

if __name__ == '__main__':
    pass