#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/2/11
'''

import pymysql

__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"


class CDBMgr:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connect = None

    # connect database
    def connect_db(self):
        self.connect = pymysql.connect(self.host, self.user, self.password, self.database, charset="utf8")

    def create_table(self):
        # 得到一个可以执行SQL语句的光标对象
        cursor = self.connect.cursor()
        # 定义要执行的SQL语句
        self.connect.ping(reconnect=True)
        sql0 = 'DROP TABLE IF EXISTS t_kdata;'
        # 执行SQL语句
        cursor.execute(sql0)

        sql = """
        CREATE TABLE t_kdata (
            id INT auto_increment  PRIMARY KEY,
            code CHAR(10) NOT NULL UNIQUE COMMENT '股票代码',
            open DECIMAL(10,2) NOT NULL COMMENT '开盘价',
            close DECIMAL(10,2) NOT NULL COMMENT '收盘价',
            high DECIMAL(10,2) NOT NULL COMMENT '最高价',
            low DECIMAL(10,2) NOT NULL COMMENT '最低价',
            amount DECIMAL(25,2) COMMENT '成交额(千元)',
            vol DECIMAL(25,2) COMMENT '成交量(手)',
            ma5vol DECIMAL(25,2)  COMMENT '5日平均成交量',
            ma10vol DECIMAL(25,2) COMMENT '10日平均成交量',
            ma20vol DECIMAL(25,2) COMMENT '20日平均成交量',
            ma30vol DECIMAL(25,2) COMMENT '30日平均成交量',
            ma5 DECIMAL(10,2) COMMENT '5日平均收盘价',
            ma10 DECIMAL(10,2) COMMENT '10日平均收盘价',
            ma20 DECIMAL(10,2) COMMENT '20日平均收盘价',
            ma30 DECIMAL(10,2) COMMENT '30日平均收盘价',
            ma60 DECIMAL(10,2) COMMENT '60日平均收盘价',
            pct_chg DECIMAL(10,2) COMMENT '涨跌幅'            
        )ENGINE=innodb DEFAULT CHARSET=utf8;
        """
        # 查看注释的sql语句
        # show full columns from k_data;
        # print(sql)

        # 执行SQL语句
        self.connect.ping(reconnect=True)
        cursor.execute(sql)
        # 关闭光标对象
        cursor.close()

    # 增加k线数据
    def add_kdata(self, code, open, close, high, low, vol):
        if self.connect is None:
            return -1

        # 得到一个可以执行SQL语句的光标对象
        cursor = self.connect.cursor()

        # sql语句
        sql = "insert into t_kdata (code, open, close, high, low, vol) VALUE (%s,%s,%s,%s,%s,%s);"
        # sql = "insert into t_kdata (code, open, close, high, low, vol) VALUE ("+code+","+open+","+close+","+high+","+low+","+vol+");"
        print(sql)

        try:
            # 执行SQL语句
            self.connect.ping(reconnect=True)
            cursor.execute(sql, (code, open, close, high, low, vol))
            # cursor.execute(sql)
            # 把修改的数据提交到数据库
            self.connect.commit()
        except Exception as e:
            # 捕捉到错误就回滚
            self.connect.rollback()
            print(e)

        # 关闭光标对象
        cursor.close()

    # 根据股票代码，删除表中的数据
    def del_kdata(self, code):
        if self.connect is None:
            return -1

        # 得到一个可以执行SQL语句的光标对象
        cursor = self.connect.cursor()

        # sql语句
        sql = "delete from t_kdata where code=%s;"
        print(sql)

        try:
            # 执行SQL语句
            cursor.execute(sql, (code,))
            # 把修改的数据提交到数据库
            self.connect.commit()
        except Exception as e:
            # 捕捉到错误就回滚
            self.connect.rollback()
            print(e)

        # 关闭光标对象
        cursor.close()

    def modify_kdata(self, code, open, close, high, low, vol):
        if self.connect is None:
            return -1

        # 得到一个可以执行SQL语句的光标对象
        cursor = self.connect.cursor()

        # sql语句
        sql = "insert into t_kdata (code, open, close, high, low, vol) VALUE (%s, %s, %s, %s, %s, %s);"
        print(sql)

        try:
            # 执行SQL语句
            cursor.execute(sql, (code, open, close, high, low, vol))
            # 把修改的数据提交到数据库
            self.connect.commit()
        except Exception as e:
            # 捕捉到错误就回滚
            self.connect.rollback()
            print(e)

        # 关闭光标对象
        cursor.close()

    def test_db_conn(self):
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = self.connect.cursor()

        # 使用 execute()  方法执行 SQL 查询
        cursor.execute("SELECT VERSION()")

        # 使用 fetchone() 方法获取单条数据.
        data = cursor.fetchone()

        print("Database version : %s " % data)

        # 关闭数据库连接
        self.connect.close()

def test():
    host = "127.0.0.1"
    user = "root"
    password = "root123"
    dbname = "kdata"
    dbmgr = CDBMgr(host,user,password,dbname)
    dbmgr.connect_db()
    dbmgr.test_db_conn()
    #dbmgr.create_table()
    dbmgr.add_kdata('000001',11.38,11.36,11.55,11.28,754246)
if __name__ == '__main__':
    test()
