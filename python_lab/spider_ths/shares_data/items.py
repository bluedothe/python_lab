#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/7/15
'''

import scrapy

class Company(scrapy.Item):
    # 股票代码
    share_id = scrapy.Field()
    # 公司简称
    nick_name = scrapy.Field()
    # 公司全称
    name = scrapy.Field()
    # 营收
    revenue = scrapy.Field()
    # 年份
    year = scrapy.Field()
    # 总市值
    market_value = scrapy.Field()
    # 建立时间
    start_time = scrapy.Field()
    # 上市时间
    market_time = scrapy.Field()

if __name__ == '__main__':
    pass