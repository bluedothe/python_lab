#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/5/6
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import datetime
import time
import pandas as pd
from sqlalchemy import create_engine

from db.mysqlHelper import mysqlHelper
from config import config, bluedothe
from stock_data.ths_helper import ThsHelper
from stock_data import mysql_script
from tool import datatime_util

class ThsDataCollect:
    def __init__(self):
        #pandas数据显示设置
        pd.set_option('display.max_columns', None)  # 显示所有列
        pd.set_option('display.max_rows', None)   # 显示所有行

        # tushare对象
        self.thsHelper = ThsHelper()

        # mysql对象
        self.mysql = mysqlHelper(config.mysql_host, config.mysql_username, bluedothe.mysql_password,
                                 config.mysql_dbname)

        # pandas的mysql对象
        db_paras = {"host": config.mysql_host, "user": config.mysql_username, "passwd": bluedothe.mysql_password,
                    "dbname": config.mysql_dbname}
        # self.engine = create_engine('mysql+pymysql://{user}:{passwd}@{host}/{dbname}?charset=utf8'.format(**db_paras))
        self.engine = create_engine(
            f'mysql+mysqlconnector://{config.mysql_username}:{bluedothe.mysql_password}@{config.mysql_host}/{config.mysql_dbname}?charset=utf8')

    #追加日线附加数据,只能获取当天的数据，不能后补
    def update_day_attach(self, trade_date = ""):
        data_type = 'ths_day_attach'
        today = datetime.datetime.now()
        today_str = today.strftime('%Y-%m-%d')
        if len(trade_date) == 0: trade_date = time.strftime("%Y%m%d")  # 如果没指定交易日期则用当天日期

        last_data_end_date_record = self.mysql.select("select max(data_end_date) from collect_log where data_type = %s",
                                                      data_type)
        last_data_end_date = last_data_end_date_record[0][0]  # last_data_end_date是日期类型
        if last_data_end_date == None:
            last_data_end_date = datatime_util.str2date(today_str) - datetime.timedelta(days=1)

        end_date = datetime.datetime.strptime(today_str, '%Y-%m-%d').date()  # end_date是日期类型
        if last_data_end_date >= end_date:  # 日志记录的
            print("今天的数据已经更新完成，不必重复执行!")
            return

        now = time.strftime("%Y-%m-%d %H:%M:%S")  # now是字符串
        paras = {"data_type": data_type, "data_name": "股票日线附加数据",
                 "data_source": "ths", "collect_start_time": now, "collect_status": "R"}
        log_id = mysql_script.record_log(paras, flag='before')

        result = self.thsHelper.get_day_attach(trade_date)

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_end_date": str(end_date), "collect_end_time": now, "collect_log": f"完成{end_date}的数据采集,更新股票{result}条",
                 "collect_status": "S", "id": log_id}
        mysql_script.record_log(paras, flag='after')

        print("--------更新每日股票附加数据完成------------")

    #更新板块数据
    def update_block_data(self):
        data_type = 'ths_block_member'
        today = datetime.datetime.now()
        today_str = today.strftime('%Y-%m-%d')

        last_data_end_date_record = self.mysql.select("select max(data_end_date) from collect_log where data_type = %s",
                                                      data_type)
        last_data_end_date = last_data_end_date_record[0][0]  # last_data_end_date是日期类型
        if last_data_end_date == None:
            last_data_end_date = datatime_util.str2date(today_str) - datetime.timedelta(days=1)

        end_date = datetime.datetime.strptime(today_str, '%Y-%m-%d').date()  # end_date是日期类型
        if last_data_end_date >= end_date:  # 日志记录的
            print("今天的数据已经更新完成，不必重复执行!")
            return
        result1 = self.thsHelper.get_block_gn()
        result2 = self.thsHelper.get_block_dy()
        result3 = self.thsHelper.get_block_zjhhy()
        result4 = self.thsHelper.get_block_thshy()
        block_count = 0
        member_count = 0
        if result1 is not None:
            block_count = block_count + result1[0]
            member_count = member_count + result1[1]
        if result2 is not None:
            block_count = block_count + result2[0]
            member_count = member_count + result2[1]
        if result3 is not None:
            block_count = block_count + result3[0]
            member_count = member_count + result3[1]
        if result4 is not None:
            block_count = block_count + result4[0]
            member_count = member_count + result4[1]

        if block_count != 0 or member_count != 0 :
            now = time.strftime("%Y-%m-%d %H:%M:%S")  # now是字符串
            today = time.strftime("%Y-%m-%d")
            paras = {"data_type": data_type, "data_name": "ths板块成分股", "data_source": "ths", "collect_start_time": now,
                     "data_end_date": today, "collect_end_time": now,
                     "collect_log": f"完成{data_type}的数据采集,更新板块信息{block_count}条，更新板块成分数据{block_count}条",
                     "collect_status": "S"}
            print(paras)
            mysql_script.record_log(paras)
        else:
            print("=======没有要更新的板块数据========")

    def batch_execute_everyday(self):
        self.update_day_attach()
        self.update_block_data()

if __name__ == '__main__':
    ths = ThsDataCollect()
    #ths.update_day_attach()
    ths.update_block_data()