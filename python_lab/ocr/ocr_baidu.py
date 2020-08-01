#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/7/27
    参考资料：https://blog.csdn.net/tang_xiaotang/article/details/91516654?utm_medium=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import urllib, sys
import requests
import ssl
from config import bluedothe

def get_access_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}'
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    wb_data = requests.get(url.format(bluedothe.baidu_Access_Key, bluedothe.baidu_Secret_Key), headers=headers)
    print(wb_data.text)


if __name__ == '__main__':
    get_access_token()