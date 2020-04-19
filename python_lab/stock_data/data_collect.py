#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/4/9
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

from stock_data import tushare_data_collect
from stock_data import tdx_data_collect

class DataCollect:
    def __init__(self):
        self.thshare_dc = tushare_data_collect()
        self.tdx_dc = tdx_data_collect()

    def batch_execute(self):
        self.thshare_dc.batch_execute()

if __name__ == '__main__':
    dc = DataCollect()
    dc.batch_execute()   #批量执行


