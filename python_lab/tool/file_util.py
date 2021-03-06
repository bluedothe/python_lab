#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/4/12
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import os
import codecs

#计算文件行数
def get_file_line_count(file):
    count = 0
    for index, line in enumerate(file):
        count += 1
    print(count)
    return count

#遍历目录下的所有文件
#传入要处理的目录和处理函数,其中处理函数必须要有两个参数：全路径文件名和文件名
def  traversal_dir(root_path,function_name):
    for root, dir, files in os.walk(root_path):
        for file in files:
            full_path = os.path.join(root, file)
            # print(full_path)
            # print(file)
            function_name(full_path, file)

'''删除文件 '''
def delete_file(fileName):
    if os.path.isfile(fileName):
        try:
            os.remove(fileName)
        except:
            pass

#将pandas的df对象保存为csv文件，如果文件不存在则新建，如果存在则追加
def df2csv_append(df, filename):
    if os.path.isfile(filename):
        df.to_csv(filename, index=False, mode='a', header=False, sep=',', encoding="utf_8_sig")
        print("更新一分钟all股票数据：", filename)
    else:
        df.to_csv(filename, index=False, mode='w', header=True, sep=',', encoding="utf_8_sig")
        print("新增加的一分钟all股票数据：", filename)

if __name__ == '__main__':
    print(os.path.isfile('E:/doc/design/dbmodel/yy'))