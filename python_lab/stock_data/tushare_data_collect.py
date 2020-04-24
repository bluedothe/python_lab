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
from stock_data.tushare_helper import TushareHelper
from stock_data import mysql_script
from tool import printHelper
from tool import file_util
from tool import datatime_util

class TushareDataCollect:
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
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_type": "stock_basic", "data_name": "股票基本信息",
                 "data_source": "tusharepro", "collect_start_time": now, "collect_status": "R"}
        log_id = mysql_script.record_log(paras)

        self.mysql.exec(mysql_script.truncate_table_common.format("stock_basic"))
        self.tshelper.stock_basic_mysql_one("L")
        self.tshelper.stock_basic_mysql_one("D")
        self.tshelper.stock_basic_mysql_one("P")

        today = datetime.datetime.now()
        end_date = today.strftime('%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_end_date": str(end_date), "collect_end_time": now,
                 "collect_log": f"完成股票基础数据更新", "collect_status": "S", "id": log_id}
        mysql_script.record_log(paras, False)

        print("--------tusharepro股票基本信息更新完成------------")


    #采集交易数据，tusharepro+tushare
    #只在第一次采集的时候执行，以后执行追加方法
    @printHelper.time_this_function
    def get_stock_history(self):
        #last_data_end_date = self.mysql.select("select max(data_end_date) from collect_log where data_type = %s",'tushare_history_all')
        #start_date = last_data_end_date[0][0] + datetime.timedelta(days=1)
        today = datetime.datetime.now()
        end_date = today.strftime('%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_type": "tushare_history_all", "data_name": "tushare交易数据，两个接口合并",
                 "data_source": "tusharepro+tushare", "collect_start_time": now, "collect_status": "R"}
        log_id = mysql_script.record_log(paras)

        sql = "select ts_code from stock_basic"
        stock_basic_df = pd.read_sql(sql, self.engine, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None,chunksize=None)
        for ts_code in stock_basic_df['ts_code']:
            print(ts_code)
            ##filename = config.tushare_csv_home + "day/" + ts_code + ".csv"
            ##if os.path.isfile(filename): continue
            time.sleep(0.8)
            self.tshelper.get_history_phase(ts_code)

        start_date = "2017-10-11"
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_end_date": str(end_date), "collect_end_time": now,
                 "collect_log": f"完成从{start_date}到{end_date}的数据采集", "collect_status": "S", "id": log_id}
        mysql_script.record_log(paras, False)

    #采集交易数据，tusharepro
    # 只在第一次采集的时候执行，以后执行追加方法
    @printHelper.time_this_function
    def get_stock_history_pro(self):
        sql = "select ts_code from stock_basic"
        stock_basic_df = pd.read_sql(sql, self.engine, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None,chunksize=None)
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_type": "tushare_history_pro", "data_name": "tusharepro交易数据",
                 "data_source": "tusharepro", "collect_start_time": now, "collect_status": "R"}
        log_id = mysql_script.record_log(paras)

        for ts_code in stock_basic_df['ts_code']:
            time.sleep(1)
            self.tshelper.get_history_pro(ts_code, "19880101", "20081231")
            self.tshelper.get_history_pro(ts_code, "20090101", "20200411")

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_end_date": "2020-04-12", "collect_end_time": now,
                 "collect_log": "一次完成到2020-04-12的所有交易数据", "collect_status": "S", "id": log_id}
        mysql_script.record_log(paras, False)

    #获取大盘指数
    @printHelper.time_this_function
    def get_day_index_all(self):
        last_data_end_date = self.mysql.select("select max(data_end_date) from collect_log where data_type = %s",'tushare_index')
        if last_data_end_date[0][0] == None:
            start_date = datatime_util.str2date("2017-10-16")
        else:
            start_date = last_data_end_date[0][0] + datetime.timedelta(days=1)
        today = datetime.datetime.now()
        end_date = today.strftime('%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        if start_date > end_date:
            print("今天的数据已经更新完成，不必重复执行!")
            return

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_type": "tushare_index", "data_name": "tushare大盘指数",
                 "data_source": "tushare", "collect_start_time": now, "collect_status": "R"}
        log_id = mysql_script.record_log(paras)

        self.tshelper.get_day_index_all(start_date, end_date)

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_end_date": str(end_date), "collect_end_time": now,
                 "collect_log": f"完成从{start_date}到{end_date}的数据采集", "collect_status": "S", "id": log_id}
        mysql_script.record_log(paras, False)

        print("--------tushare_index大盘指数追加完成------------")

    #增量追加交易历史数据(tusharepro+tushare)
    @printHelper.time_this_function
    def get_history_by_date(self):
        # start_date = self.mysql.select("select max(data_end_date) from collect_log where data_type = 'tushare_history_all'")
        # start_date = self.mysql.select("select * from collect_log where data_type = %s",['tushare_history_all'])
        # start_date = self.mysql.select("select * from collect_log ")
        last_data_end_date = self.mysql.select("select max(data_end_date) from collect_log where data_type = %s",'tushare_history_all')
        start_date = last_data_end_date[0][0] + datetime.timedelta(days=1)
        start_date_bak = start_date
        today = datetime.datetime.now()
        end_date = today.strftime('%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        if start_date > end_date:
            print("今天的数据已经更新完成，不必重复执行!")
            return

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_type": "tushare_history_all", "data_name": "tushare交易数据，两个接口合并",
                 "data_source": "tusharepro+tushare", "collect_start_time": now, "collect_status": "R"}
        log_id = mysql_script.record_log(paras)
        while start_date <= end_date:
            start_date_pro = start_date.strftime('%Y%m%d')
            #print(start_date_pro)
            self.tshelper.get_history_by_date(start_date_pro)
            start_date = start_date + datetime.timedelta(days=1)
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_end_date": str(end_date), "collect_end_time": now,
                 "collect_log": f"完成从{start_date_bak}到{end_date}的数据追加", "collect_status": "S", "id": log_id}
        mysql_script.record_log(paras, False)

        print("--------tusharepro+tushare日数据追加完成------------")

    # 增量追加交易历史数据(pro)
    @printHelper.time_this_function
    def get_history_pro_by_date(self):
        # start_date = self.mysql.select("select max(data_end_date) from collect_log where data_type = 'tushare_history_all'")
        # start_date = self.mysql.select("select * from collect_log where data_type = %s",['tushare_history_all'])
        # start_date = self.mysql.select("select * from collect_log ")
        last_data_end_date = self.mysql.select("select max(data_end_date) from collect_log where data_type = %s",
                                               'tushare_history_pro')
        start_date = last_data_end_date[0][0] + datetime.timedelta(days=1)
        start_date_bak = start_date
        today = datetime.datetime.now()
        end_date = today.strftime('%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        if start_date > end_date:
            print("今天的数据已经更新完成，不必重复执行!")
            return

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_type": "tushare_history_pro", "data_name": "tusharepro交易数据",
                 "data_source": "tusharepro", "collect_start_time": now, "collect_status": "R"}
        log_id = mysql_script.record_log(paras)

        while start_date <= end_date:
            start_date_pro = start_date.strftime('%Y%m%d')
            # print(start_date_pro)
            self.tshelper.get_history_pro_by_date(start_date_pro)
            start_date = start_date + datetime.timedelta(days=1)
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        paras = {"data_end_date": str(end_date), "collect_end_time": now,
                 "collect_log": f"完成从{start_date_bak}到{end_date}的数据追加", "collect_status": "S", "id": log_id}
        mysql_script.record_log(paras, False)

        print("--------tusharepro日数据追加完成-----------------")

    #批量执行历史交易数据追加
    def batch_execute_everyday(self):
        self.get_stock_basic_one()  #更新股票基本信息
        self.get_history_by_date()   #追加tusharepro+tushare日交易数据
        self.get_history_pro_by_date()   #追加tusharepro日交易数据
        self.get_day_index_all()  #追加tushare的大盘指数
        print("========tushare数据更新，批量执行完成=======")

    #删除cvs文件中指定的行数据
    def del_cvs_rows(self):
        path = "E:/database/csv/tushare/day_test/"
        datestr = "2020-04-13"
        for root, dir, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                # print(full_path)
                # print(file)
                filesize = os.path.getsize(full_path)  #文件字节数
                print("filesize为: %s" % (filesize))
                if filesize == 0: continue
                mtime = os.stat(full_path).st_mtime
                file_modify_time = time.strftime('%Y-%m-%d', time.localtime(mtime))
                if file_modify_time == datestr:
                    print("{0} 修改时间是: {1}".format(full_path, file_modify_time))
                    csv_file =  open(full_path, "rb+")
                    print("csv_file.tell为: %s" % (csv_file.tell()))
                    csv_file.seek(-400, os.SEEK_END)  #seek是光标移到
                    lines = csv_file.readlines()
                    lines_count = len(lines)
                    print("总行数：%s" % (lines_count))
                    print("csv_file.tell为: %s" % (csv_file.tell()))
                    if lines_count >=3:
                        csv_file.seek(-400, os.SEEK_END)  # seek是光标移到
                        print("csv_file.tell为: %s" % (csv_file.tell()))
                        for i in range(lines_count):
                            print("i:",i)
                            line = csv_file.readline()
                            print("读取的数据为: %s" % (line))
                            print("csv_file.tell为: %s" % (csv_file.tell()))

                            print("xx1:",line)
                            print("xx2:",chardet.detect(line))
                            print("xx3:",line.decode(encoding="gb2312"))
                            print("xx5:",chardet.detect((line.decode(encoding="gb2312")).encode("utf-8")))

                            linexx = line.decode(encoding="utf-8")
                            print("行头：",linexx[0:2])
                            if linexx[0:2] == "0,":
                                print("该行要删除: %s" % (linexx))

                    # file.truncate([size])从文件的首行首字符开始截断，截断文件为 size 个字符，无 size 表示从当前位置截断；截断之后后面的所有字符被删除，其中 windows 系统下的换行代表2个字符大小。
                    #csv_file.truncate()  #截取光标位置之前的内容，后面的删除
                    csv_file.close()
                    break

    #删除文件最后一行
    def delete_last_row(self,full_path,filename=""):
        df = pd.read_csv(full_path)
        filesize = os.path.getsize(full_path)  # 文件字节数
        print("filesize为: %s" % (filesize))
        if filesize == 0: return
        df = df.astype(str)
        mtime = os.stat(full_path).st_mtime
        file_modify_time = time.strftime('%Y-%m-%d', time.localtime(mtime))
        if file_modify_time == "2020-04-13":
            csv_file = open(full_path, "rb+")
            print("csv_file.tell为: %s" % (csv_file.tell()))
            csv_file.seek(-400, os.SEEK_END)  # seek是光标移到
            lines = csv_file.readlines()
            lines_count = len(lines)
            print("读取的行数：%s" % (lines_count))
            print("csv_file.tell为: %s" % (csv_file.tell()))
            if lines_count >= 2:
                csv_file.seek(-400, os.SEEK_END)  # seek是光标移到
                print("csv_file.tell为: %s" % (csv_file.tell()))
                for i in range(lines_count-1):
                    print("i:", i)
                    line = csv_file.readline()
                    print("读取的数据为: %s" % (line))
                    print("csv_file.tell为: %s" % (csv_file.tell()))

                    line_utf8 = line.decode(encoding="utf-8")
                    print("行{}：".format(i+1), line_utf8)
                    if line_utf8[0:2] == "0,":
                        print("该行要删除: %s" % (line_utf8))

                # file.truncate([size])从文件的首行首字符开始截断，截断文件为 size 个字符，无 size 表示从当前位置截断；截断之后后面的所有字符被删除，其中 windows 系统下的换行代表2个字符大小。
                csv_file.truncate()  #截取光标位置之前的内容，后面的删除
            csv_file.close()
        else:
            print("no update file")

    @printHelper.time_this_function
    def batch_delete_last_row(self):
        file_util.traversal_dir("E:/database/csv/tushare/day",self.delete_last_row)

    #更新后文件中多了换行，有问题
    def update_value(self):
        full_path = "E:/database/csv/tushare/day/000001.SZ.csv"
        df = pd.read_csv(full_path)
        filesize = os.path.getsize(full_path)  # 文件字节数
        print("filesize为: %s" % (filesize))
        if filesize == 0: return
        df = df.astype(str)
        mtime = os.stat(full_path).st_mtime
        file_modify_time = time.strftime('%Y-%m-%d', time.localtime(mtime))
        if file_modify_time == "2020-04-13":
            num = len(df)
            print((df.iloc[num-1])['code'])
            #df.loc[df['code'].str.contains('.'), 'code'] = df['code'][0:-3]
            code = (df.iloc[num-1])['code']
            if len(code) >6: (df.iloc[num - 1])['code'] = code[0:-3]

            print(df.iloc[num-1])
            df.to_csv(full_path, index=False, mode='w', header=True, sep=',', encoding="utf_8_sig")
        else:
            print("no")

    def test_record_log(self):
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        print(now)
        paras = {"data_type": "tushare_history_all", "data_name": "tushare交易数据，两个接口合并",
                 "data_source": "tusharepro+tushare", "collect_start_time": now, "collect_status": "R"}
        paras = {"data_end_date": "2020-04-03", "collect_end_time": now, "collect_log": "一次完成2017-10-09到2020-04-03的所有交易数据", "collect_status": "S", "id": 1}
        mysql_script.record_log(paras,False)

    # 测试通过传递value元组批量插入，试验失败
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
    dc = TushareDataCollect()
    #dc.get_stock_basic_pandas()
    dc.get_stock_basic_one()
    #dc.get_stock_history()
    #dc.get_stock_history_pro()
    #dc.get_day_index_all()
    #dc.get_history_pro_by_date()
    #dc.get_history_by_date()
    #dc.batch_execute_everyday()   #批量执行

    #dc.update_value()
    #dc.del_cvs_rows()
    # dc.test_record_log()
    # dc.test()
    #dc.delete_last_row("E:/database/csv/tushare/day/000001.SZ.csv")
    #dc.batch_delete_last_row()

