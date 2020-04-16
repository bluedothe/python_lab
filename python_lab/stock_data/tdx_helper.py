#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/3/28
    通过通达信本地数据获取股票数据
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

from pytdx.hq import TdxHq_API,TDXParams
from pytdx.exhq import TdxExHq_API

class TdxHelper:
    def __init__(self):
        self.api = TdxHq_API()

    def get_data(self):
        if self.api.connect('119.147.212.81', 7709):
            data = self.api.get_security_bars(9, 0, '000001', 0,
                                              10)  # 返回普通list,五个参数分别为：category（k线),市场代码(深市),股票代码,开始时间,记录条数
            print(data)
            data = self.api.to_df(self.api.get_security_bars(9, 0, '000001', 0, 10))  # 返回DataFrame
            print(data)
            self.api.disconnect()

if __name__ == '__main__':
    tdx = TdxHelper()
    tdx.get_data()