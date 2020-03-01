#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2019/11/2
    模拟浏览器请求
'''

import requests
from pprint import pprint

__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2019"

'simulate get method'
def test1():
    url ='http://httpbin.org/get'
    args = {'username':'bigcard','age':'20','desc':'测试'}
    rsp = requests.get(url, params=args)
    print(rsp.status_code)
    pprint(rsp.content)
    pprint(rsp.text)
    pprint(rsp.json())

'simulate post method'
def test2():
    url ='http://httpbin.org/post'
    datas = {'username':'bigcard','age':'20','desc':'测试'}
    rsp = requests.post(url, data=datas)
    print("status_code",rsp.status_code,sep=':')
    print("content",rsp.content)
    print("text",rsp.text)
    print("json",rsp.json())
    print("encoding",rsp.encoding,sep=':')
    print("apparent_encoding",rsp.apparent_encoding,sep=':')

'simulate headers info'
def test3():
    url ='http://httpbin.org/get'
    args = {'username':'bigcard','age':'20','desc':'测试'}
    headers = {'User-Agent':'Firefox6.6','Referer':'http://www.baidu.com'}
    rsp = requests.get(url, params=args, headers = headers)
    print(rsp.status_code)
    pprint(rsp.content)
    pprint(rsp.text)
    pprint(rsp.json())
    #print(rsp.headers['User-Agent'])  #没有取得值
    #type(rsp.headers)  #没有取得值

'simulate cookie1'
def test4():
    url ='http://127.0.0.1:5000/info'
    args = {'username':'bigcard','age':'20','desc':'测试'}
    headers = {'User-Agent':'Firefox6.6','Referer':'http://www.baidu.com'}
    cookie = {'login':'yes'}
    rsp = requests.get(url, params=args, headers = headers, cookies = cookie)
    print(rsp.status_code)
    pprint(rsp.content)
    pprint(rsp.text)

'simulate cookie2'
def test5():
    url ='http://127.0.0.1:5000/info'
    args = {'username':'bigcard','age':'20','desc':'测试'}
    headers = {'User-Agent':'Firefox6.6','Referer':'http://www.baidu.com'}
    jar = requests.cookies.RequestsCookieJar()
    jar.set('login','yes')
    rsp = requests.get(url, params=args, headers = headers, cookies = jar)
    print(rsp.status_code)
    pprint(rsp.content)
    pprint(rsp.text)


if __name__ == '__main__':
    pprint(test2.__name__)
    test1()