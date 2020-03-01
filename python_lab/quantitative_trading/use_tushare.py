#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/2/12
    tushare测试
    官方参考文档
'''

import tushare as ts
import os
import csv
import datetime
import time
import pymysql

__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

token = 'b5f94a8161ede1ba5b20b62c133d866ccfebcb2ce314489d6447f948'

# 设置tushare pro的token并获取连接
#ts.set_token(token)    #改语句可以省略，直接将token作为pro_api的参数即可
pro = ts.pro_api(token)

def get_data():
    #df = pro.trade_cal(exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
    df = pro.query('trade_cal', exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
    print(df)

def get_kdata():
    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
    start_dt = '20200210'
    time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
    end_dt = time_temp.strftime('%Y%m%d')
    # 建立数据库连接,剔除已入库的部分
    #db = pymysql.connect(host='127.0.0.1', user='root', passwd='admin', db='stock', charset='utf8')
    #cursor = db.cursor()
    # 设定需要获取数据的股票池
    stock_pool = ['603912.SH', '300666.SZ', '300618.SZ', '002049.SZ', '300672.SZ']
    total = len(stock_pool)
    # 循环获取单个股票的日线行情
    for i in range(len(stock_pool)):
        try:
            df = pro.daily(ts_code=stock_pool[i], start_date=start_dt, end_date=end_dt)
            # 打印进度
            print('Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))
            c_len = df.shape[0]
            print(type(df))
            print(df)
        except Exception as aa:
            print(aa)
            print('No DATA Code: ' + str(i))
            continue

def write2csv():
    # input date
    # 获取当天系统日期 如20190308
    timest = time.strftime("%Y%m%d")

    ##获取交易日期
    ##平台上到接口，可以获取每天交易日期 ，该变量保存日期文件
    file_date = os.getcwd() + "/tushare_file/" + '/dt_' + timest + '.csv'

    ##df_date 若果想获取多天数据 修改 start_date=timest, end_date=timest 中变量则可以
    df_date = pro.query('trade_cal', start_date=timest, end_date=timest)
    ##把日期文件信息保存到csv文件
    df_date.to_csv(file_date, index=False, mode='w', header=False, encoding='gbk')

    ##文件内容如下SSE, 20190307, 1   其中:1表示为交易当天有交易,0表示当天没交易

    ##filename = '/root/workspace/stock/src/dt_'+timest+'.csv'

    ##下面代码打开日期文件，循环读取日期，并下载有交易日期到数据

    with open(file_date) as f:

        reader = csv.reader(f)
        dt_dates = []
        for row in reader:
            dt_dates.append([row[1], row[2]])
        print(dt_dates)

    file_name = os.getcwd() + "/tushare_file/" + '/stock_datas_' + timest + '.csv'
    for dt_date, act_flag in dt_dates:
        ##若干当天为交易日期则连接平台获取交易数据并保存到本地
        #文件格式：股票代码，日期，开、高，低，收，，涨跌金额，涨跌幅，成交量（手），成交额（千元）
        if act_flag == '1':
            df = pro.daily(trade_date=dt_date)
            df.to_csv(file_name, index=False, mode='w', header=False, encoding="utf-8", sep='|')


def write2db(timest, file_name):
    ###下面把数据保持到mysql
    if os.path.exists(file_name):
        db = pymysql.connect(host='127.0.0.1', user='mysql用户', passwd='mysql密码', db='mysql数据库', charset='utf8',
                             local_infile=1)
        cursor = db.cursor()

        sql_load_datas = """LOAD DATA LOCAL INFILE '%s' 
            INTO TABLE tb_tock_daily 
            FIELDS TERMINATED BY '|' 
            LINES TERMINATED BY '\n'
            ;
    """ % (file_name)

        sql_ddl = """ truncate table  tb_tock_daily ;"""    #删除表内容
        sql_delete = """delete from tb_tock_daily_his where trade_date ='%s' """ % (timest)
        sql_insert = """insert into tb_tock_daily_his select a.* from tb_tock_daily a where trade_date ='%s' """ % (
            timest)
        cursor.execute(sql_ddl)
        cursor.execute("commit;")
        cursor.execute(sql_load_datas)
        cursor.execute("commit;")

        cursor.execute(sql_delete)
        cursor.execute("commit;")

        cursor.execute(sql_insert)
        cursor.execute("commit;")
        cursor.close()
        db.close()


def get_version():
    print(ts.__version__)

if __name__ == '__main__':
    #get_version()
    #get_kdata()
    write2csv()