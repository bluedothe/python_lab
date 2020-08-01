#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/7/25
    参考资料：https://blog.csdn.net/eryk86/article/details/104338991
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import os
import time

import requests
from bs4 import BeautifulSoup
from taskflow import engines
from taskflow.patterns import linear_flow
from taskflow.task import Task

REQUEST_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}


class MoneyFlowDownload(Task):
    """
    下载资金流数据
    数据源地址：http://data.10jqka.com.cn/funds/gnzjl/
    """
    BASE_URl = {
        "concept": 'http://data.10jqka.com.cn/funds/gnzjl/field/tradezdf/order/desc/page/%s/ajax/1/free/1/',
    }

    def execute(self, bizdate, *args, **kwargs):

        for name, base_url in self.BASE_URl.items():
            # 爬取数据的存储路径
            dt_path = os.getcwd() + '/file_down/ths/%s_%s.csv' % (bizdate, name)

            with open(dt_path, "a+") as f:
                # 记录数据文件的当前位置
                pos = f.tell()
                f.seek(0)
                lines = f.readlines()
                # 读取文件中的全部数据并将第一列存储下来作为去重依据，防止爬虫意外中断后重启程序时，重复写入相同
                crawled_list = list(map(lambda line: line.split(",")[0], lines))
                f.seek(pos)
                # 循环500次，从第一页开始爬取数据，当页面没有数据时终端退出循环
                for i in range(1, 500):
                    print("start crawl %s, %s" % (name, base_url % i))
                    web_source = requests.get(base_url % i, headers=REQUEST_HEADER)
                    soup = BeautifulSoup(web_source.content.decode("gbk"), 'lxml')
                    table = soup.select('.J-ajax-table')[0]
                    tbody = table.select('tbody tr')
                    # 当tbody为空时，则说明当前页已经没有数据了，此时终止循环
                    if len(tbody) == 0:
                        break
                    for tr in tbody:
                        fields = tr.select('td')
                        # 将每行记录第一列去掉，第一列为序号，没有存储必要
                        record = [field.text.strip() for field in fields[1:]]
                        # 如果记录还没有写入文件中，则执行写入操作，否则跳过这行写入
                        if record[0] not in crawled_list:
                            f.writelines([','.join(record) + '\n'])
                    # 同花顺网站有反爬虫的机制，爬取速度过快很可能被封
                    time.sleep(1)


if __name__ == '__main__':
    bizdate = '20200214'
    tasks = [
        MoneyFlowDownload('moneyflow data download')
    ]
    flow = linear_flow.Flow('ths data download').add(*tasks)
    e = engines.load(flow, store={'bizdate': bizdate})
    e.run()
