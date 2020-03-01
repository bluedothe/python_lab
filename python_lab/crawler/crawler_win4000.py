#!/usr/bin/python3
# -*- coding: utf-8 -*-

from requests_html import HTMLSession
import requests
import time
import os

'''
    module description
    date: 2020/2/9
    案例地址：https://blog.csdn.net/weixin_34232617/article/details/88877158
    目标网址：http://www.win4000.com/
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

session = HTMLSession()

# 解析图片列表
def get_girl_list():
    # 返回一个 response 对象
    response = session.get('http://www.win4000.com/zt/xinggan.html')  # 单位秒数

    content = response.html.find('div.Left_bar', first=True)

    li_list = content.find('li')

    for li in li_list:
        url = li.find('a', first=True).attrs['href']
        get_girl_detail(url)


# 解析图片详细
def get_girl_detail(url):
    # 返回一个 response 对象
    response = session.get(url)  # 单位秒数
    content = response.html.find('div.scroll-img-cont', first=True)
    li_list = content.find('li')
    for li in li_list:
        img_url = li.find('img', first=True).attrs['data-original']
        img_url = img_url[0:img_url.find('_')] + '.jpg'
        print(img_url + '.jpg')
        save_image(img_url)

# 保持大图
def save_image(img_url):
    img_response = requests.get(img_url)
    t = int(round(time.time() * 1000))  # 毫秒级时间戳
    f = open(os.getcwd() + "/pic_down/win4000/" + '%d.jpg' % t, 'ab')  # 存储图片，多媒体文件需要参数b（二进制文件）
    f.write(img_response.content)  # 多媒体存储content
    f.close()


if __name__ == '__main__':
    get_girl_list()