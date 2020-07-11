#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/3/5
    selenium模拟浏览器操作，可以用于自动化测试，或者爬取js中的数据
    使用前需要给浏览器安装插件，google浏览器的插件chromedriver.exe放到anconna目录中即可
    google插件下载地址：http://chromedriver.storage.googleapis.com/index.html
    selenium学习资料：https://blog.csdn.net/One_of_them/article/details/82560880
                    https://www.jianshu.com/p/1531e12f8852
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import time

#Chrome有界面运行
def test1():
    # 实例化出一个浏览器
    driver = webdriver.Chrome()

    # 打开一个页面
    driver.get("http://www.baidu.com")
    driver.find_element_by_id("kw").send_keys("selenium")
    driver.find_element_by_id("su").click()
    time.sleep(2)
    driver.quit()   # 使用完, 记得关闭浏览器, 不然chromedriver.exe进程为一直在内存中.

def test2():
    chrome_opt = Options()  # 创建参数设置对象.
    chrome_opt.add_argument('--headless')  # 无界面化.
    chrome_opt.add_argument('--disable-gpu')  # 配合上面的无界面化.
    chrome_opt.add_argument('--window-size=1366,768')  # 设置窗口大小, 窗口大小会有影响.

    # 创建Chrome对象并传入设置信息.
    driver = webdriver.Chrome(chrome_options=chrome_opt)
    # 操作这个对象.
    driver.get('https://www.baidu.com')  # get方式访问百度.
    time.sleep(2)
    print(driver.page_source)  # 获取当前页渲染后的源代码
    driver.quit()  # 使用完, 记得关闭浏览器, 不然chromedriver.exe进程为一直在内存中.

if __name__ == '__main__':
    #test1()
    test2()