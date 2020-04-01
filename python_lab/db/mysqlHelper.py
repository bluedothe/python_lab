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
        # 关闭游标
        cursor.close()
        # 关闭连接
        db.close()
        return results


    # 执行添加、删除和更新
    # 有values参数则会执行批量操作，这时sql参数格式为：'insert into '表名'(字段名) values(%s,%s,%s,%s)'，
    # values参数的格式为数组或元组内套元组：[(),(),()]或((),(),())
    # values的生成方法：values = [],values.append(('需要插入的字段对应的value'))  这里注意要用两个括号扩起来
    def exec(self, sql, *values):
        # 打开数据库连接
        db = pymysql.connect(self.host, self.username, self.password, self.dbname)
        # 创建一个游标
        cursor = db.cursor()
        # 执行
        try:
            # 执行SQL语句
            if values == ():
                print("单条执行")
                cursor.execute(sql)
            else:
                print("批量执行")
                cursor.executemany(sql,values)
            # 提交到数据库
            db.commit()
            print("执行SQL成功, sql: " + sql)
        except Exception as ex:
            db.rollback()
            print("执行SQL出错, sql: " + sql)
            print("出现如下异常: %s" % ex)
        # 关闭游标
        cursor.close()
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
