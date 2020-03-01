#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2019/11/4
    爬取图片网站http://www.umei.cc
'''

import requests
import urllib.request
import re
import os

__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2019"

'use requests lib'
def test1():
    url= 'http://e.hiphotos.baidu.com/image/pic/item/4610b912c8fcc3cef70d70409845d688d53f20f7.jpg'
    rsq = requests.get(url, stream = True)
    if rsq.status_code == 200:
        result = rsq.content
        with open(os.getcwd() + "/pic_down/" + 'umei/pic001.jpg', 'wb') as f:
            f.write(result)
        with open(os.getcwd() + "/pic_down/" + 'umei/pic002.jpg', 'wb') as f:
            for chunk in rsq.iter_content(1024):
                f.write(chunk)

'use urllib lib'
def test2():
    url= 'http://e.hiphotos.baidu.com/image/pic/item/4610b912c8fcc3cef70d70409845d688d53f20f7.jpg'
    urllib.request.urlretrieve(url, 'result/pic003.jpg')

def extra_umei():
    url = 'http://www.umei.cc/bizhitupian/huyanbizhi/'
    rsp = requests.get(url)
    if rsp.status_code == 200:
        html = rsp.text
        expression = r'<img src="(.*?)" width="180" '
        results = re.findall(expression, html)
        print(len(results))
        for i, result in enumerate(results):
            picname = r'pics/00{}.jpg'.format(i+1)    #必须提前创建子目录
            urllib.request.urlretrieve(result, picname)


if __name__ == '__main__':
    extra_umei()