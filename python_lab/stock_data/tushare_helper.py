#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/3/28
    通过tushare接口获取股票数据
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import os
import pandas as pd
import tushare as ts
import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, Float, Integer, DateTime, BigInteger

from db.mysqlHelper import mysqlHelper
from stock_data import bluedothe
from stock_data import config
from tool import printHelper

class TushareHelper:
    def __init__(self):
        self.pro = ts.pro_api(bluedothe.tushare_token)

        # pandas数据显示设置
        pd.set_option('display.max_columns', None)  # 显示所有列
        pd.set_option('display.max_rows', None)  # 显示所有行

        # mysql对象
        self.mysql = mysqlHelper(config.mysql_host, config.mysql_username, bluedothe.mysql_password,
                                 config.mysql_dbname)

        # pandas的mysql对象
        db_paras = {"host": config.mysql_host, "user": config.mysql_username, "passwd": bluedothe.mysql_password,
                    "dbname": config.mysql_dbname}
        #self.engine = create_engine('mysql+pymysql://{user}:{passwd}@{host}/{dbname}?charset=utf8'.format(**db_paras))
        self.engine = create_engine(f'mysql+pymysql://{config.mysql_username}:{bluedothe.mysql_password}@{config.mysql_host}/{config.mysql_dbname}?charset=utf8')

    #将pandas.DataFrame中列名和预指定的类型映射
    # 此方法对VARCHAR的长度不能灵活定义，不具体通用性
    def mapping_df_types(df):
        dtypedict = {}
        for i, j in zip(df.columns, df.dtypes):
            if "object" in str(j):
                dtypedict.update({i: NVARCHAR(length=16)})
            if "float" in str(j):
                dtypedict.update({i: Float(precision=2, asdecimal=True)})
            if "int" in str(j):
                dtypedict.update({i: Integer()})
            if "datetime" in str(j):
                dtypedict.update({i: DateTime()})
            if "bool" in str(j):
                dtypedict.update({i: bool()})
        return dtypedict

    # 基础数据：获取股票列表
    def get_stock_basic(self, list_status="L"):
        # data = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        data = self.pro.query('stock_basic', exchange='', list_status=list_status,
                         fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_date,delist_date,is_hs')
        #print(data)
        return data

    """
       if_exists：（fail，replace，append）
         fail：如果表存在，则不进行操作
         replace：如果表存在就删除表，重新生成，插入数据
         append：如果表存在就插入数据，不存在就直接生成表
       """

    # 获取股票基本信息，通过pandas入库
    @printHelper.time_this_function
    def stock_basic_mysql_pandas(self, list_status="L",if_exists='append'):
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        df = self.get_stock_basic(list_status)
        col_name = df.columns.tolist()
        ##col_name.insert(1, 'id')  #在最前面插入一列id
        #col_name.insert(col_name.index('ts_code'), 'id')  # 在ts_code列前面插入id,col_name.index('ts_code')+1表示在此列后插入
        df.reindex(columns=col_name)
        ##df['id'] = range(1,len(df) + 1)   #不能这样赋值，应该是从数据库中取出最大id后加1
        df['list_status'] = [list_status] * len(df)  #字段赋值
        df['create_time'] = [cur_time] * len(df)    #字段赋值
        df['update_time'] = [cur_time] * len(df)    #字段赋值
        dtypedict = {
            'id': BigInteger,'ts_code': NVARCHAR(length=16), 'symbol': NVARCHAR(length=16), 'name': NVARCHAR(length=16), 'area': NVARCHAR(length=16), 'industry': NVARCHAR(length=16), 'fullname': NVARCHAR(length=64), 'enname': NVARCHAR(length=128), 'market': NVARCHAR(length=16), 'exchange': NVARCHAR(length=16), 'curr_type': NVARCHAR(length=16),'list_status': NVARCHAR(length=16), 'list_date': NVARCHAR(length=16), 'delist_date': NVARCHAR(length=16), 'is_hs': NVARCHAR(length=16), 'create_time': DateTime, 'update_time': DateTime
        }
        ## dtypedict =self.mapping_df_types(df)   #此方法对VARCHAR的长度不能灵活定义，不具体通用性
        ##df.to_sql('stock_basic_pd', self.engine, if_exists='append', index=False, dtype=dtypedict)   # 追加数据到现有表
        pd.io.sql.to_sql(df, 'stock_basic_pd', con=self.engine, if_exists=if_exists, index=False, index_label="symbol", dtype=dtypedict, chunksize = 10000) #chunksize参数针对大批量插入，pandas会自动将数据拆分成chunksize大小的数据块进行批量插入;
        ##self.engine.connect().execute("ALTER TABLE stock_basic_pd ADD PRIMARY KEY (symbol);") #第一次建表的时候执行，再次执行报错

    #获取股票基本信息，单条记录入库,如果有字段存在none值，转为空字符串
    @printHelper.time_this_function
    def stock_basic_mysql_one(self, list_status="L"):
        df = self.get_stock_basic(list_status)
        df['list_status'] = [list_status] * len(df)  # 字段赋值
        df = df.where(df.notnull(), "")
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #sql = "INSERT INTO stock_basic(ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_date,delist_date,is_hs,create_time,update_time) VALUES"  #  ON duplicate KEY UPDATE code=values(code)
        table_name = "stock_basic"
        column_name = ','.join(df.keys().values) + ",create_time,update_time"
        values = ""
        for index, row in df.iterrows():
            value = "("
            for record in row.tolist():
                value = value + '"' + record + '",'
            value = value + '"' + cur_time + '",'
            value = value + '"' + cur_time + '",'
            value = value[0:-1] + "),"
            values = values + value
        values = values[0:-1]
        sql = f"INSERT INTO {table_name} ({column_name}) VALUES{values} ON duplicate KEY UPDATE ts_code=values(ts_code)"  # ON duplicate KEY UPDATE code=values(code)
        result_num = self.mysql.exec(sql)
        print("总共{}条数据，成功插入{}条数据".format(len(df),result_num))

    def joinStr(self,str):
        if type(str) is None: return ""

    # 获取股票基本信息，多条记录批量入库,执行报错：not enough arguments for format string，原因是没有把传入的数组参数分开，把元组当成一个sql参数了
    @printHelper.time_this_function
    def stock_basic_mysql_many(self, list_status="L"):
        df = self.get_stock_basic()
        df['list_status'] = [list_status] * len(df)  # 字段赋值
        df = df.where(df.notnull(), 'NULL')
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        dates = [cur_time,cur_time]
        values = []
        sql = "INSERT INTO stock_basic(code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_date,delist_date,is_hs,create_time,update_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for index, row in df.iterrows():
            value = [0]
            value.extend(row.tolist())
            #value = row.tolist()
            #value.extend(dates)
            #print(value)
            values.append((value))
            if index == 3: break
        print(values)
        self.mysql.exec(sql,values)
        print("已完成插入{}条数据".format(len(values)))

    #测试
    #执行时抛异常：(1241, 'Operand should contain 1 column(s)')
    def stock_basic_mysql_many2(self):
        df = self.get_stock_basic()
        into = ','.join(df.keys().values)
        val = ','.join(str(v) for v in df.values)
        print(into)
        print(val)
        df = df.where(df.notnull(), 'NULL')
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        dates = [cur_time,cur_time]
        #values = ('000001.SZ', '000001', '平安银行')
        #values = (('000001SZ', '000001', '平安银行'),('000002SZ', '000002', '平安银行2'),('000001SZ', '000001', '平安银行'),('000002SZ', '000002', '平安银行2'))
        sql = """INSERT INTO stock_basic (code,symbol,fullname) VALUES (%s,%s,%s) ON duplicate KEY UPDATE code=values(code)""" #ON duplicate KEY UPDATE code=values(code)
        #values = (("000001.SZ", "000001", "平安银行"),("000002.SZ", "000002", "平安银行2"),("000003.SZ", "000003", "平安银行3"),("000004.SZ", "000004", "平安银行4"))
        values = []
        values.append(('000001.SZ', '000001', '平安银行'))
        values.append(('000002.SZ', '000002', '平安银行2'))
        values.append(('000003.SZ' '000003', '平安银行3'))
        #print(values)
        #self.mysql.exec(sql,values)
        print("已完成插入{}条数据".format(len(values)))

    # 基础数据：交易日历
    # 1990年12月19日 上海证券交易所开市交易
    # 1991年07月03日 深圳证券交易所开市交易
    # 2009年10月30日 创业板开市交易
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

    #获取特定一天的全部股票交易数据
    #@printHelper.time_this_function
    def get_history_day(self,onedate = ""):
        start_dt = '20200404'
        time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
        end_dt = time_temp.strftime('%Y%m%d')
        end_dt = "20200407"
        stock_pool = ['600848.SH', '300666.SZ', '300618.SZ', '002049.SZ', '300672.SZ']
        ##df = ts.get_hist_data(code='600848',start="2020-04-01",end="2020-04-03")  # 一次性获取全部日k线数据
        df = ts.get_hist_data(code='600848', start="2020-04-04", end="2020-04-07")  # 一次性获取全部日k线数据
        #df = ts.get_today_all()
        #df = self.pro.query("daily",ts_code=stock_pool[0], start_date=start_dt, end_date=end_dt)
        ##df = self.pro.query("daily", start_date=start_dt, end_date=start_dt)
        #df = self.pro.daily(trade_date=end_dt)
        print(df)

    #批量格式化日期字段，去掉分隔符
    def format_date(self,str):
        return str.replace('-', '')

    #获取特定一支股票的全部交易数据
    #tushare接口只有2017-10-11以后的数据
    def get_history_phase(self,ts_code):
        code = ts_code[0:-3]
        dfpro = self.pro.query("daily", ts_code=ts_code,start_date="20171011")
        dfpro.insert(0,'code',code)
        df = ts.get_hist_data(code=code, start="2017-10-11")
        if not dfpro.empty and not df.empty:
            df.drop(['open','high','low','close'], axis=1, inplace=True)
            df.rename(index=self.format_date, inplace=True)
            df['new_date'] = (df.index)
            dfall = pd.merge(dfpro, df,how='left', left_on='trade_date',right_on='new_date',sort=False,copy=False)
            dfall.drop('new_date', axis=1, inplace=True)
            newdf = dfall.sort_values(by ='trade_date', axis=0, ascending=True)

            filename = config.tushare_csv_home + "day/" + ts_code + ".csv"
            newdf.to_csv(filename, index=False, sep=',', encoding="utf_8_sig")
            ## sep='?'使用?分隔需要保存的数据，如果不写，默认是,;na_rep='NA'缺失值保存为NA，如果不写，默认是空;float_format='%.2f',保留两位小数;,header=0不保存列名;,index=0不保存行索引
            #print(df)

    #通过tusharePro接口获取一段时间内的交易数据
    def get_history_pro(self,ts_code,start_date,end_date):
        dfpro = self.pro.query("daily", ts_code=ts_code,start_date=start_date, end_date=end_date)
        dfpro.insert(0, 'code', ts_code[0:-3])
        if not dfpro.empty:
            newdf = dfpro.sort_values(by='trade_date', axis=0, ascending=True)

            filename = config.tushare_csv_home + "day_pro/" + ts_code + ".csv"
            if os.path.isfile(filename):
                newdf.to_csv(filename, index=False, mode='a', header=False, sep=',', encoding="utf_8_sig")
            else:
                newdf.to_csv(filename, index=False, mode='w', header=True, sep=',', encoding="utf_8_sig")

    #获取某天的全部交易数据，然后追加到cvs文件中，文件没有则自动创建
    def get_history_by_date(self,trade_date_pro):
        trade_date = datetime.datetime.strptime(trade_date_pro,'%Y%m%d').date()
        print(trade_date)
        dfpro = self.pro.query("daily", trade_date=trade_date_pro)
        dfpro.insert(0, 'code', (dfpro['ts_code'].str)[0:-3])
        #将dfpro数据按照ts_code分组，按照trade_date升序，取出相同ts_code的一组数据，构造成一个dataFrame对象
        #dfpro_new = dfpro.sort_values(by =['ts_code','trade_date'], axis=0, ascending=True)
        #dfpro_code = dfpro_new.loc[dfpro_new['ts_code'] == '603300.SH']
        ##print(dfpro['ts_code'].drop_duplicates())  #列数据去重
        #调用旧接口（ts_code,start_date,end_date)取数据，按照trade_date升序，与上一个dataFrame对象合并
        #写入cvs文件中，如果cvs文件不存在则新建
        #if os.path.isfile(filename):df.to_csv(filename, mode='a', header=False,sep=',');else:df.to_csv(filename, mode='w', header=True,sep=',')
        if dfpro.empty:return
        for i in range(0,len(dfpro) - 1):
            row = pd.DataFrame(dfpro.iloc[i:i+1])
            ts_code = row.loc[i,'ts_code']
            code = ts_code[0:-3]
            #row.loc[i,'code'] = code

            filename = config.tushare_csv_home + "day/" + ts_code + ".csv"
            df = ts.get_hist_data(code=code, start=str(trade_date), end=str(trade_date))
            if not df.empty:
                df.drop(['open', 'high', 'low', 'close'], axis=1, inplace=True)
                df.rename(index=self.format_date, inplace=True)
                df['new_date'] = (df.index)
                dfall = pd.merge(row, df, how='left', left_on='trade_date', right_on='new_date', sort=False,copy=False)
                dfall.drop('new_date', axis=1, inplace=True)
            else:
                dfall = row

            if os.path.isfile(filename):
                dfall.to_csv(filename, index=False, mode='a', header=False, sep=',', encoding="utf_8_sig")
            else:
                dfall.to_csv(filename, index=False, mode='w', header=True, sep=',', encoding="utf_8_sig")

    # 获取某天的tusharepro交易数据，然后追加到cvs文件中，文件没有则自动创建
    def get_history_pro_by_date(self, trade_date_pro):
        dfpro = self.pro.query("daily", trade_date=trade_date_pro)
        #dfpro['code'] = dfpro['ts_code'][0:-3]
        dfpro.insert(0, 'code', (dfpro['ts_code'].str)[0:-3])
        # 将dfpro数据按照ts_code分组，按照trade_date升序，取出相同ts_code的一组数据，构造成一个dataFrame对象
        # dfpro_new = dfpro.sort_values(by =['ts_code','trade_date'], axis=0, ascending=True)
        # dfpro_code = dfpro_new.loc[dfpro_new['ts_code'] == '603300.SH']
        ##print(dfpro['ts_code'].drop_duplicates())  #列数据去重
        # 调用旧接口（ts_code,start_date,end_date)取数据，按照trade_date升序，与上一个dataFrame对象合并
        # 写入cvs文件中，如果cvs文件不存在则新建
        # if os.path.isfile(filename):df.to_csv(filename, mode='a', header=False,sep=',');else:df.to_csv(filename, mode='w', header=True,sep=',')
        if dfpro.empty: return

        for i in range(0, len(dfpro) - 1):
            row = pd.DataFrame(dfpro.iloc[i:i + 1])
            ts_code = row.loc[i, 'ts_code']
            filename = config.tushare_csv_home + "day_pro/" + ts_code + ".csv"

            if os.path.isfile(filename):
                row.to_csv(filename, index=False, mode='a', header=False, sep=',', encoding="utf_8_sig")
            else:
                row.to_csv(filename, index=False, mode='w', header=True, sep=',', encoding="utf_8_sig")

if __name__ == '__main__':
    tshelper = TushareHelper()
    #tshelper.get_stock_basic()
    #tshelper.get_trade_cal()
    #tshelper.is_trade_day("20200125")
    #tshelper.stock_basic_mysql_one()
    #tshelper.stock_basic_mysql_many2()
    #tshelper.stock_basic_mysql_pandas()

    #tshelper.get_history_day()
    #tshelper.get_history_phase("000003.SZ")
    #tshelper.get_history_pro_by_date("20200413")

