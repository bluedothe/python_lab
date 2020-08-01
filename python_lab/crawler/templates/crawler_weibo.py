#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/7/26
    爬取新浪微博内容
    参考资料：https://blog.csdn.net/qq_36936730/article/details/104750041?utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~all~first_rank_v2~rank_v25-5-104750041.nonecase
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

def get_weibo():
    type = "uid"
    value = "1216903164"
    containerid = "1076031216903164"
    since_id = "4529633788429523"
    url = f"https://m.weibo.cn/api/container/getIndex?type={type}&value={value}&containerid={containerid}&since_id={since_id}"
    headers = {'User-Agent': str(UserAgent(verify_ssl=False).random)}
    params = {"name": "disease_h5", "callback": "", "_": "%d" % int(time.time() * 1000)}
    wb_data = requests.get(url, headers=headers)  #, params=params
    print(wb_data.content.decode("utf-8"))
    json_data = json.dumps(wb_data.json(), ensure_ascii=False)
    print(json_data)
    #soup = BeautifulSoup(wb_data.content.decode("gbk"), "lxml")
    #soup = BeautifulSoup(wb_data.text, 'lxml')
    #print(soup.prettify())

if __name__ == '__main__':
    get_weibo()