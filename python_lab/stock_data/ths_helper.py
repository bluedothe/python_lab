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

from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re
import pandas as pd
import time

from stock_data import mysql_script
from config import config
from tool import file_util

class ThsHelper:
    def __init__(self):
        # pandas数据显示设置
        pd.set_option('display.max_columns', None)  # 显示所有列
        pd.set_option('display.max_rows', None)  # 显示所有行

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

        self.data_source = "ths"


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
        block_category = self.data_source + ".thshy"
        block_type = block_category + '.1'
        block_info = []  # 板块数据数组，里面包含板块字典
        block_member = []  # 板块成员数组，里面包含成员字典
        url = "http://q.10jqka.com.cn/thshy/index/field/199112/order/desc/page/{}/ajax/1/"

        html = self.get_page_bs(url.format(1))
        if html is None: return None
        page_no_span = html.find("span", class_="page_info")
        if page_no_span is None: return None
        page_sum = int((page_no_span.string).split('/')[-1])
        print('page_sum:', page_sum)

        page_no = 0
        while True:
            page_no = page_no + 1
            if page_no > page_sum: break
            bs = self.get_page_bs(url.format(page_no))
            if bs is None:
                print("bs is None，page_no: ", page_no)
                continue
            if bs.find('tbody') is None:
                print("tbody is None,page_no:",page_no)
                continue
            list = bs.find('tbody').find_all("a", target="_blank", href=re.compile("q.10jqka.com.cn/thshy"))
            if len(list) == 0:
                print("list==0, page_no: ", page_no)
                break
            print('page_no:',page_no)

            for line in list:
                href = str((line.get('href')))
                block_name = line.string
                block_code = href.split("/")[-2]
                print(block_code,block_name)

                ###ts_codes = self.get_block_member(block_category, block_code)
                ###block_info.append({"data_source": self.data_source, "block_category": block_category, "block_type": block_type,"block_name": block_name,"block_code": block_code, "member_count": len(ts_codes)})

                ###for ts_code in ts_codes:block_member.append({"data_source": self.data_source, "block_category": block_category, "block_type": block_type,"block_name": block_name, "block_code": block_code, "ts_code": ts_code})
        ###return self.save_df(block_category, block_info, block_member)

    # 同花顺行业成分股数据
    def get_block_member_thshy(self,block_code):
        thshy_stock_code = []  # 行业代码名称字典
        url = "http://q.10jqka.com.cn/thshy/detail/field/199112/order/desc/page/{}/ajax/1/code/{}"
        page_no = 0
        while True:
            page_no = page_no + 1
            html = self.get_page_bs(url.format(page_no,block_code))
            if html is None:
                print("page_no(none): ", page_no)
                break
            if html.find('tbody') is None:continue
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

        print(thshy_stock_code)
        print(len(thshy_stock_code))

    # 证监会行业数据
    def get_block_zjhhy(self):
        block_category = self.data_source + ".zjhhy"
        block_type = block_category + '.2'
        block_info = []  # 板块数据数组，里面包含板块字典
        block_member = []  # 板块成员数组，里面包含成员字典
        url = "http://q.10jqka.com.cn/zjhhy"

        html = self.get_page_bs(url)
        list = html.find('tbody').find_all("a", target="_blank", href=re.compile(url))
        if len(list) == 0:return None
        for line in list:
            href = str((line.get('href')))
            block_name = line.string
            block_code = href.split('/')[-2]

            ts_codes = self.get_block_member(block_category, block_code)
            block_info.append(
                {"data_source": self.data_source, "block_category": block_category, "block_type": block_type,
                 "block_name": block_name, "block_code": block_code, "member_count": len(ts_codes)})

            for ts_code in ts_codes:
                block_member.append(
                    {"data_source": self.data_source, "block_category": block_category, "block_type": block_type,
                     "block_name": block_name, "block_code": block_code, "ts_code": ts_code})

        return self.save_df(block_category, block_info, block_member)

    # 成分股数据，返回ts_code格式股票代码数组
    def get_block_member_bak(self, block_category, block_code):
        member_stock_code = set()  # 行业代码集合
        if block_category == "ths.zjhhy":
            url = "http://q.10jqka.com.cn/zjhhy/detail/field/199112/order/desc/page/{}/ajax/1/code/{}"  #证监会行业
        elif block_category == "ths.thshy":
            url = "http://q.10jqka.com.cn/thshy/detail/field/199112/order/desc/page/{}/ajax/1/code/{}"  #同花顺行业
        elif block_category == "ths.dy":
            url = "http://q.10jqka.com.cn/dy/detail/field/199112/order/desc/page/{}/ajax/1/code/{}"     #地域
        elif block_category == "ths.gn":
            url = "http://q.10jqka.com.cn/gn/detail/field/264648/order/desc/page/{}/ajax/1/code/{}"     #概念

        html = self.get_page_bs(url.format(1, block_code))
        page_no_span = html.find("span", class_="page_info")
        if page_no_span is None:
            url = "http://q.10jqka.com.cn/zjhhy/detail/code/{}/"
            page_sum = 1
        else:
            page_sum = int((page_no_span.string).split('/')[-1])
        print('page_sum:',page_sum)
        page_no = 0
        while True:
            page_no = page_no + 1
            if page_no > page_sum: break
            if page_no_span is None:
                html = self.get_page_bs(url.format(block_code))
                if html is None: continue
            else:
                html = self.get_page_bs(url.format(page_no, block_code))
            #print("page_no:",page_no)
            #print("url:", url)
            #print(html)
            if html.find('tbody') is None:
                print("tbody is None,page_no:",page_no)
                continue
            list = html.find('tbody').find_all("a", target="_blank", href=re.compile("http://stockpage.10jqka.com.cn"))
            ##selector = etree.HTML(html)
            ##list = selector.xpath('//table[@class="m-table m-pager-table"]/tbody')  #'//table[@class="m-table m-pager-table"]/tbody/tr[1]/td[2]/a'
            if len(list) == 0:
                print("page_no(0): ", page_no)
                continue

            i = 0
            for line in list:
                i = i + 1
                if i % 2 == 1:
                    href = str((line.get('href')))
                    code_str = line.string
                    code = href.split('/')[-2]
                    handle_code = lambda x: x + '.SH' if x[0] == '6' else x + '.SZ'
                    member_stock_code.add(handle_code(code))

        return member_stock_code

    # 成分股数据，返回ts_code格式股票代码数组
    def get_block_member(self, block_category, block_code):
        member_stock_code = set()  # 行业代码集合
        block_category = block_category.split('.')[-1]
        url = "http://q.10jqka.com.cn/{}/detail/field/199112/order/desc/page/{}/ajax/1/code/{}"
        url_one = "http://q.10jqka.com.cn/{}/detail/code/{}/"

        html = self.get_page_bs(url.format(block_category, 1, block_code))
        page_no_span = html.find("span", class_="page_info")
        if page_no_span is None:
            page_sum = 1
        else:
            page_sum = int((page_no_span.string).split('/')[-1])
        print('page_sum:', page_sum)
        page_no = 0
        while True:
            page_no = page_no + 1
            if page_no > page_sum: break
            if page_no_span is None:
                html = self.get_page_bs(url_one.format(block_category, block_code))
                if html is None: continue
            else:
                html = self.get_page_bs(url.format(block_category,page_no, block_code))

            table = html.table
            if table is None:
                print("table is None,page_no:", page_no)
                html = self.get_page_bs(url.format(block_category, page_no, block_code))
                print(html)
                continue
            df = pd.read_html(table.prettify(), attrs={"class": "m-table m-pager-table"},
                              converters={1: lambda x: str(x) + ".SH" if str(x)[0:1] == '6' else str(x) + ".SZ"})[0]  # converters将股票代码转换为ts_code
            df.drop(df.columns[[0,2, 3,4,5, 6,7,8,9, 10,11,12,13, 14]], axis=1, inplace=True)  # 删除不需要的列
            df.columns = ['ts_code']  # 重命名列名:代码,名称,换手(%),流通股,流通市值,市盈率
            df = df.drop_duplicates(subset=['ts_code'], keep='first');  # 按指定字段去重, 保留第一个
            if page_no == 1:
                dfall = df
            else:
                dfall = dfall.append(df, ignore_index=True)  # 两个df纵向合并，即追加数据
        member_stock_code = dfall.values.T.tolist()[0]
        print('value:', member_stock_code)
        print('type:',type(member_stock_code))

        return member_stock_code

    # 地域数据，与证监会行业函数通用
    def get_block_dy(self):
        block_category = self.data_source + ".dy"
        block_type = block_category + '.3'
        block_info = []  # 板块数据数组，里面包含板块字典
        block_member = []  # 板块成员数组，里面包含成员字典
        url = "http://q.10jqka.com.cn/dy"

        html = self.get_page_bs(url)
        list = html.find('tbody').find_all("a", target="_blank", href=re.compile(url))
        if len(list) == 0: return None
        for line in list:
            href = str((line.get('href')))
            block_name = line.string
            block_code = href.split('/')[-2]
            ts_codes = self.get_block_member(block_category, block_code)
            block_info.append(
                {"data_source": self.data_source, "block_category": block_category, "block_type": block_type,
                 "block_name": block_name, "block_code": block_code, "member_count": len(ts_codes)})

            for ts_code in ts_codes:
                block_member.append(
                    {"data_source": self.data_source, "block_category": block_category, "block_type": block_type,
                     "block_name": block_name, "block_code": block_code, "ts_code": ts_code})

        return self.save_df(block_category, block_info, block_member)

    # 获取概念板块数据
    def get_block_gn(self):
        block_category = self.data_source + ".gn"
        block_type = block_category + '.4'
        block_info = []  #板块数据数组，里面包含板块字典
        block_member = []  # 板块成员数组，里面包含成员字典
        url = "http://q.10jqka.com.cn/gn/index/field/addtime/order/desc/page/{}/ajax/1/"

        html = self.get_page_bs(url.format(1))
        if html is None: return None
        page_no_span = html.find("span", class_="page_info")
        if page_no_span is None: return None
        page_sum = int((page_no_span.string).split('/')[-1])
        print('page_sum:', page_sum)
        page_no = 0
        while True:
            page_no = page_no + 1
            if page_no > page_sum: break
            bs = self.get_page_bs(url.format(page_no))
            if bs is None:
                print("bs is None，page_no: ", page_no)
                break
            list = bs.find('tbody').find_all("a", target="_blank", href=re.compile("q.10jqka.com.cn/gn"))
            if len(list) == 0:
                print("list==0, page_no: ", page_no)
                break
            print('page_no:',page_no)
            for line in list:
                #获取tr数据
                tr = line.parent.parent
                i = 0
                for child in tr.find_all('td'):
                    i = i + 1
                    if i == 4: continue
                    if i == 1: gn_date = child.string
                    if i == 2:
                        block_name = line.string
                        href = child.find("a").get('href')
                        block_code = href.split("/")[-2]
                    if i == 3: gn_event = child.string
                    if i == 5: member_count = child.string
                block_info.append({"data_source":self.data_source, "block_category":block_category, "block_type":block_type, "block_name":block_name,
                                   "block_code":block_code, "member_count":member_count, "gn_date":gn_date, "gn_event":gn_event, "href":href})
                ts_codes = self.get_block_member(block_category,block_code)
                for ts_code in ts_codes:
                    block_member.append({"data_source":self.data_source, "block_category":block_category, "block_type":block_type, "block_name":block_name,
                                   "block_code":block_code, "ts_code":ts_code})

        block_info_df = pd.DataFrame(block_info)
        block_info_df['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        block_info_df = block_info_df[
            ['data_source', 'block_category', 'block_type', 'block_name', 'block_code', 'member_count', 'gn_date', 'gn_event', 'create_time']]
        block_info_df = block_info_df.drop_duplicates(
            subset=['data_source', 'block_category', 'block_type', 'block_name', 'block_code'],
            keep='first');  # 按指定字段去重, 保留第一个
        block_member_df = pd.DataFrame(block_member)
        block_member_df['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        block_member_df = block_member_df[
            ['data_source', 'block_category', 'block_type', 'block_name', 'block_code', 'ts_code', 'create_time']]
        block_member_df = block_member_df.drop_duplicates(
            subset=['data_source', 'block_category', 'block_type', 'block_name', 'block_code', 'ts_code'],
            keep='first');  # 按指定字段去重, 保留第一个

        delete_condition = f"block_category = '{block_category}'"
        mysql_script.df2db_update(delete_condition=delete_condition, block_basic_df=block_info_df,
                                  block_member_df=block_member_df)
        return (len(block_info_df), len(block_member_df))

    # 获取每只股票的附加数据并写入csv
    # 获取个股每日涨跌幅、涨跌、换手率、量比、振幅、流通股、流通市值、市盈率
    def get_day_attach(self, trade_date=""):
        url = "http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/{}/ajax/1/"
        if len(trade_date) == 0: trade_date = time.strftime("%Y%m%d")  # 如果没指定交易日期则用当天日期

        html = self.get_page_bs(url.format(1))
        if html is None: return 0
        page_no_span = html.find("span", class_="page_info")
        if page_no_span is None: return 0
        page_sum = int((page_no_span.string).split('/')[-1])

        page_no = 0
        while True:
            page_no = page_no + 1
            if page_no > page_sum: break
            bs = self.get_page_bs(url.format(page_no))
            if bs is None:
                print("page_no", page_no)
                continue
            table = bs.table
            df = pd.read_html(table.prettify(), attrs={"class":"m-table m-pager-table"}, converters={1:lambda x: str(x) + ".SH" if str(x)[0:1] == '6' else str(x) + ".SZ"})[0]  #converters将股票代码转换为ts_code
            df.drop(df.columns[[0, 3, 6, 10, 14]], axis=1, inplace=True)  #删除不需要的列
            df.columns = ['ts_code', 'name', 'pct_chg', 'price_change', 'turnover_rate', 'qrr', 'amplitude', 'circulate_num', 'circulate_amount', 'per']   #重命名列名:代码,名称,换手(%),流通股,流通市值,市盈率

            if page_no == 1:
                dfall = df
            else:
                dfall = dfall.append(df, ignore_index=True)  # 两个df纵向合并，即追加数据

        dfall.insert(0,'code', dfall['ts_code'].apply(lambda x: str(x)[0:6]))
        dfall.insert(2, 'trade_date', trade_date)
        dfall = dfall[dfall.pct_chg != '--']  # 删除无数据的行

        for i in range(len(dfall)):
            df = dfall.iloc[i:i+1]   #取dataframe对象必须用iloc[i:i+1]写法
            print(type(df))
            ts_code = dfall.iloc[i]['ts_code']  #iloc[i]取出的是一行的元组对象
            filename = config.ths_csv_day_attach + ts_code + ".csv"
            file_util.df2csv_append(df,filename)
        return len(dfall)

    def save_df(self,block_category, block_info, block_member):
        block_info_df = pd.DataFrame(block_info)
        block_info_df['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # block_info_df = block_info_df[['data_source','block_category','block_type','block_name','block_code','member_count','create_time']]
        block_info_df = block_info_df.drop_duplicates(
            subset=['data_source', 'block_category', 'block_type', 'block_name', 'block_code'],
            keep='first');  # 按指定字段去重, 保留第一个
        block_member_df = pd.DataFrame(block_member)
        block_member_df['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # block_member_df = block_member_df[['data_source', 'block_category', 'block_type', 'block_name', 'block_code', 'ts_code','create_time']]
        # block_member_df = block_member_df.drop_duplicates(subset=['data_source', 'block_category', 'block_type', 'block_name', 'block_code', 'ts_code'], keep='first');  # 按指定字段去重, 保留第一个
        print(block_member_df)
        print(block_info_df)
        delete_condition = f"block_category = '{block_category}'"
        mysql_script.df2db_update(delete_condition=delete_condition, block_basic_df=block_info_df,
                                  block_member_df=block_member_df)
        return (len(block_info_df), len(block_member_df))

if __name__ == '__main__':
    ths = ThsHelper()
    #ths.get_block_thshy()
    #ths.get_block_member_thshy('881129')
    #list = ths.get_block_member("ths.thshy",'881129')
    list = ths.get_block_thshy()
    print(list)
    print(len(list))