#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/7/25
    解决利用selenium爬取同花顺翻页只能取5页的问题
    在selenium只生成一个webdriver对象的情况下仍然会被同花顺限制在五页之类的访问次数，可是如果我每访问一次都重建一个新的webdriver对象则可以避免这种情况
    参考资料：https://blog.csdn.net/CY19980216/article/details/86647597?utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~all~first_rank_v2~rank_v25-7-86647597.nonecase
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import os
import re
import json
import time
import numpy
import pandas
import random
import requests

from bs4 import BeautifulSoup
from selenium import webdriver

"""
	作者：囚生CY
	平台：CSDN
	时间：2019/01/27
	转载请注明原作者
	创作不易，仅供分享
"""


class StraightFlush():

    def __init__(self,
                 #userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0",
                 userAgent="Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
                 cookie="v=AigMPjtB4I7PKMwKRvAplY1u-Rc7UYxbbrVg3-JZdKOWPcYFimFc677FMG4x; log=; \
				Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1548080158; \
				Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1548080196; \
				Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1548080175; \
				Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1548080196; \
				Hm_lvt_f79b64788a4e377c608617fba4c736e2=1548080175; \
				Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1548080196; \
				vvvv=1"
                 ):
        """ 定义构造函数传入可变参数 """
        self.userAgent = userAgent
        self.cookie = cookie

        """ 定义常用的固定参数 """
        self.date = time.strftime("%Y-%m-%d")  # 获取类初始化的时间
        self.workSpace = os.getcwd()  # 获取工作目录
        self.errorLog = "Error_Log.txt"
        self.mainURL = "http://www.10jqka.com.cn/"
        self.dataURL = "http://data.10jqka.com.cn/"

        self.orderSuffix = "field/code/order/asc/page/{}/ajax/1/"

        self.stockFlowURL = self.dataURL + "funds/ggzjl/"
        self.conceptFlowURL = self.dataURL + "funds/gnzjl/"
        self.industryFlowURL = self.dataURL + "funds/hyzjl/"

        self.stockTableURL = self.stockFlowURL + self.orderSuffix
        self.conceptTableURL = self.conceptFlowURL + self.orderSuffix
        self.industryTableURL = self.industryFlowURL + self.orderSuffix
        self.headers = {
            "User-Agent": self.userAgent,
            "Cookie": self.cookie,
        }
        self.session = requests.Session()
        self.session.headers = self.headers

        """ 初始化操作 """
        self.session.get(self.mainURL)

    def parse_money_flow_stock(self, ):  # 获取A股个股资金流动
        self.session.get(self.dataURL)
        html = self.session.get(self.stockFlowURL).text
        soup = BeautifulSoup(html, "lxml")
        spans = soup.find_all("span")
        ths = soup.find_all("th")
        """ 将<th>标签中的string作为DataFrame的header """
        flag = False
        with open(r"{}\{}\money_flow_stock_{}.csv".format(self.workSpace, "file_down/ths", self.date), "a") as f:
            for th in ths:
                aLabel = th.find_all("a")
                string = aLabel[0].string if len(aLabel) else th.string
                if flag:
                    f.write(",{}".format(string))
                else:
                    flag = True
                    f.write(str(string))
            f.write("\n")
        """ 遍历<span>标签获取总页数 """
        for span in spans:
            string = str(span.string)
            if len(string) > 2 and string[:2] == "1/":
                page = int(string[2:])
                break
        """ 获取资金流动信息 """
        for i in range(1, page + 1):
            b = webdriver.Chrome()
            b.get(self.stockTableURL.format(i))
            html = b.page_source
            soup = BeautifulSoup(html, "lxml")
            trs = soup.find_all("tr")
            with open(r"{}\{}\money_flow_stock_{}.csv".format(self.workSpace, "file_down/ths", self.date), "a") as f:
                for tr in trs[1:]:  # 跳过第一个<tr>标签是因为第一行是表头
                    flag = False
                    tds = tr.find_all("td")
                    for td in tds:
                        string = str(td.string)
                        string = string.replace(" ", "").replace("\t", "").replace("\n", "")
                        if flag:
                            f.write(",{}".format(string))
                        else:
                            flag = True
                            f.write(string)
                    f.write("\n")
            b.quit()
        return True

    def parse_money_flow_concept(self, ):  # 获取A股概念板块资金流动
        self.session.get(self.dataURL)
        html = self.session.get(self.conceptFlowURL).text
        soup = BeautifulSoup(html, "lxml")
        spans = soup.find_all("span")
        ths = soup.find_all("th")
        """ 将<th>标签中的string作为DataFrame的header """
        flag = False
        with open(r"{}\{}\money_flow_concept_{}.csv".format(self.workSpace, "file_down/ths", self.date), "a") as f:
            for th in ths:
                aLabel = th.find_all("a")
                if len(aLabel):  # 概念板块与行业板块读取表头的代码如此笨拙因为与个股的方法在这里竟然只能拿到None,而且两者格式一模一样,让我很奇怪
                    tag = str(aLabel[0])
                    index1 = tag.find(">")
                    index2 = tag.find("<", index1)
                    string = tag[index1 + 1:index2]
                else:
                    string = th.string
                if flag:
                    f.write(",{}".format(string))
                else:
                    flag = True
                    f.write(str(string))
            f.write("\n")
        """ 遍历<span>标签获取总页数 """
        for span in spans:
            string = str(span.string)
            if len(string) > 2 and string[:2] == "1/":
                page = int(string[2:])
                break
        """ 获取资金流动信息 """
        for i in range(1, page + 1):
            b = webdriver.Chrome()
            b.get(self.conceptTableURL.format(i))
            html = b.page_source
            soup = BeautifulSoup(html, "lxml")
            trs = soup.find_all("tr")
            with open(r"{}\{}\money_flow_concept_{}.csv".format(self.workSpace, "file_down/ths", self.date), "a") as f:
                for tr in trs[1:]:  # 跳过第一个<tr>标签是因为第一行是表头
                    flag = False
                    tds = tr.find_all("td")
                    for td in tds:
                        string = str(td.string)
                        string = string.replace(" ", "").replace("\t", "").replace("\n", "")
                        if flag:
                            f.write(",{}".format(string))
                        else:
                            flag = True
                            f.write(string)
                    f.write("\n")
            b.quit()
        return True

    def parse_money_flow_industry(self, ):  # 获取A股概念板块资金流动
        self.session.get(self.dataURL)
        html = self.session.get(self.industryFlowURL).text
        soup = BeautifulSoup(html, "lxml")
        spans = soup.find_all("span")
        ths = soup.find_all("th")
        """ 将<th>标签中的string作为DataFrame的header """
        flag = False
        with open(r"{}\{}\money_flow_industry_{}.csv".format(self.workSpace, "file_down/ths", self.date), "a") as f:
            for th in ths:
                aLabel = th.find_all("a")
                if len(aLabel):  # 概念板块与行业板块读取表头的代码如此笨拙因为与个股的方法在这里竟然只能拿到None,而且两者格式一模一样,让我很奇怪
                    tag = str(aLabel[0])
                    index1 = tag.find(">")
                    index2 = tag.find("<", index1)
                    string = tag[index1 + 1:index2]
                else:
                    string = th.string
                if flag:
                    f.write(",{}".format(string))
                else:
                    flag = True
                    f.write(str(string))
            f.write("\n")
        """ 遍历<span>标签获取总页数 """
        for span in spans:
            string = str(span.string)
            if len(string) > 2 and string[:2] == "1/":
                page = int(string[2:])
                break
        """ 获取资金流动信息 """
        for i in range(1, page + 1):
            b = webdriver.Chrome()
            b.get(self.industryTableURL.format(i))
            html = b.page_source
            soup = BeautifulSoup(html, "lxml")
            trs = soup.find_all("tr")
            with open(r"{}\{}\money_flow_industry_{}.csv".format(self.workSpace, "file_down/ths", self.date), "a") as f:
                for tr in trs[1:]:  # 跳过第一个<tr>标签是因为第一行是表头
                    flag = False
                    tds = tr.find_all("td")
                    for td in tds:
                        string = str(td.string)
                        string = string.replace(" ", "").replace("\t", "").replace("\n", "")
                        if flag:
                            f.write(",{}".format(string))
                        else:
                            flag = True
                            f.write(string)
                    f.write("\n")
            b.quit()
        return True


if __name__ == "__main__":
    print("测试开始...")
    sf = StraightFlush()
    sf.parse_money_flow_stock()
    sf.parse_money_flow_concept()
    sf.parse_money_flow_industry()