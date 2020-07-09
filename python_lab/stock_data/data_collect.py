#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/4/9
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

from stock_data.tushare_data_collect import TushareDataCollect
from stock_data.tdx_data_collect import TdxDataCollect
from stock_data.ths_data_collect import ThsDataCollect
from tool import kit
class DataCollect:
    def __init__(self):
        self.tushare_dc = TushareDataCollect()
        self.tdx_dc = TdxDataCollect()
        self.ths_dc = ThsDataCollect()

    def batch_execute(self):
        #self.tushare_dc.batch_execute_everyday() #1更新股票信息；2追加tusharepro+tushare日线数据；3追加tusharepro;4追加指数日线数据；

        self.tdx_dc.batch_execute_everyday() #1追加分钟数据；2板块数据以及成分数据
        self.tdx_dc.tdx_close_connect()

        self.ths_dc.batch_execute_everyday()  #1追加日线附加数据 2更新板块数据以及成分数据
        kit.alarm(3)

if __name__ == '__main__':
    dc = DataCollect()
    dc.batch_execute()   #批量执行


