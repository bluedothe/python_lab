#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/3/28
    1从同花顺网页爬取板块数据，包括板块名称和板块成分股
    2获取个股换手率、流通股、流通市值、市盈率
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import os
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re
from lxml import etree
import pandas as pd
import html5lib
import time

from stock_data import mysql_script
from db.mysqlHelper import mysqlHelper
from stock_data import bluedothe
from stock_data import config

class ThsHelper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        browser = webdriver.Chrome(chrome_options=options)
        url = "http://q.10jqka.com.cn/thshy/"
        browser.get(url)
        # 获取cookie列表
        cookies = browser.get_cookies()
        browser.close()
        self.cookie = cookies[0]['value']

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Referer': 'http://q.10jqka.com.cn/thshy/detail',
            'Cookie': 'v={}'.format(self.cookie)
        }

    # 获取网页详情页
    def get_page_bs(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                html = response.text.encode('utf-8')
                bs = BeautifulSoup(html, "html.parser")  #lxml   html
                return bs
            return None
        except RequestException:
            print('请求页面失败', url)
            return None

    # 获取网页详情页
    def get_page_html(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                html = response.text.encode('utf-8')
                return html
            return None
        except RequestException:
            print('请求页面失败', url)
            return None

    # 同花顺行业数据
    def get_block_thshy(self):
        thshy_code_name = []  # 行业代码名称字典
        thshy_codes_href = []  # 行业代码链接字典
        url = "http://q.10jqka.com.cn/thshy/index/field/199112/order/desc/page/{}/ajax/1/"
        page_no = 1
        while True:
            bs = self.get_page_bs(url.format(page_no))
            if bs is None:
                print("page_no",page_no)
                break
            list = bs.find('tbody').find_all("a", target="_blank", href=re.compile("q.10jqka.com.cn/thshy"))
            if len(list) == 0:
                print("page_no", page_no)
                break
            #print(list)
            #print(len(list))
            for line in list:
                href = str((line.get('href')))
                block_name = line.get_text
                block_code = href.split("/")[-2]
                thshy_code_name.append({"code": block_code, "name": block_name})
                thshy_codes_href.append({"code": block_code, "href": href})
            page_no = page_no + 1
        print(thshy_code_name)
        print(len(thshy_code_name))
        print(thshy_codes_href)
        print(len(thshy_codes_href))

    # 同花顺行业成分股数据
    def get_block_member_thshy(self,block_code):
        thshy_stock_code = []  # 行业代码名称字典
        url = "http://q.10jqka.com.cn/thshy/detail/field/199112/order/desc/page/{}/ajax/1/code/{}"
        page_no = 1
        while True:
            html = self.get_page_bs(url.format(page_no,block_code))
            if html is None:
                print("page_no(none): ", page_no)
                break
            list = html.find('tbody').find_all("a", target="_blank", href=re.compile("http://stockpage.10jqka.com.cn"))
            ##selector = etree.HTML(html)
            ##list = selector.xpath('//table[@class="m-table m-pager-table"]/tbody')  #'//table[@class="m-table m-pager-table"]/tbody/tr[1]/td[2]/a'
            if len(list) == 0:
                print("page_no(0): ", page_no)
                break

            i = 0
            for line in list:
                i = i + 1
                if i % 2 == 0:continue
                #href = str((line.get('href')))
                thshy_stock_code.append(line.string)

            page_no = page_no + 1
        print(thshy_stock_code)

    # 证监会行业数据
    def get_block_zjhhy(self):
        thshy_code_name = []  # 行业代码名称字典
        thshy_codes_href = []  # 行业代码链接字典
        url = "http://q.10jqka.com.cn/zjhhy"

        bs = self.get_page_bs(url)

        list = bs.find('tbody').find_all("a", target="_blank", href=re.compile(url))
        if len(list) == 0:return
        # print(list)
        # print(len(list))
        for line in list:
            print(line)
            href = str((line.get('href')))
            block_name = line.string
            block_code = href.split('/')[-2]
            thshy_code_name.append({"code": block_code, "name": block_name})
            thshy_codes_href.append({"code": block_code, "href": href})

        print(thshy_code_name)
        print(len(thshy_code_name))
        print(thshy_codes_href)
        print(len(thshy_codes_href))

    # 证监会行业成分股数据
    def get_block_member(self, url, block_code):
        thshy_stock_code = []  # 行业代码名称字典 <span class="page_info">1/11</span>
        #url = "http://q.10jqka.com.cn/zjhhy/detail/field/199112/order/desc/page/{}/ajax/1/code/{}"  #证监会行业
        #url = "http://q.10jqka.com.cn/thshy/detail/field/199112/order/desc/page/{}/ajax/1/code/{}"  #同花顺行业
        #url = "http://q.10jqka.com.cn/dy/detail/field/199112/order/desc/page/{}/ajax/1/code/{}"     #地域
        #url = "http://q.10jqka.com.cn/gn/detail/field/264648/order/desc/page/{}/ajax/1/code/{}"     #概念

        html = self.get_page_bs(url.format(1, block_code))
        if html is None: return 0
        page_no_span = html.find("span", class_="page_info")
        if page_no_span is None:return 0
        page_sum = int((page_no_span.string).split('/')[-1])

        page_no = 1
        while True:
            if page_no > page_sum: break
            html = self.get_page_bs(url.format(page_no, block_code))
            if html is None:
                print("page_no(none): ", page_no)
                break
            list = html.find('tbody').find_all("a", target="_blank",
                                               href=re.compile("http://stockpage.10jqka.com.cn"))
            ##selector = etree.HTML(html)
            ##list = selector.xpath('//table[@class="m-table m-pager-table"]/tbody')  #'//table[@class="m-table m-pager-table"]/tbody/tr[1]/td[2]/a'
            if len(list) == 0:
                print("page_no(0): ", page_no)
                break

            i = 0
            for line in list:
                i = i + 1
                if i % 2 == 0: continue
                # href = str((line.get('href')))
                thshy_stock_code.append(line.string)

            page_no = page_no + 1
        print(thshy_stock_code)

    # 地域数据，与证监会行业函数通用
    def get_block_dy(self):
        thshy_code_name = []  # 行业代码名称字典
        thshy_codes_href = []  # 行业代码链接字典
        url = "http://q.10jqka.com.cn/dy"

        bs = self.get_page_bs(url)

        list = bs.find('tbody').find_all("a", target="_blank", href=re.compile(url))
        if len(list) == 0: return
        # print(list)
        # print(len(list))
        for line in list:
            print(line)
            href = str((line.get('href')))
            block_name = line.string
            block_code = href.split('/')[-2]
            thshy_code_name.append({"code": block_code, "name": block_name})
            thshy_codes_href.append({"code": block_code, "href": href})

        print(thshy_code_name)
        print(len(thshy_code_name))
        print(thshy_codes_href)
        print(len(thshy_codes_href))

    # 地域成分股数据
    def get_block_member_dy(self):
        thshy_stock_code = []  # 行业代码名称字典 <span class="page_info">1/11</span>
        url = "http://q.10jqka.com.cn/dy/detail/field/199112/order/desc/page/{}/ajax/1/code/{}"
        self.get_block_member(url,'882005')

    # 概念数据
    def get_block_gn(self):
        thshy_code_name = []  # 行业代码名称字典
        thshy_codes_href = []  # 行业代码链接字典
        url = "http://q.10jqka.com.cn/gn/index/field/addtime/order/desc/page/{}/ajax/1/"

        html = self.get_page_bs(url.format(1))
        if html is None: return 0
        page_no_span = html.find("span", class_="page_info")
        if page_no_span is None: return 0
        page_sum = int((page_no_span.string).split('/')[-1])

        page_no = 1
        while True:
            if page_no > page_sum: break
            bs = self.get_page_bs(url.format(page_no))
            if bs is None:
                print("page_no", page_no)
                break
            list = bs.find('tbody').find_all("a", target="_blank", href=re.compile("q.10jqka.com.cn/gn"))
            if len(list) == 0:
                print("page_no", page_no)
                break
            # print(list)
            # print(len(list))
            for line in list:
                href = str((line.get('href')))
                block_name = line.string
                block_code = href.split("/")[-2]
                thshy_code_name.append({"code": block_code, "name": block_name})
                thshy_codes_href.append({"code": block_code, "href": href})
                #---
                tr = line.parent.parent
                i = 1
                for child in tr.find_all('td'):
                    if i == 1:print("date:", child.string)
                    if i == 2:
                        block_name = line.string
                        href = child.find("a").get('href')
                        block_code = href.split("/")[-2]
                        print("name:", block_name)
                        print("href:", href)
                        print("code:", block_code)
                    if i == 3: print("desc:", child.string)
                    if i == 5: print("sum:", child.string)
                    i = i + 1
                break
            break
            #---
            page_no = page_no + 1
        print(thshy_code_name)
        print(len(thshy_code_name))
        print(thshy_codes_href)
        print(len(thshy_codes_href))

    # 概念成分股数据
    def get_block_member_gn(self):
        thshy_stock_code = []  # 行业代码名称字典 <span class="page_info">1/11</span>
        url = "http://q.10jqka.com.cn/gn/detail/field/264648/order/desc/page/{}/ajax/1/code/{}"
        self.get_block_member(url, '301209')

    #获取个股每日换手率、流通股、流通市值、市盈率
    def stock_day_info(self):
        thshy_code_name = []  # 行业代码名称字典
        thshy_codes_href = []  # 行业代码链接字典
        url = "http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/{}/ajax/1/"

        html = self.get_page_bs(url.format(1))
        if html is None: return 0
        page_no_span = html.find("span", class_="page_info")
        if page_no_span is None: return 0
        page_sum = int((page_no_span.string).split('/')[-1])

        page_no = 1
        while True:
            if page_no > page_sum: break
            bs = self.get_page_bs(url.format(page_no))
            if bs is None:
                print("page_no", page_no)
                break
            list = bs.find('tbody').find_all("a", target="_blank", href=re.compile("http://stockpage.10jqka.com.cn"))
            if len(list) == 0:
                print("page_no", page_no)
                break
            # print(list)
            # print(len(list))
            for line in list:
                href = str((line.get('href')))
                block_name = line.string
                block_code = href.split("/")[-2]
                thshy_code_name.append({"code": block_code, "name": block_name})
                thshy_codes_href.append({"code": block_code, "href": href})
                # ---
                tr = line.parent.parent
                i = 1
                for child in tr.find_all('td'):
                    if i == 1: print("date:", child.string)
                    if i == 2:
                        block_name = line.string
                        href = child.find("a").get('href')
                        block_code = href.split("/")[-2]
                        print("name:", block_name)
                        print("href:", href)
                        print("code:", block_code)
                    if i == 3: print("desc:", child.string)
                    if i == 5: print("sum:", child.string)
                    i = i + 1
                break
            break
            # ---
            page_no = page_no + 1
        print(thshy_code_name)
        print(len(thshy_code_name))
        print(thshy_codes_href)
        print(len(thshy_codes_href))

    #获取每只股票的附加数据并写入csv
    # 获取个股每日涨跌幅、涨跌、换手率、量比、振幅、流通股、流通市值、市盈率
    def get_day_attach(self, trade_date = ""):
        url = "http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/{}/ajax/1/"
        if len(trade_date) == 0: trade_date = time.strftime("%Y%m%d")  #如果没指定交易日期则用当天日期

        html = self.get_page_bs(url.format(1))
        if html is None: return 0
        page_no_span = html.find("span", class_="page_info")
        if page_no_span is None: return 0
        page_sum = int((page_no_span.string).split('/')[-1])

        page_no = 1
        while True:
            if page_no > page_sum: break
            bs = self.get_page_bs(url.format(page_no))
            if bs is None:
                print("page_no", page_no)
                break
            table = bs.table
            df = pd.read_html(table.prettify(), attrs={"class":"m-table m-pager-table"}, converters={1:lambda x: str(x) + ".SH" if str(x)[0:1] == '6' else str(x) + ".SZ"})[0]  #converters将股票代码转换为ts_code
            df.drop(df.columns[[0, 3, 6, 10, 14]], axis=1, inplace=True)  #删除不需要的列
            df.columns = ['ts_code', 'name', 'pct_chg', 'price_change', 'turnover_rate', 'qrr', 'amplitude', 'circulate_num', 'circulate_amount', 'per']   #重命名列名:代码,名称,换手(%),流通股,流通市值,市盈率
            if page_no == 1:
                dfall = df
            else:
                dfall = dfall.append(df, ignore_index=True)  # 两个df纵向合并，即追加数据
            page_no = page_no + 1

        dfall.insert(0,'code', dfall['ts_code'].apply(lambda x: str(x)[0:6]))
        dfall.insert(2, 'trade_date', trade_date)
        print(dfall)
        print(len(dfall))

        for i in range(len(dfall)):
            df = dfall.iloc[i:i+1]   #取dataframe对象必须用iloc[i:i+1]写法
            print(type(df))
            ts_code = dfall.iloc[i]['ts_code']  #iloc[i]取出的是一行的元组对象

            filename = config.ths_csv_day_attach + ts_code + ".csv"
            if os.path.isfile(filename):
                df.to_csv(filename, index=False, mode='a', header=False, sep=',', encoding="utf_8_sig")
                print("更新一分钟all股票数据：", filename)
            else:
                df.to_csv(filename, index=False, mode='w', header=True, sep=',', encoding="utf_8_sig")
                print("新增加的一分钟all股票数据：", filename)

if __name__ == '__main__':
    ths = ThsHelper()
    ths.stock_day_info2()