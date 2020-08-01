#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/7/29
    每次获取分页数据都用新的header，可以解决5页限制
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"


import requests
from bs4 import BeautifulSoup
import re
import sys
import time
import random
import json
import pprint
import jsonpath
from fake_useragent import UserAgent  #代理
import lxml.html

global cur_page, omi_flag, page_list
max_page = 20
min_page = 10
cur_page = min_page
omi_flag = 0         #用于标识，是否使用 url_omi() 函数
page_list = []     #第一次爬取的 html 缺失的页面 的url 列表,先进先出的列表
URL_START = "http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/"
PARAMS = "/ajax/1/"
headers_list = [{
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'log=; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1533992361,1533998469,1533998895,1533998953; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1533998953; user=MDrAz9H9akQ6Ok5vbmU6NTAwOjQ2OTU0MjIzNDo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxLDQwOzIsMSw0MDszLDEsNDA7NSwxLDQwOzgsMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDEsNDA6Ojo6NDU5NTQyMjM0OjE1MzM5OTkwNzU6OjoxNTMzOTk5MDYwOjg2NDAwOjA6MTZmOGFjOTgwMGNhMjFjZjRkMWZlMjk0NDQ4M2FhNDFkOmRlZmF1bHRfMjox; userid=459542234; u_name=%C0%CF%D1%FDjD; escapename=%25u8001%25u5996jD; ticket=7c92fb758f81dfa4399d0983f7ee5e53; v=Ajz6VIblS6HlDX_9PqmhBV0QDdH4NeBfYtn0Ixa9SCcK4daNPkWw77LpxLZl',
        'hexin-v': 'AiDRI3i0b1qEZNNemO_FOZlE8SXqKQQBpg9Y4Jox7pbOH8oZQjnUg_YdKIHp',
        'Host': 'q.10jqka.com.cn',
        'Referer': 'http://q.10jqka.com.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }, {'Accept': 'text/html, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'user=MDq62tH9NUU6Ok5vbmU6NTAwOjQ2OTU0MjA4MDo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxLDQwOzIsMSw0MDszLDEsNDA7NSwxLDQwOzgsMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDEsNDA6Ojo6NDU5NTQyMDgwOjE1MzM5OTg4OTc6OjoxNTMzOTk4ODgwOjg2NDAwOjA6MTEwOTNhMzBkNTAxMWFlOTg0OWM1MzVjODA2NjQyMThmOmRlZmF1bHRfMjox; userid=459542080; u_name=%BA%DA%D1%FD5E; escapename=%25u9ed1%25u59965E; ticket=658289e5730da881ef99b521b65da6af; log=; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1533992361,1533998469,1533998895,1533998953; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1533998953; v=AibgksC3Qd-feBV7t0kbK7PCd5e-B2rBPEueJRDPEskkk8xLeJe60Qzb7jDj',
        'hexin-v': 'AiDRI3i0b1qEZNNemO_FOZlE8SXqKQQBpg9Y4Jox7pbOH8oZQjnUg_YdKIHp',
        'Host': 'q.10jqka.com.cn',
        'Referer': 'http://q.10jqka.com.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        },
        {'Accept': 'text/html, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate, sdch',
         'Accept-Language': 'zh-CN,zh;q=0.8', 'Connection': 'keep-alive',
         'Cookie': 'user=MDq62sm9wM%2FR%2FVk6Ok5vbmU6NTAwOjQ2OTU0MTY4MTo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxLDQwOzIsMSw0MDszLDEsNDA7NSwxLDQwOzgsMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDEsNDA6Ojo6NDU5NTQxNjgxOjE1MzM5OTg0NjI6OjoxNTMzOTk4NDYwOjg2NDAwOjA6MTAwNjE5YWExNjc2NDQ2MGE3ZGYxYjgxNDZlNzY3ODIwOmRlZmF1bHRfMjox; userid=459541681; u_name=%BA%DA%C9%BD%C0%CF%D1%FDY; escapename=%25u9ed1%25u5c71%25u8001%25u5996Y; ticket=4def626a5a60cc1d998231d7730d2947; log=; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1533992361,1533998469; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1533998496; v=AvYwAjBHsS9PCEXLZexL20PSRyfuFzpQjFtutWDf4ll0o5zbyKeKYVzrvsAz',
         'hexin-v': 'AiDRI3i0b1qEZNNemO_FOZlE8SXqKQQBpg9Y4Jox7pbOH8oZQjnUg_YdKIHp', 'Host': 'q.10jqka.com.cn',
         'Referer': 'http://q.10jqka.com.cn/',
         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
         'X-Requested-With': 'XMLHttpRequest'},
        {'Accept': 'text/html, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate, sdch',
         'Accept-Language': 'zh-CN,zh;q=0.8', 'Connection': 'keep-alive',
         'Cookie': 'Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1533992361; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1533992361; user=MDq62sm9SnpsOjpOb25lOjUwMDo0Njk1NDE0MTM6NywxMTExMTExMTExMSw0MDs0NCwxMSw0MDs2LDEsNDA7NSwxLDQwOzEsMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOjo6OjQ1OTU0MTQxMzoxNTMzOTk4MjA5Ojo6MTUzMzk5ODE2MDo4NjQwMDowOjFlYTE2YTBjYTU4MGNmYmJlZWJmZWExODQ3ODRjOTAxNDpkZWZhdWx0XzI6MQ%3D%3D; userid=459541413; u_name=%BA%DA%C9%BDJzl; escapename=%25u9ed1%25u5c71Jzl; ticket=b909a4542156f3781a86b8aaefce3007; v=ApheKMKxdxX9FluRdtjNUdGcac08gfwLXuXQj9KJ5FOGbTKxepHMm671oBoh',
         'hexin-v': 'AiDRI3i0b1qEZNNemO_FOZlE8SXqKQQBpg9Y4Jox7pbOH8oZQjnUg_YdKIHp', 'Host': 'q.10jqka.com.cn',
         'Referer': 'http://q.10jqka.com.cn/',
         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
         'X-Requested-With': 'XMLHttpRequest'},

    ]


def get_page_data(url):
    #url = "http://q.10jqka.com.cn//index/index/board/all/field/zdf/order/desc/page/6/ajax/1/"
    time.sleep(random.random() * 5)  # 设置延时
    headers = random.choice(headers_list)
    wb_data = requests.get(url, headers=headers)
    #print(wb_data.text)
    return wb_data.text

#使用yield函数，每次只返回一个url
def url_yield():
    """
    :func 用于生成url
    :yield items
    """
    global cur_page, omi_flag, page_list
    for i in range(min_page, max_page + 1):
        cur_page = i+2  # 页面追踪
        omi_flag += 1  # 每次加1
        print('omi_flag 是：', omi_flag)
        url = "{}{}{}".format(URL_START, cur_page, PARAMS)
        yield url

#将抓取失败的url，再次进行抓取
def url_omi():
    global cur_page, omi_flag, page_list
    print("开始补漏")
    length_pl = len(page_list)
    if length_pl != 0:  # 判断是否为空
        for i in range(length_pl):
            cur_page = page_list.pop(0)  # 构造一个动态列表, 弹出第一个元素
            url = "{}{}{}".format(URL_START, cur_page, PARAMS)
            yield url

def get_all_page_data():
    global cur_page, omi_flag, page_list
    sys.setrecursionlimit(5000)  #设置递归调用深度
    count = 0
    while True:
        if omi_flag < max_page:
            url_list = url_yield()  # 获取url
        else:
            break
            url_list = url_omi()
            if len(page_list) == 0:
                break
        print("执行到了获取模块")

        for url in url_list:   #迭代器结果必须这样取值，不能直接使用
            html = get_page_data(url)
            # 打印提示信息

            print('URL is:', url)
            items = {}  # 建立一个空字典，用于信息存储
            try:
                soup = BeautifulSoup(html, 'lxml')
                record_num = 0
                for tr in soup.find('tbody').find_all('tr'):
                    td_list = tr.find_all('td')
                    items['代码'] = td_list[1].string
                    items['名称'] = td_list[2].string
                    items['现价'] = td_list[3].string
                    items['涨跌幅'] = td_list[4].string
                    record_num += 1
                print('记录数：', record_num)
                ###print(items)
                ###print("保存成功")
                # 如果保存成功，则继续使用代理
                # print("解析成功")
                # yield items          #将结果返回
            except:
                print("解析失败")
                # print(html)
                if not cur_page in page_list:
                    page_list.append(cur_page)
                else:
                    count += 1

        if count == 2:
            break
    # soup = BeautifulSoup(resp.content.decode("gbk"), "lxml")
    #soup = BeautifulSoup(wb_data.text, 'lxml')
    #print(soup.prettify())

if __name__ == '__main__':
    get_all_page_data()
