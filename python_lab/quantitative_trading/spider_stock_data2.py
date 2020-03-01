#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2019/11/29
    爬取股票交易数据
'''

import requests
from fake_useragent import UserAgent
import re
import csv
#import ssl
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2019"


def getHtml(url):
    r = requests.get(url, headers={
        'User-Agent': UserAgent().random,
    })
    r.encoding = r.apparent_encoding
    return r.text

def get_data():
    stockUrl = 'http://quote.eastmoney.com/stocklist.html'
    PATTERN_STOCK = "<li><a.*>(\w*)\((\d{6})\)</a></li>"
    if __name__ == '__main__':
        html = getHtml(stockUrl)
        reslist = re.findall(PATTERN_STOCK, html)
        # 数据清洗：去掉非个股,个股以6（沪市）,0（深市）,3（创业板）开头
        datalist = reslist[:]
        for res in reslist:
            if not (str(res[1]).startswith('6') or str(res[1]).startswith('3') or str(res[1]).startswith('0')):
                datalist.remove(res)
        f = open('D:/Py/stock.csv', 'w+', encoding='utf-8', newline="")
        writer = csv.writer(f)
        writer.writerow(('名称', '代码'))
        for data in datalist:
            writer.writerow((data[0], data[1]))
        f.close()



if __name__ == '__main__':
    get_data()