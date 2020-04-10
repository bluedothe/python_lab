#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/4/10
'''

import unittest
from tool import datatime_util

""""
self.assertEqual(a,b,msg="None")  判断a,b是否相等，不相等时，抛出msg；
self.assertTure(x,msg="None") 判断x表达式是否为真，表达式为假时，抛出msg；
self.assertIn(a,b,msg="None") 判断a是否在b里面，a不在b里面时，抛出msg；
self.assertIsNone(x,msg="None") 判断x是否为空，x不为空时，抛出msg。
更多参考：https://www.cnblogs.com/xiaoxiaolvdou/p/9503090.html
断言也可以直接写>= = <= 来判断，比如：assert sum >= 10
"""

class TestDatetimeUtil(unittest.TestCase):
    def setUp(self) -> None:
        pass
    def tearDown(self) -> None:
        pass

    def test01(self):
        try:
            print(datatime_util.curDatetime(datatime_util.TIME_FORMAT))
            print(datatime_util.curDatetime(datatime_util.DATE_FORMAT))
            print(datatime_util.curDatetime(datatime_util.DATETIME_FORMAT))
            print(datatime_util.curDatetime(datatime_util.DATETIME_FORMAT))
        except Exception as e:
            print("断言出错了:{}".format(e))
            raise e

    def test02(self):
        try:
            print(datatime_util.curDatetime(datatime_util.TIME_FORMAT))
            print(datatime_util.curDatetime(datatime_util.DATE_FORMAT))
            print(datatime_util.curDatetime(datatime_util.DATETIME_FORMAT))
            print(datatime_util.curDatetime(datatime_util.DATETIME_FORMAT))
        except Exception as e:
            print("断言出错了:{}".format(e))
            raise e


if __name__ == '__main__':
    # verbosity=*：默认是1；设为0，则不输出每一个用例的执行结果；2-输出详细的执行结果
    unittest.main(verbosity=1)      #执行当前页面test_开头的所有用例