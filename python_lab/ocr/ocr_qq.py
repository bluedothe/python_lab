#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/7/27
    腾讯开放平台：https://open.tencent.com/
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import os
import base64
import hashlib
import time
import uuid
from urllib import parse

import requests

from config import bluedothe

APP_ID = bluedothe.qq_SecretId
APP_KEY = bluedothe.qq_SecretKey
OCR = 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_generalocr'

def __get_sign(params):
    # 参数升序
    param_list = list(params.keys())
    param_list.sort()
    param_str = ''
    for param in param_list:
        # 空值不参与签名
        value = params[param]
        if value:
            if param_str:
                param_str += '&'
            #    对 value进行编码
            parse_quote = list(parse.quote_plus(str(value)))
            i = 0
            for a in parse_quote:
                if a == '%':
                    parse_quote[i + 1] = str(parse_quote[i + 1]).upper()
                    parse_quote[i + 2] = str(parse_quote[i + 2]).upper()
                i += 1
            param_str += str(param) + '=' + (''.join(parse_quote))

    key_ = ("%s&app_key=%s" % (param_str, APP_KEY)).encode(encoding='utf-8')
    return hashlib.md5(key_).hexdigest().upper()


def getWork(image_path):
    params = {
        'app_id': APP_ID,
        'time_stamp': int(time.time()),
        'nonce_str': str(uuid.uuid4()).replace('-', '')[0:31]
    }
    with open(image_path, 'rb') as f:
        params['image'] = str(base64.b64encode(f.read()), 'utf-8').replace(r'\r\n', '')
    params['sign'] = __get_sign(params)

    result = requests.post(OCR, headers={"Content-Type": "application/x-www-form-urlencoded"}, data=params).json()
    print(result)
    if result['ret'] == 0:
        item_list = []
        for item in result['data']['item_list']:
            print(item['itemstring'])
            item_list.append(item['itemstring'])
        return item_list
    else:
        print('系统忙：', result['msg'])
        return result['msg']


if __name__ == '__main__':
    file_path = os.getcwd() + "/img_file/pic1.jpg"
    getWork(file_path)

