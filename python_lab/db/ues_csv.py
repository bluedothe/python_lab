#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/3/5
    csv文件读写方法
'''

import csv
import os
import time

# 获取当天系统日期 如20190308
timest = time.strftime("%Y%m%d")
#file_name = os.getcwd() + "/csv_file/" + '/csv_' + timest + '.csv'
file_name = os.getcwd() + "/csv_file/" + '/csv_test' + '.csv'

# 判断文件是否存在
def test_remove():
    if os.path.exists(file_name):
        os.remove(file_name)

# 将数据写入文件
def test_write():
    with open(file_name, "a", newline="") as cf:
        w = csv.writer(cf)
        w.writerow([1001, "北京"])
        w.writerow([1002, "上海"])
        w.writerow([1003, "广州"])
        cf.close()

# 将数据从文件读出
def test_read():
    with open(file_name, "r") as cf:
        d = csv.reader(cf)
        for row in d:
            print(row)

def test_dir():
    path = os.getcwd() + "/../.."
    print(path)
    print(os.listdir()) #当前目录下的文件和子目录，不递归
    for s in os.listdir():
        print(s)  # 输出文件名
        print(os.path.join(os.getcwd(),s))  #输出绝对路径
    print(os.listdir(path))  # 本级目录下的文件和子目录，不递归

#递归处理文件夹示例，删除__pycache__名称的文件夹
def clear(filepath):
    files = os.listdir(filepath)
    for fd in files:
        cur_path = os.path.join(filepath, fd)
        if os.path.isdir(cur_path):
            if fd == "__pycache__":
                print("删除文件夹： %s" % cur_path)
                os.system("rm %s -rf" % cur_path) #linux下的写法
                os.system("rd /s/q %s" % cur_path) #windows下的写法
            else:
                clear(cur_path)

def test_walk():
    path = os.getcwd()
    for root, dirs, files in os.walk(path):
        print("root: " + root)
        for dir in dirs:
            print(os.path.join(root,dir))
        for file in files:
            print(os.path.join(root,file))

#在指定的目录中搜索文件
def test_search_file():
    path = os.getcwd()
    search_file = "csv_test.csv"
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == search_file:
                print(os.path.join(root,file))

if __name__ == '__main__':
    #test_remove()
    #test_write()
    #test_read()
    #test_dir()
    #test_walk()
    test_search_file()