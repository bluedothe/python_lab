#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from urllib import request, parse
from pprint import pprint
from http import cookiejar

'''
    module description
    date: 2020/2/1
    模拟北京总工会12351APP操作
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"
username = "142126197103270016"
password = "Hzy740908"
headers = {
'Accept': 'application/json, text/plain, */*',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; HUAWEI NXT-AL10 Build/HUAWEINXT-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.132 Mobile Safari/537.36',
'X-Requested-With': 'com.longser.bj12351app',
'Host': 'www.bjzgh12351.org',
'Connection': 'keep-alive',
#'Cookie': 'JSESSIONID=0001CFBQmgCRL4nbpQ_-3UdpBsr:1clgfl40r'
}
url = "http://www.bjzgh12351.org"

def test_urllib():
    req = request.Request(url, headers=headers)
    rsp = request.urlopen(req)
    result = rsp.read().decode()  # read and decode
    pprint(rsp.getcode())
    pprint(dict(rsp.info()))
    pprint(result)

def test():
    req = requests(url, "lxml",headers = headers)
    print(req.text)

if __name__ == '__main__':
    #test()
    test_urllib()