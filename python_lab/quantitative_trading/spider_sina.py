#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/5/1
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import requests
import re
import json
import pandas as pd

def get_block():
    res = requests.get('http://vip.stock.finance.sina.com.cn/q/view/newSinaHy.php')
    res.encoding = 'gbk'
    res.text
    #%%
    table_text = re.findall('\{.*\}',res.text)[0]
    table_text
    #%%
    bk = json.loads(table_text)
    bk

    #%%
    bk.keys()
    #%%
    bk.values()
    #%%
    list_values = bk.values()
    len(list_values)
    #%%
    df_bk = pd.DataFrame.from_dict(bk,orient='index',columns=['info'])
    #%%
    print(df_bk)
    #%%
    values = df_bk['info'].str.split(",",expand=True)
    values.columns=['板块编码','板块','公司家数','平均价格','涨跌额','涨跌幅','总成交量','总成交金额','领涨股代码','涨跌幅','当前价','涨跌额','领涨股名称']
    values.to_csv("d:\\bk.csv",encoding='gbk')


if __name__ == '__main__':
    get_block()