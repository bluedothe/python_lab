#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/2/11
'''
import pymysql
from quantitative_trading.exam1.cdbmgr import CDBMgr

__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

def test_db():
    # 打开数据库连接
    #db = pymysql.connect("localhost", "root", "", "jeesite")
    db = pymysql.connect("127.0.0.1", "root", "root123", "kdata")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("SELECT VERSION()")

    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()

    print("Database version : %s " % data)

    # 关闭数据库连接
    db.close()

def test():
    host = "127.0.0.1"
    user = "root"
    password = "root123"
    dbname = "kdata"
    dbmgr = CDBMgr(host,user,password,dbname)
    dbmgr.connect_db()
    print(type(dbmgr))
    #dbmgr.create_table()

if __name__ == '__main__':
    #test_db()
    test()