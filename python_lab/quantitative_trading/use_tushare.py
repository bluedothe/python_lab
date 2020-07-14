#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/2/12
    tushare测试
    官方参考文档
    tusharePro接口：https://tushare.pro/document/2?doc_id=27
    tushare接口：http://tushare.org/classifying.html#id2
'''

import tushare as ts
import os
import csv
import datetime
import time
import pymysql
import pandas as pd

from config import bluedothe

__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

token = bluedothe.tushare_token

# 设置tushare pro的token并获取连接
#ts.set_token(token)    #该语句可以省略，直接将token作为pro_api的参数即可
pro = ts.pro_api(token)

# pandas数据显示设置
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.max_rows', None)  # 显示所有行

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

#基础数据：获取股票列表
def get_stock_basic():
    #data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date,fullname,enname,market,exchange,curr_type,list_date,delist_date,is_hs')
    print(data)

#基础数据：交易日历
def get_trade_cal():
    #data = pro.trade_cal(exchange='', start_date='20180101', end_date='20181231')
    data = pro.query('trade_cal', start_date='20180101', end_date='20181231',fields='exchange,cal_date,is_open,pretrade_date')
    print(data)

#基础数据：股票曾用名
def get_namechange():
    data = pro.namechange(ts_code='600848.SH', fields='ts_code,name,start_date,end_date,change_reason')
    print(data)

#基础数据：上市公司基本信息
def get_stock_company():
    #data = pro.stock_company(exchange='SZSE', fields='ts_code,chairman,manager,secretary,reg_capital,setup_date,province,introduction,employees,main_business,business_scope')
    data = pro.stock_company(exchange='SSE', fields='ts_code,chairman,manager,secretary,reg_capital,setup_date,province,introduction,employees,main_business,business_scope')
    print(data)

#行情数据：日线行情
#数据说明：交易日每天15点～16点之间。本接口是未复权行情，停牌期间不提供数据.或通过通用行情接口获取数据，包含了前后复权数据
#调取说明：基础积分每分钟内最多调取500次，每次5000条数据，相当于23年历史，用户获得超过5000积分正常调取无频次限制。
#日期都填YYYYMMDD格式，比如20181010
def get_daily():
    #data = pro.daily(ts_code='000001.SZ,600000.SH', start_date='20180701', end_date='20180718')
    data = pro.query('daily', ts_code='XIN9', start_date='20180701', end_date='20180718')
    #data = pro.daily(trade_date='20180810')
    print(data)

#（sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板）
def get_dpzs():
    df = ts.get_hist_data(code='cyb', start="2020-04-15", end='2020-04-15')
    print(df)

#行情数据：停复牌信息
def get_suspend():
    data = pro.query('suspend', ts_code='', suspend_date='20180720', resume_date='', fields='')
    print(data)

#行情数据：每日停复牌信息
def get_suspend_d():
    data = pro.suspend_d(suspend_type='S', trade_date='20200312')
    print(data)

#行情数据：每日指标
#更新时间：交易日每日15点～17点之间
#描述：获取全部股票每日重要的基本面指标，可用于选股分析、报表展示等。
#日期都填YYYYMMDD格式，比如20181010
#积分：用户需要至少300积分才可以调取
def get_daily_basic():
    data = pro.query('daily_basic', ts_code='', trade_date='20180726',fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb')
    print(data)

#行情数据：通用行情接口
#更新时间：股票和指数通常在15点～17点之间
#由于本接口是集成接口，在SDK层做了一些逻辑处理，目前暂时没法用http的方式调取通用行情接口。用户可以访问Tushare的Github，查看源代码完成类似功能。

#行情数据：沪深股通十大成交股
def get_hsgt_top10():
    #data = pro.query('hsgt_top10', ts_code='600519.SH', start_date='20180701', end_date='20180725')
    data = pro.hsgt_top10(trade_date='20180725', market_type='1')
    print(data)

#股票分类
def get_industry():
    #data = ts.get_industry_classified()   #行业分类
    #data = ts.get_concept_classified()        #概念分类
    #data = ts.get_area_classified()        #地域分类
    #data = ts.get_sme_classified()        #获取中小板股票数据，即查找所有002开头的股票
    #data = ts.get_gem_classified()        #获取创业板股票数据，即查找所有300开头的股票
    #data = ts.get_st_classified()        #获取风险警示板股票数据，即查找所有st股票
    #data = ts.get_hs300s()        #获取沪深300当前成份股及所占权重
    #data = ts.get_sz50s()        #获取上证50成份股
    #data = ts.get_zz500s()        #获取中证500成份股
    #data = ts.get_terminated()        #获取已经被终止上市的股票列表，数据从上交所获取，目前只有在上海证券交易所交易被终止的股票。
    data = ts.get_suspended()        #获取被暂停上市的股票列表，数据从上交所获取，目前只有在上海证券交易所交易被终止的股票。
    print(data)

def test():
    data = ts.get_h_data('002337', start='2015-01-01', end='2015-03-16')  # 两个日期之间的前复权数据
    print(data)

if __name__ == '__main__':
    #get_version()
    #get_kdata()
    #write2csv()
    #get_stock_basic()
    #get_trade_cal()
    #get_namechange()
    #get_stock_company()
    #get_daily()
    #get_suspend()
    #get_suspend_d()
    #get_daily_basic()
    #get_hsgt_top10()
    #get_industry()
    #test()
    get_dpzs()
