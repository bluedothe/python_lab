#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/2/12
'''


import pymysql

__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"


class CT_Kdata:
    def __init__(self, connect):
        self.connect = connect

    # 增加k线数据
    def add_kdata(self, code, trade_day, open, close, high, low, vol):
        if self.connect is None:
            return -1

        ret = self.exist_kdata_day(code, trade_day)
        if ret > 0:
            return 0

        # 得到一个可以执行SQL语句的光标对象
        cursor = self.connect.cursor()

        # sql语句
        sql = "insert into t_kdata (code,trade_day, open, close, high, low, vol) VALUE (%s,%s,%s,%s,%s,%s,%s);"
        print(sql)

        try:
            # 执行SQL语句
            self.connect.ping(reconnect=True)
            cursor.execute(sql, (code, trade_day, open, close, high, low, vol))
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
            self.connect.ping(reconnect=True)
            cursor.execute(sql, (code,))
            # 把修改的数据提交到数据库
            self.connect.commit()
        except Exception as e:
            # 捕捉到错误就回滚
            self.connect.rollback()
            print(e)

        # 关闭光标对象
        cursor.close()

    def modify_kdata(self, code, trade_day, ma5, ma10, ma20):
        if self.connect is None:
            return -1

        # 得到一个可以执行SQL语句的光标对象
        cursor = self.connect.cursor()

        # sql语句
        sql = "update t_kdata set ma5='" + ma5 + \
              "' ,ma10='" + ma10 + \
              "' ,ma20='" + ma20 + \
              "' where code='" + code + "' and trade_day='" + trade_day + "';"
        print(sql)

        try:
            # 执行SQL语句
            self.connect.ping(reconnect=True)
            cursor.execute(sql)
            # 把修改的数据提交到数据库
            self.connect.commit()
        except Exception as e:
            # 捕捉到错误就回滚
            self.connect.rollback()
            print(e)

        # 关闭光标对象
        cursor.close()

    # 判断某个股票代码是否存在
    def exist_kdata(self, code):
        if self.connect is None:
            return -1

        # 得到一个可以执行SQL语句的光标对象
        cursor = self.connect.cursor()

        # sql语句
        sql = "select 1 from t_kdata where code = '" + code + "' limit 1;"
        print(sql)

        try:
            # 执行SQL语句
            self.connect.ping(reconnect=True)
            cursor.execute(sql)
            # 把修改的数据提交到数据库
            self.connect.commit()

            result = cursor.fetchone()
            # 关闭光标对象
            cursor.close()

            if result is None:
                return 0

            for i in result:
                print(i)
                if i == 1:
                    return 1

        except Exception as e:
            # 捕捉到错误就回滚
            self.connect.rollback()
            print(e)
        return 0

    # 判断某个股票代码,在具体日期的k线数据是否存在
    def exist_kdata_day(self, code, trade_day):
        if self.connect is None:
            return -1

        # 得到一个可以执行SQL语句的光标对象
        cursor = self.connect.cursor()

        # sql语句
        sql = "select 1 from t_kdata where code = '" + code + "'and trade_day='" + trade_day + "' limit 1;"
        print(sql)

        try:
            # 执行SQL语句
            self.connect.ping(reconnect=True)
            cursor.execute(sql)
            # 把修改的数据提交到数据库
            self.connect.commit()

            result = cursor.fetchone()
            # 关闭光标对象
            cursor.close()

            if result is None:
                return 0

            for i in result:
                print(i)
                if i == 1:
                    return 1

        except Exception as e:
            # 捕捉到错误就回滚
            self.connect.rollback()
            print(e)
        return 0

    def query_kdata(self, code):
        if self.connect is None:
            return -1

        # 得到一个可以执行SQL语句的光标对象
        cursor = self.connect.cursor()

        # sql语句
        sql = "select * from t_kdata where code = '%s';"
        print(sql)

        try:
            # 执行SQL语句
            self.connect.ping(reconnect=True)
            cursor.execute(sql, (code,))
            # 把修改的数据提交到数据库
            self.connect.commit()

            result = cursor.fetchone()

            for i in result:
                print(i)

        except Exception as e:
            # 捕捉到错误就回滚
            self.connect.rollback()
            print(e)

        # 关闭光标对象
        cursor.close()
        return 0

if __name__ == '__main__':
    pass