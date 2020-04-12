#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/3/8
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import os
import datetime
import time
from tool.printHelper import time_this_function
from tool import file_util

def test1():
    str = "abvcelsdss"
    print(str[5:-3])

def test2():
    timest = time.strftime("%Y-%m-%d")
    print(timest)
    print(timest.month)
    #now.strftime('%Y-%m-%d %H:%M:%S')
    timest.strftime('%Y-%m-%d')
    print(timest.strftime('%Y-%m-%d'))


def monthdays(y, m):
    oneday = datetime.timedelta(days=1)
    dt0 = datetime.datetime(y, m, 1)
    return filter(lambda dt: dt.month==m,map(lambda n: dt0+n*oneday, range(32)))

def getBetweenDay(begin_date):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d',time.localtime(time.time())), "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list

@time_this_function
def test3(year,month,day):
    date_list = []
    #begin_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    begin_date = datetime.datetime.strftime(datetime.datetime(year, month, day),"%Y-%m-%d")
    #begin_date = datetime.datetime(2020, 2, 1)
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    if year == datetime.date.today().year and month == datetime.date.today().month:
        end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
    else:
        end_date = last_day_of_month(begin_date)
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    print(date_list)

def test4():
    begin_date = datetime.datetime.strftime(datetime.datetime(2020, 2, 1),"%Y-%m-%d")
    print(begin_date)

def last_day_of_month(any_day):
    """
    获取获得一个月中的最后一天
    :param any_day: 任意日期
    :return: string
    """
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)

def string_format(self):
    paras = {"host":"localhost", "user":"root", "passwd":"root123", "dbname":"stock"}
    str = 'mysql://{user}:{passwd}@{host}/{dbname}?charset=utf8'.format(**paras)
    print(str)

def test5():
    time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
    end_dt = time_temp.strftime('%Y-%m-%d')
    print(end_dt)
    date_str = "20200403"
    mydate = time.strptime(date_str,'%Y%m%d')
    print(mydate)

#读取文件的创建时间和修改时间
def test6():
    t1 = time.ctime(os.stat("D:/Temp/f_00006b").st_mtime)  # 文件的修e5a48de588b67a686964616f31333365666263改时间
    print(datetime.datetime.strptime(t1, '%Y-%m-%d').date())
    t2 = time.ctime(os.stat("D:/Temp/f_00006b").st_ctime)  # 文件的创建时间
    print(datetime.datetime.strptime(t2, '%Y-%m-%d').date())
    t3 = time.localtime(os.stat("D:/Temp/f_00006b").st_mtime)  # 文件访问时间 适合计算时间
    print(datetime.datetime.strptime(t3, '%Y-%m-%d').date())
    t4 = ModifiedTime = time.localtime(os.stat("D:/Temp/f_00006b").st_mtime)  # 文件访问时间
    print(datetime.datetime.strptime(t4, '%Y-%m-%d').date())
    y = time.strftime('%Y', ModifiedTime)
    m = time.strftime('%m', ModifiedTime)
    d = time.strftime('%d', ModifiedTime)
    H = time.strftime('%H', ModifiedTime)
    M = time.strftime('%M', ModifiedTime)

#遍历目录，打印文件修改时间
def test7():
    path = "E:/database/csv/tushare/day_test/"
    for root, dir, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            #print(full_path)
            #print(file)
            mtime = os.stat(full_path).st_mtime
            file_modify_time = time.strftime('%Y-%m-%d', time.localtime(mtime))
            if file_modify_time > "2020-04-07":
                print("{0} 修改时间是: {1}".format(full_path, file_modify_time))

def test8(full_path, file):
    print("文件路径:{},{}".format(full_path, file))

if __name__ == '__main__':
    file_util.traversal_dir("D:/Temp/android/HelloWorld/res",test8)
