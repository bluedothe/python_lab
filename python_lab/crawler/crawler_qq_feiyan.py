#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import time
import json
import pprint
import jsonpath

'''
    module description
    date: 2020/2/1
    从腾讯网站抓取肺炎实时数据
    教程来源：https://blog.csdn.net/msssssss/article/details/104109503
    目标网址：https://news.qq.com/zt2020/page/feiyan.htm?from=timeline&isappinstalled=0
    深入分析，我们就得到了url地址、请求方法、参数、应答格式等信息。
    查询参数中，callback是回调函数名，我们可以尝试置空，_应该是以毫秒为单位的当前时间戳。有了这些信息，分分钟就可以抓到数据了。
'''

__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

def test():
    url = "https://view.inews.qq.com/g2/getOnsInfo"
    params = {"name": "disease_h5", "callback": "", "_": "%d"%int(time.time()*1000)}
    req = requests.get(url,params=params)
    #soup = BeautifulSoup.get(req.text, "lxml")
    json_dict = json.loads(req.json()['data'])
    print(len(json_dict),type(json_dict))
    json_str = json.dumps(json_dict,ensure_ascii=False)  #dumps方法将字典类型转为字符串类型，dumps方法会把中文转为unicode码,ensure_ascii=False可以禁止转码
    print(len(json_str), type(json_str))
    print(json_str)
    print(json_dict)
    for item in json_dict:
        print()
        print(item)
    json_list = jsonpath.jsonpath(json_dict,"$..name")
    print()
    for item in json_list:
        print(item)
    """print()
    for item in result['chinaTotal']:
        print(item)
    print()
    for item in result['lastUpdateTime']:
         print(item)
    print()
    for item in result['areaTree']:
        print(item['name'],item['total'])
    print()
    for item in result['chinaDayList']:
        print(item)"""



if __name__ == '__main__':
    test()