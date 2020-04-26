#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/3/28
    通过通达信接口获取股票数据，参考资料：https://rainx.gitbooks.io/pytdx/content/pytdx_reader.html
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import os
import pandas as pd

from pytdx.hq import TdxHq_API,TDXParams
from pytdx.exhq import TdxExHq_API
from pytdx.config.hosts import hq_hosts
from sqlalchemy import create_engine

from db.mysqlHelper import mysqlHelper
from stock_data import bluedothe
from stock_data import config
from tool import printHelper
from tool import datatime_util
from tool import file_util

class TdxHelper:
    ip_list = [{'ip': '119.147.212.81', 'port': 7709},{'ip': '60.12.136.250', 'port': 7709}]

    def __init__(self):
        self.api = TdxHq_API()
        if not self.api.connect('60.12.136.250', 7709):
            print("服务器连接失败！")

        # pandas数据显示设置
        pd.set_option('display.max_columns', None)  # 显示所有列
        pd.set_option('display.max_rows', None)  # 显示所有行

        # mysql对象
        self.mysql = mysqlHelper(config.mysql_host, config.mysql_username, bluedothe.mysql_password,
                                 config.mysql_dbname)

        # pandas的mysql对象
        self.engine = create_engine(f'mysql+pymysql://{config.mysql_username}:{bluedothe.mysql_password}@{config.mysql_host}/{config.mysql_dbname}?charset=utf8')

    def close_connect(self):
        self.api.disconnect()

    #获取k线，最后一个参数day,说明需要获取的数量，本接口只获取从最近交易日往前的数据
    #输入参数：五个参数分别为：category（k线),市场代码(0:深圳，1:上海),股票代码,开始位置(从最近交易日向前取，0表示最近交易日),返回的记录条数
    #K线种类:  0 5分钟K线; 1 15分钟K线; 2 30分钟K线; 3 1小时K线; 4 日K线;5 周K线;6 月K线;7 1分钟;8 1分钟K线; 9 日K线;10 季K线;11 年K线
    #返回值：open,close,high,low,vol,amount,year,month,day,hour,minute,datetime
    # csv格式：code,ts_code,trade_date(缩写）,trade_time,time_index,open,high,low,close,amount,volume
    def get_security_bars(self,category,market,code,start=0,count=240):
        dict = {0:'SZ',1:'SH'}
        ts_code = code + "." + dict[market]
        order = ['code','ts_code','trade_date','trade_time','time_index','open','high','low','close','amount','volume']
        #df = self.api.get_security_bars(9, 0, '000001', 0, 10)  # 返回普通list
        df = self.api.to_df(self.api.get_security_bars(category, market, code, start, count))  # 返回DataFrame
        if df.empty:return df

        df.insert(0, 'ts_code', ts_code)
        df.insert(0, 'code', code)
        df['trade_time'] = df['datetime'].apply(lambda x: str(x)[11:19])
        df['time_index'] = df['trade_time'].apply(lambda x: datatime_util.stockTradeTime2Index(x))
        df['trade_date'] = df['datetime'].apply(lambda x: (str(x)[0:10]).replace('-', ''))
        df.rename(columns={'vol': 'volume'}, inplace=True)
        df.drop(['year','month','day','hour','minute','datetime'], axis=1, inplace=True)
        df['volume'] = df['volume'].apply(lambda x: int(x))  #取整
        df.loc[df['amount'] == 5.877471754111438e-39, 'amount'] = 0   #列值根据条件筛选后修改为0
        df = df[order]

        filename = config.tdx_csv_minline1_all + ts_code + ".csv"
        if os.path.isfile(filename):
            df.to_csv(filename, index=False, mode='a', header=False, sep=',', encoding="utf_8_sig")
        else:
            df.to_csv(filename, index=False, mode='w', header=True, sep=',', encoding="utf_8_sig")
            print("新增加的一分钟all股票数据：", filename)

    # 获取1分钟k线，最后一个参数说明需要获取的数量，本接口只获取从最近交易日往前的数据
    # 输入参数：五个参数分别为：category（k线),市场代码(0:深圳，1:上海),股票代码,开始位置(从最近交易日向前取，0表示最近交易日),返回的记录条数
    # K线种类:  0 5分钟K线; 1 15分钟K线; 2 30分钟K线; 3 1小时K线; 4 日K线;5 周K线;6 月K线;7 1分钟;8 1分钟K线; 9 日K线;10 季K线;11 年K线
    # 返回值：open,close,high,low,vol,amount,year,month,day,hour,minute,datetime
    # csv格式：code,ts_code,trade_date(缩写）,trade_time,time_index,open,high,low,close,amount,volume
    def get_security_bars_minute1(self, category, market, code, start, count):
        dict = {0: 'SZ', 1: 'SH'}
        ts_code = code + "." + dict[market]
        order = ['code', 'ts_code', 'trade_date', 'trade_time', 'time_index', 'open', 'high', 'low', 'close',
                 'amount', 'volume']
        # df = self.api.get_security_bars(9, 0, '000001', 0, 10)  # 返回普通list
        df = self.api.to_df(self.api.get_security_bars(category, market, code, start, count))  # 返回DataFrame
        if df.empty: return

        df.insert(0, 'ts_code', ts_code)
        df.insert(0, 'code', code)
        df['trade_time'] = df['datetime'].apply(lambda x: str(x)[11:19])
        df['time_index'] = df['trade_time'].apply(lambda x: datatime_util.stockTradeTime2Index(x))
        df['trade_date'] = df['datetime'].apply(lambda x: (str(x)[0:10]).replace('-', ''))
        df.rename(columns={'vol': 'volume'}, inplace=True)
        df.drop(['year', 'month', 'day', 'hour', 'minute', 'datetime'], axis=1, inplace=True)
        df['volume'] = df['volume'].apply(lambda x: int(x))  # 取整
        df.loc[df['amount'] == 5.877471754111438e-39, 'amount'] = 0  # 列值根据条件筛选后修改为0
        df = df[order]
        return df

    #可以获取多只股票的行情信息
    #返回值：market,code,active1,price,last_close,open,high,low,reversed_bytes0,reversed_bytes1,vol,cur_vol,amount,s_vol,
    #reversed_bytes2,reversed_bytes3,bid1,ask1,bid_vol1,ask_vol1,bid2,ask2,bid_vol2,ask_vol2,bid3,ask3,bid_vol3,ask_vol3,bid4,
    #ask4,bid_vol4,ask_vol4,bid5,ask5,bid_vol5,ask_vol5,reversed_bytes4,reversed_bytes5,reversed_bytes6,reversed_bytes7,
    #reversed_bytes8,reversed_bytes9,active2
    def get_security_quotes(self):
        df = self.api.to_df(self.api.get_security_quotes([(0, '000001'), (1, '600300')]))
        print(df)

    # 获取市场股票数量
    #返回值：value
    def get_security_count(self):
        df = self.api.to_df(self.api.get_security_count(0))  #0 - 深圳， 1 - 上海
        print(df)

    # 获取股票列表，返回值里面除了股票，还有国债等
    #返回值：code,volunit,decimal_point,name,pre_close
    def get_security_list(self):
        df = self.api.to_df(self.api.get_security_list(0, 10000))  # 市场代码, 起始位置 如： 0,0 或 1,100
        print(df)

    # 获取指数k线
    #输入参数同股票k线接口
    # 返回值：open,close,high,low,vol,amount,year,month,day,hour,minute,datetime,up_count  down_count
    def get_index_bars(self):
        index_dict_cn = {"上证指数":"999999","深证成指":"399001","中小板指":"399005","创业板指":"399006","深证综指":"399106","上证50":"000016","沪深300":"000300"}
        index_dict = {"sh": "999999", "sz": "399001", "zxb": "399005", "cyb": "399006", "szz": "399106",
                         "sz50": "000016", "hs300": "000300"}
        for key in index_dict.keys():
            df = self.api.to_df(self.api.get_index_bars(9,1, index_dict[key], 0, 2))
            print(df)

    # 查询分时行情，最近交易日的数据，一分钟一条记录
    #返回值：price,vol
    def get_minute_time_data(self):
        df = self.api.to_df(self.api.get_minute_time_data(1, '600300'))  #市场代码， 股票代码
        print(df)

    # 查询历史分时行情
    # 返回值：price,vol
    def get_history_minute_time_data(self):
        df = self.api.to_df(self.api.get_history_minute_time_data(TDXParams.MARKET_SH, '603887', 20200420))  #市场代码， 股票代码，时间
        print(df)

    # 查询分笔成交，最近交易日数据
    #返回值：time，price，vol，num，buyorsell
    def get_transaction_data(self):
        df = self.api.to_df(self.api.get_transaction_data(TDXParams.MARKET_SZ, '000001', 0, 30))  #市场代码， 股票代码，起始位置， 数量
        print(df)

    # 查询历史分笔成交
    #返回值:time,price,vol,buyorsell
    def get_history_transaction_data(self):
        df = self.api.to_df(self.api.get_history_transaction_data(TDXParams.MARKET_SZ, '000001', 0, 10, 20170209))  #市场代码， 股票代码，起始位置，日期 数量
        print(df)

    # 查询公司信息目录,返回的不是具体数据
    #返回值:name,filename,start,length
    def get_company_info_category(self):
        df = self.api.to_df(self.api.get_company_info_category(TDXParams.MARKET_SZ, '000001'))  #市场代码， 股票代码
        print(df)

    # 读取公司信息详情
    #返回值:value
    def get_company_info_content(self):
        df = self.api.to_df(self.api.get_company_info_content(0, '000001', '000001.txt', 0, 1000))  #市场代码， 股票代码, 文件名, 起始位置， 数量
        print(df)

    # 读取除权除息信息
    #返回值:year,month,day,category,name,fenhong,peigujia,songzhuangu,peigu
    def get_xdxr_info(self):
        df = self.api.to_df(self.api.get_xdxr_info(1, '600300'))  #市场代码， 股票代码
        print(df)

    # 读取财务信息
    #返回值:market,code,liutongguben,province,industry,updated_date,ipo_date,zongguben,guojiagu,faqirenfarengu,farengu,bgu,hgu,zhigonggu,
    #zongzichan,liudongzichan,gudingzichan,wuxingzichan,gudongrenshu,liudongfuzhai,changqifuzhai,zibengongjijin,jingzichan,zhuyingshouru,
    #zhuyinglirun,yingshouzhangkuan,yingyelirun,touzishouyu,jingyingxianjinliu,zongxianjinliu,cunhuo,lirunzonghe,shuihoulirun,jinglirun,weifenlirun,baoliu1,baoliu2
    def get_finance_info(self):
        df = self.api.to_df(self.api.get_finance_info(1, '600300'))  #市场代码， 股票代码
        print(df)

    # 读取k线信息
    # 返回值:value
    def get_k_data(self):
        df = self.api.to_df(self.api.get_k_data('600300','2017-07-03','2017-07-10'))  #股票代码， 开始时间， 结束时间
        print(df)

    # 读取板块信息
    #返回值：blockname, block_type, code_index, code
    """   BLOCK_SZ = "block_zs.dat";BLOCK_FG = "block_fg.dat";BLOCK_GN = "block_gn.dat";BLOCK_DEFAULT = "block.dat"  """
    def get_and_parse_block_info(self):
        ##指数板块 风格板块  概念板块  一般板块
        block_filename = ["block_zs.dat", "block_fg.dat", "block_gn.dat", "block.dat"]
        for block in block_filename:
            df = self.api.to_df(self.api.get_and_parse_block_info(block))  #板块文件名称
            filename = config.tdx_csv_block + block[0:-4] + ".csv"
            if os.path.isfile(filename):
                os.remove(filename)
                df.to_csv(filename, index=False, mode='w', header=True, sep=',', encoding="utf_8_sig")
            else:
                df.to_csv(filename, index=False, mode='w', header=True, sep=',', encoding="utf_8_sig")

    #返回值：0没有提取到数据；1提取到数据
    def get_minute1_data(self, category, market, code, start_date, end_date):
        init_start_date = start_date.replace('-', '')
        init_end_date = end_date.replace('-', '')
        day = datatime_util.diffrentPeriod(datatime_util.DAILY, start_date, end_date)
        df = self.get_security_bars_minute1(category, market, code, 0, 240 * 3)  # 返回DataFrame
        if df is None or df.empty:
            print('{0}没有交易数据'.format(code))
            return 0
        print(market,'--', code, '--', start_date, '--', end_date)
        #print("最大值：",df.groupby('datetime').max())
        #print(df.describe())   #df数据统计
        data_start_date = df.min()['trade_date']
        data_end_date = df.max()['trade_date']

        start_date = start_date.replace('-', '')
        end_date = end_date.replace('-', '')
        if data_end_date < start_date or end_date < data_start_date:
            print("采集时间在数据范围之外，退出函数")
            return 0
        elif end_date > data_end_date:
            end_date = data_end_date

        if start_date < data_start_date:
            #最近三天的数据中，去掉无用的数据后即是最终数据
            #需要取的数据还有三天前的数据，需要继续向前取
            n = (day - 3) // 3
            m = (day - 3) % 3
            for i in range(0, n):
                dfn = self.get_security_bars_minute1(category, market, code, 240 * 3 * i, 240 * 3)  # 返回DataFrame
                if (not (dfn is None)) and (not dfn.empty): df = dfn.append(df,ignore_index=True)
            if m > 0:
                dfn = self.get_security_bars_minute1(category, market, code, 240 * 3 * (n + 1), 240 * m)  # count=240 * day
                if (not (dfn is None)) and (not dfn.empty): df = dfn.append(df,ignore_index=True)

        df = df.sort_values(by=['trade_date','time_index'], axis=0, ascending=True)
        #过滤掉start_date, end_date之外的数据
        df = df[(df['trade_date'] >= str(init_start_date)) & (df['trade_date'] <= str(init_end_date))] #每个条件要用括号()括起来

        dict = {0: 'SZ', 1: 'SH'}
        ts_code = code + "." + dict[market]
        filename = config.tdx_csv_minline1_all + ts_code + ".csv"
        if os.path.isfile(filename):
            df.to_csv(filename, index=False, mode='a', header=False, sep=',', encoding="utf_8_sig")
            print("更新一分钟all股票数据：", filename)
        else:
            df.to_csv(filename, index=False, mode='w', header=True, sep=',', encoding="utf_8_sig")
            print("新增加的一分钟all股票数据：", filename)

if __name__ == '__main__':
    tdx = TdxHelper()
    #tdx.get_security_bars(7, 0, '000001',2*240, 1*240)
    #tdx.get_security_count()
    tdx.get_minute1_data(7, 0, '000518','2020-04-21', '2020-04-25')
    tdx.close_connect()