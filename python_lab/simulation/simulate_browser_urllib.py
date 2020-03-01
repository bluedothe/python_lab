#!/usr/bin/python3
# -*- coding: utf-8 -*-

from urllib import request, parse
from pprint import pprint
from http import cookiejar
import flask


'''
    module description
    date: 2019/10/30
    模拟浏览器请求
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2019"

def test1():
    url = "http://127.0.0.1:5000/reg"
    rsp = request.urlopen(url)
    result = rsp.read().decode()    #read and decode
    print(rsp.getcode())
    pprint(dict(rsp.info()))
    pprint(result)

'simulate get method'
def test2():
    url = "http://127.0.0.1:5000/get_data"
    args = "?username=bigcard&email=begcard@sina.com&edu=3"
    args2 = parse.quote(args)   # ? and & be encoded too
    print(args2)
    rsp = request.urlopen(url + args)
    result = rsp.read().decode()
    print(rsp.getcode())
    pprint(dict(rsp.info()))
    pprint(result)

'simulate get method'
def test3():
    url = "http://127.0.0.1:5000/get_data"
    params = {'username':'小河', 'email':'bluedothe@sina.com', 'edu':'2'}
    params2 = parse.urlencode(params)
    print(params2)
    #rsp = request.urlopen(url + '?' + params2)
    rsp = request.urlopen(f'{url}?{params2}')
    result = rsp.read().decode()
    print(rsp.getcode())
    pprint(dict(rsp.info()))
    pprint(result)

'simulate post method，set header info'
def test4():
    url = "http://127.0.0.1:5000/post_data"
    params = {'username': '小河', 'email': 'bluedothe@sina.com', 'edu': '2'}
    params2 = parse.urlencode(params).encode('utf-8')
    print(params2)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': '127.0.0.1:5000',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
    #req = request.Request(url, params2, method="POST")
    #req = request.Request(url, data=params2)  #default is post
    req = request.Request(url, data=params2, headers=headers)
    rsp = request.urlopen(req)
    result = rsp.read().decode()
    print(rsp.getcode())
    pprint(dict(rsp.info()))
    pprint(result)

'use #http://httpbin.org'
def test5():
    url = 'http://httpbin.org'
    rsp = request.urlopen(f'{url}/get')
    result = rsp.read().decode()
    print(rsp.getcode())
    pprint(dict(rsp.info()))
    pprint(result)

'simulate head info'
'''
headers = {
 'Accept': 'application/json, text/plain, */*',
 'Accept-Encoding': 'gzip, deflate',
 'Accept-Language': 'zh-CN,zh;q=0.8',
 'Connection': 'keep-alive',
 'Content-Length': '14',
 'Content-Type': 'application/x-www-form-urlencoded',
 'Referer': 'http://10.1.2.151/',
 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 '
               'Mobile Safari/537.36'}
'''
def test6():
    url = 'http://httpbin.org/get'
    req = request.Request(url, method="GET")
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36')
    req.add_header('Referer','http://www.sina.com')
    rsp = request.urlopen(req)
    result = rsp.read().decode()
    print(rsp.getcode())
    pprint(dict(rsp.info()))
    pprint(result)

'simulate cookie'
'''
Response.set_cookie(
    key,            //键
    value='',       //值
    max_age=None,   //秒为单位的cookie寿命，None表示http-only
    expires=None,   //失效时间，datetime对象或unix时间戳
    path='/',       //cookie的有效路径
    domain=None,    //cookie的有效域
    secure=None, 
    httponly=False)
'''
def test7():
    url = 'http://127.0.0.1:5000/info'
    jar = cookiejar.CookieJar()
    openner = request.build_opener(request.HTTPCookieProcessor(jar))
    rsp = openner.open(url)
    result = rsp.read().decode()
    print(rsp.getcode())
    pprint(dict(rsp.info()))
    pprint(result)
    pprint(jar)

    rsp = openner.open(url)
    result = rsp.read().decode()
    print(rsp.getcode())
    pprint(dict(rsp.info()))
    pprint(result)
    pprint(jar)

if __name__ == '__main__':
    #pprint(sys.path)  #打印系统搜索第三方库的路径
    #print(flask.__file__)  #查找模块的路径
    test7()
