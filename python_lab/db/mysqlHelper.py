#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/2/28
    mysql数据库操作接口
'''

import pymysql

class mysqlHelper:
    def __init__(self, host, username, password, dbname):
        self.host = host
        self.username = username
        self.password = password
        self.dbname = dbname

    # 执行查询
    def select(self, sql):
        # 数据列表
        results = []
        # 打开数据库连接
        db = pymysql.connect(self.host, self.username, self.password, self.dbname)
        # 创建一个游标
        cursor = db.cursor()
        # 执行
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            print("执行SQL成功, sql: " + sql)
            # for row in results:
            #     ipurl = row[1]
            #     state = row[2]
            #     # 打印结果
            #     print("地址：{0:24}{1}".format(ipurl,state))
        except:
            print("执行SQL出错, sql: " + sql)
        # 关闭连接
        db.close()
        return results


    # 执行添加、删除和更新
    def exec(self, sql):
        # 打开数据库连接
        db = pymysql.connect(self.host, self.username, self.password, self.dbname)
        # 创建一个游标
        cursor = db.cursor()
        # 执行
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库
            db.commit()
            print("执行SQL成功, sql: " + sql)
        except:
            db.rollback()
            print("执行SQL出错, sql: " + sql)
        # 关闭连接
        db.close()


if __name__ == "__main__":
    host = "localhost"
    username = "root"
    password = "root123"
    dbname = "kdata"
    mysql = mysqlHelper(host,username,password,dbname)
    result = mysql.select("select * from t_kdata")
    for row in result:
        field_value = row[1]
        print(field_value)
