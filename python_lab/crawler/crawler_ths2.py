#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/7/25
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import requests
from bs4 import BeautifulSoup
import re
import time
import json
import pprint
import jsonpath
from fake_useragent import UserAgent  #代理


def crawler_template():
    url = ""
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '14',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://bj.58.com',
        'User-Agent': str(UserAgent(verify_ssl=False).random)
        # 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
        #              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 '
        #              'Mobile Safari/537.36'
    }
    params = {"name": "disease_h5", "callback": "", "_": "%d" % int(time.time() * 1000)}
    wb_data = requests.get(url, headers=headers, params=params)
    # print(wb_data.text)
    # soup = BeautifulSoup(resp.content.decode("gbk"), "lxml")
    soup = BeautifulSoup(wb_data.text, 'lxml')
    print(soup.prettify())


def get_gnzjl():
    REQUEST_HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    REQUEST_HEADER = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36'}
    headers = {'User-Agent': str(UserAgent(verify_ssl=False).random)}
    page_number = 1
    url = "http://data.10jqka.com.cn/funds/gnzjl/field/tradezdf/order/desc/page/%s/ajax/1/free/1/"
    params = {"name": "disease_h5", "callback": "", "_": "%d"%int(time.time()*1000)}
    resp = requests.get(url % page_number,headers=headers)
    #soup = BeautifulSoup(resp.content.decode("gbk"), "lxml")
    soup = BeautifulSoup(resp.text, "lxml")
    table = soup.select('.J-ajax-table')[0]
    tbody = table.select('tbody tr')
    print(tbody)

if __name__ == '__main__':
    get_gnzjl()