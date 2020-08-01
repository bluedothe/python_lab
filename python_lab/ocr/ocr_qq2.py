#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/7/27
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

# !/user/bin/env Python3
# -*- coding:utf-8 -*-

"""
file：qq_api.py
create time:2019/4/12 15:14
author:Loong Xu
desc: 调用腾讯OCRapi实现文本识别
"""
import base64, hashlib, json, cv2, random, string, time
from urllib import parse, request
from config import bluedothe
import os
def GetAccessToken(formdata, app_key):
    '''
    获取签名
    :param formdata:请求参数键值对
    :param app_key:应用秘钥
    :return:返回接口调用签名
    '''
    dic = sorted(formdata.items(), key=lambda d: d[0])
    sign = parse.urlencode(dic) + '&app_key=' + app_key
    m = hashlib.md5()
    m.update(sign.encode('utf8'))
    return m.hexdigest().upper()


def RecogniseGeneral(app_id, time_stamp, nonce_str, image, app_key):
    '''
    腾讯OCR通用接口
    :param app_id:应用标识，正整数
    :param time_stamp:请求时间戳（单位秒），正整数
    :param nonce_str: 随机字符串，非空且长度上限32字节
    :param image:原始图片的base64编码
    :return:
    '''
    host = 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_generalocr'
    formdata = {'app_id': app_id, 'time_stamp': time_stamp, 'nonce_str': nonce_str, 'image': image}
    app_key = app_key
    sign = GetAccessToken(formdata=formdata, app_key=app_key)
    formdata['sign'] = sign
    req = request.Request(method='POST', url=host, data=parse.urlencode(formdata).encode('utf8'))
    response = request.urlopen(req)
    if (response.status == 200):
        json_str = response.read().decode()
        print(json_str)
        jobj = json.loads(json_str)
        datas = jobj['data']['item_list']
        recognise = {}
        for obj in datas:
            recognise[obj['itemstring']] = obj
        return recognise


def Recognise(img_path):
    with open(file=img_path, mode='rb') as file:
        base64_data = base64.b64encode(file.read())
    nonce = ''.join(random.sample(string.digits + string.ascii_letters, 32))
    stamp = int(time.time())
    recognise = RecogniseGeneral(app_id=bluedothe.qq_SecretId, time_stamp=stamp, nonce_str=nonce, image=base64_data,
                                 app_key=bluedothe.qq_SecretKey)  # 替换成自己的app_id,app_key
    for k, v in recognise.items():
        print(k, v)
    return recognise

def run():
    file_path = os.getcwd() + "/img_file/pic1.jpg"
    im = cv2.imread(file_path)
    recognise_dic = Recognise(file_path)
    for k, value in recognise_dic.items():
        print(k)
        for v in value['itemcoord']:
            cv2.rectangle(im, (v['x'], v['y']), (v['x'] + v['width'], v['y'] + v['height']), (255, 0, 0), 4)

    cv2.imshow('img', im)
    cv2.waitKey(0)

if __name__ == '__main__':
    file_path = os.getcwd() + "/img_file/pic1.jpg"
    run()