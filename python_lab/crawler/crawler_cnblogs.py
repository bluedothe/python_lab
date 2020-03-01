#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import lxml
import re

'''
    module description
    date: 2020/1/31
    爬取cnblogs的数据
'''

__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

headers = {
 'Accept': 'application/json, text/plain, */*',
 'Accept-Encoding': 'gzip, deflate',
 'Accept-Language': 'zh-CN,zh;q=0.8',
 'Connection': 'keep-alive',
 'Content-Length': '14',
 'Content-Type': 'application/x-www-form-urlencoded',
 'Referer': 'https://www.cnblogs.com',
 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 '
               'Mobile Safari/537.36'}
r = requests.get('https://www.cnblogs.com', headers = headers)
soup = BeautifulSoup(r.text, 'lxml') #lxml为解析器

def test1():
    print(soup.prettify())
    print(soup.title, soup.title.string)  # 获取指定标签，获取指定标签里面的内容
    print(soup('title'), soup('title')[0].string)  # 获取指定标签也可以写成这样
    print(soup.meta.get('charset'))  # 获取指定标签的属性
    print(soup.meta['charset'])  # 获取指定标签的属性也可写成这样
    print(soup.meta)  # 获取第一个标签（多个只取第一个）
    print(soup.find('meta'))  # 获取第一个标签，结果和上面一样
    print(soup.find('meta', attrs={'name': 'viewport'}))  # 获取第一个标签，根据属性过滤获取
    print(soup.find_all('meta', attrs={'charset': True}))  # 获取所有标签的列表，同时根据是否含有属性charset过滤获取

def test_tag():
    print(soup.title)

def test_find():
    pass

def test_findall():
    pass

def test_select():
    pass

if __name__ == '__main__':
    test1()