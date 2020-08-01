#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/7/27
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import os
import requests

def get_text(img_path):
    print("")
    img = img_path  # 图片路径
    files = {"pic_path": open(img, "rb")}  # files # 类似data数据
    url = "http://pic.sogou.com/pic/upload_pic.jsp"  # post的url
    keywords = requests.post(url, files=files).text  # requests 提交图片
    url = "http://pic.sogou.com/pic/ocr/ocrOnline.jsp?query=" + keywords  # keywords就是图片url此方式为get请求
    ocrResult = requests.get(url).json()  # 直接转换为json格式

    contents = ocrResult['result']  # 类似字典 把result的value值取出来 是一个list然后里面很多json就是识别的文字
    text = ""
    for content in contents:  # 遍历所有结果
        text += (content['content'].strip() + '\n')  # strip去除空格 他返回的结果自带一个换行
    return text

def get_text2():
    multiple_files = {'pic': ('1111111.jpg', open(r'QQ截图20180905172943.jpg', 'rb'), 'image/jpg')}
    resp = requests.post(r'http://ocr.shouji.sogou.com/v2/ocr/json', files=multiple_files)
    str_json = resp.json()


if __name__ == '__main__':
    file_path = os.getcwd() + "/img_file/pic1.jpg"
    text = get_text(file_path)
    print(text)