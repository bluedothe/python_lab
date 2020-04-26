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

class DataCollect:
    def __init__(self):
        self.tushare_dc = TushareDataCollect()
        self.tdx_dc = TdxDataCollect()

    def batch_execute(self):
        #self.tushare_dc.batch_execute_everyday()
        self.tdx_dc.batch_execute_everyday()

if __name__ == '__main__':
    dc = DataCollect()
    dc.batch_execute()   #批量执行


