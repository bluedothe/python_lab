#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/4/11
    字符串相关操作练习
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import chardet
import codecs
import os


#字符串格式化示例
def str_format():
    filesize = 1122
    print("filesize为: %s" %(filesize))   #变量要用括号

    full_path = "d:\\temp\\测试文件"
    full_path = "d:/temp/测试文件/"
    file_modify_time = "2020-04-05"
    print("{0} 修改时间是: {1}".format(full_path, file_modify_time))
    print("{} 修改时间是: {}".format(full_path, file_modify_time))

    db_paras = {"host": "localhost", "user": "root", "passwd": "root123","dbname": "mydb"}
    conn_str = 'mysql+pymysql://{user}:{passwd}@{host}/{dbname}?charset=utf8'.format(**db_paras)  #参数名前一定要加**
    print(conn_str)

    host = "localhost"
    user = "root"
    passwd = "root456"
    dbname = "mydb"
    conn_str2 = f'mysql+pymysql://{user}:{passwd}@{host}/{dbname}?charset=utf8'  #前面必须加f
    print(conn_str2)

#字符编码转码示例
#https://www.cnblogs.com/laogaoyang/p/5715671.html
def str_code():
    line = "this is a test str."
    #print("xx2:", chardet.detect(line))
    #print("xx3:", line.decode(encoding="gb2312"))
    #print("xx5:", chardet.detect((line.decode(encoding="gb2312")).encode("utf-8")))

    f = codecs.open('test.txt', encoding='UTF-8')
    u = f.read()
    f.close()
    print(type(u))  # <type 'unicode'>

    f = codecs.open('test.txt', 'a', encoding='UTF-8')
    # 写入unicode
    f.write(u)

    # 写入str，自动进行解码编码操作
    # GBK编码的str
    s = '汉'
    print(repr(s))  # '\xba\xba'
    # 这里会先将GBK编码的str解码为unicode再编码为UTF-8写入
    f.write(s)
    f.close()

#元组、序列、字典、字符串拼接
def str_join():
    a = ['1', '2', '3', '4', '5']
    print('  '.join(a))
    print(';'.join(a))
    print(','.join(v for v in a))

    b = "Hello My Boy"
    print(','.join(b))

    c = {'name1':'a','name2':'b','name3':'c','name4':'d'}
    print(','.join(c))
    print(','.join(c.keys()))
    print(','.join(c.values()))

#路径拼接
def path_join():
    print(os.path.join('/hello/','good/date','datbody','bac'))

#字符串分割与拼接，将分隔符由逗号换位斜杠
def str_join():
    mStr = '192.168.1.1,192.168.1.2,192.168.1.3'
    strList = mStr.split(',')
    newStr = '/'.join(strList)

#字符串分割
def str_split():
    str = 'http://q.10jqka.com.cn/zjhhy/detail/code/I/'
    strs = str.split('/')
    print(strs)
    print(str.split('/')[-2])  #取字母I
    print("1/12".split('/')[-1])
    print("abcdt"[2])

if __name__ == '__main__':
    str_split()