#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2019/11/29
    爬取股票交易数据
'''

import pymysql
import numpy as np
import sys
import json
import urllib.request
import urllib
import os
import time

__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2019"

gp_count = 1  # 股票当天所有数据的保存编号

def db_connect():
    # 连接数据库
    db = pymysql.connect(host='127.0.0.1', user='root', password='root', db='gp_db', port=3306)
    # 获取cursor
    cursor = db.cursor()  # 使用 execute() 方法执行 SQL，如果表存在则删除
    sql = "select * from gp"
    cursor.execute(sql)
    print("SELECT OK")
    # all_gp = cursor.fetchmany(1)
    all_gp = cursor.fetchall()  # 从数据库中获取所有股票的基本信息数据
    arr = np.array(all_gp)  # 转化为numpy数据格式

    now = int(time.time())
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    timeStruct = time.localtime(now)
    strTime = time.strftime("%Y-%m-%d", timeStruct)
    db.commit()
    db.close()

def mkdir(path):  # 股票保存路径函数
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print(path)


def getData(url):  # 函数——从接口中获取单只股票当天每分钟的数据
    content = ""
    try:  # 网络会偶发出现奔溃情况，为了保证不中断和保证数据齐全，休息5秒重新执行
        response = urllib.request.urlopen(url)
        content = response.read().decode('utf-8')
        print(content)
    except:
        print("发生网络异常")
        time.sleep(5)
        return getData(url)
    if content != "":
        return content
    else:
        print("内容为空")
        return getData(url)


def csv_create(path, msg):  # 函数——将单只股票的数据保存进指定文件夹
    file = open(path, 'w')
    file.write(msg)
    print("文件" + path + "创建成功")
    file.close()


def tranformToCSV(content, filepath):  # 函数——将下载的数据转换为csv数据，以便读取
    content = content.replace("(", "").replace(")", "")
    json_str = json.loads(content)
    a_str = json_str.get("data")
    a_time = json_str.get("info").get("time")
    a_date = str(a_time).split(" ")
    mkdir(filepath)
    array_str = np.array(a_str)
    csv_str = "time,first,second,third,fourth\n"  # time为当天时间点，first为该分钟股票价格
    for item in array_str:
        item = str(item)
        items = item.split(",")
        itemss = (str(items[0])).split(" ")
        items0 = itemss[1]
        csv_str += '"' + items0 + '",' + items[1] + ',' + items[2] + ',' + items[3] + ',' + items[4] + '\n'
    csv_create(filepath + "/" + a_date[0] + ".csv", csv_str)

def exec():
    arr = []
    for item in arr:
       url = "http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&id=" + item[3] + item[1] + "&type=r&iscr=false"
       data = getData(url)
       item2 = item[2].replace("*", "")
       tranformToCSV(data, "D://gp/" + str(gp_count) + "、" + item2 + item[3])  # 股票信息的保存路径是（D：//pg/序号+股票名字+股票代号/日期.csv）
       gp_count = gp_count + 1;
       # 使用 DebugLog

def get_data(gpflag, gpname, gpcode):
    gp_count = 1
    url = "http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&id=" + gpcode + gpflag + "&type=r&iscr=false"
    print(url)
    data = getData(url)
    item2 = gpname.replace("*", "")
    tranformToCSV(data, "D://gp/" + str(gp_count) + "、" + gpname + gpcode)  # 股票信息的保存路径是（D：//pg/序号+股票名字+股票代号/日期.csv）
    gp_count = gp_count + 1;

if __name__ == '__main__':
    get_data('1', '桐昆股份', '6001233')