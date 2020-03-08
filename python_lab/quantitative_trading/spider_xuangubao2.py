#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/3/8
    爬取选股宝网站数据
    教程地址：https://blog.csdn.net/xy229935/article/details/90019252
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"
from selenium import webdriver
from bs4 import BeautifulSoup
from _datetime import datetime
import common.datetime_oper as do
import os
import shutil
import time
import csv

class XuanGuBao():
    # 创建"agudata"，复盘数据表"dapan.csv"
    dapan_path = "agudata"  # 保存数据的目录
    dapan = "dapan.csv"  # 复盘数据表
    # 创建浏览器对象，使用chrome浏览器的headless模式(无窗体模式)
    # chrome_options = webdriver.chrome.options.Options()
    # chrome_options.add_argument("--headless")
    # browser = webdriver.Chrome(chrome_options=chrome_options)
    browser = webdriver.Chrome()
    page = browser.page_source  # 得到页面源码
    soup = BeautifulSoup(page, "lxml")

    #################################################
    # 创建目录和复盘数据文件
    def create_path(self):
        # 如果目录存在，则删除
        if (os.path.exists(self.dapan_path)):
            shutil.rmtree(self.dapan_path)

        # 创建目录
        os.mkdir(self.dapan_path)
        # 创建文件
        with open(self.dapan, "a", newline="") as file:
            w = csv.writer(file)
            w.writerow(
                ['日期', '红盘', '绿盘', '涨停', '跌停', '炸板率', '1板', '2板', '3板', '4板', '5板', '6板', '7板', '8板', '9板', '10板',
                 '10板以上'])

    #################################################
    #################################################
    # 登录选股网站
    def login(self):
        # 一、打开首页
        self.browser.get("https://xuangubao.cn")
        loginlink = self.browser.find_element_by_css_selector(".go-login")
        loginlink.click()
        # 二、点击登录链接
        time.sleep(1)
        loginid = self.browser.find_element_by_css_selector(".login-phone-input");
        loginid.send_keys(data.xgb_id)
        loginpwd = self.browser.find_element_by_css_selector(".login-setpwd-input")
        loginpwd.send_keys(data.xgb_pwd)
        loginbtn = self.browser.find_element_by_css_selector(".login-btn")
        loginbtn.click()
        # 三、登录后等1秒
        time.sleep(1)

    #################################################
    #################################################
    # ——————得到大盘复盘数据对象——————
    # date: 字符串类型
    def get_todaydata(self, date):
        spans = self.soup.find("div", attrs={"class": "ban-chart"}).find_all("span")
        up = spans[3].get_text().strip()  # 涨
        down = spans[4].get_text().strip()  # 跌
        limitUp = spans[6].get_text().strip()  # 涨停
        limitDown = spans[7].get_text().strip()  # 跌停
        bomb = spans[8].get_text().strip()  # 炸板率
        return FuPanData(date, up, down, limitUp, limitDown, bomb, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    # ——————统计每种连板情况的个数——————
    # date: 字符串类型
    def calc_lianbanamount(self, today_data, list_count):
        for i in set(list_count):
            # print("{0}：{1}".format(i, list_count.count(i)))
            if i == "首板":
                today_data.ban1 = list_count.count(i)
            elif i == "2连板":
                today_data.ban2 = list_count.count(i)
            elif i == "3连板":
                today_data.ban3 = list_count.count(i)
            elif i == "4连板":
                today_data.ban4 = list_count.count(i)
            elif i == "5连板":
                today_data.ban5 = list_count.count(i)
            elif i == "6连板":
                today_data.ban6 = list_count.count(i)
            elif i == "7连板":
                today_data.ban7 = list_count.count(i)
            elif i == "8连板":
                today_data.ban8 = list_count.count(i)
            elif i == "9连板":
                today_data.ban9 = list_count.count(i)
            elif i == "10连板":
                today_data.ban10 = list_count.count(i)
            else:
                today_data.ban10s = list_count.count(i)

    # ——————保存连板个股数据，并返回list_count（该列表用于统计每种连板股的个数）——————
    # date: 字符串类型
    def get_lianbandata(self, date):
        guList = self.soup.find("table", attrs={"class", "table hit-pool__table"}).find_all("tr")
        # 1. 判断当天连板个股是否保存，如果保存过则删除
        today_path = self.dapan_path + "\\" + date + ".csv"
        if os.path.exists(today_path):
            os.remove(today_path)
        # 2. 循环读取连板个股
        list_count = []  # 连板个数
        for gu in guList[1:]:  # 为了剔除列标题，从1开始
            tds = gu.find_all("td")
            name = tds[1].find_all("span")[0].get_text().strip()
            code = tds[1].find_all("a")[0].get_text().strip()[-6:]
            # 保存所属板块
            reason = ''
            if (len(tds[2].select("span.line-clamp")) > 0):
                reason = tds[2].select("span.line-clamp")[0].get_text()
            if (len(reason.split('|')) > 0):
                reason = reason.split('|')[0].strip()

            sealdate = tds[10].get_text().strip()
            level = tds[12].get_text().strip()
            list_count.append(level)  # 将连板数据保存到list
            stock = StockData(name, code, reason, sealdate, level)  # 创建股票对象
            # 将个股保存到CSV文件  （如果需要T除首板加上代码：if tds[12].get_text().strip()!="首板"）
            with open(today_path, "a", newline="") as apdFile:
                w = csv.writer(apdFile)
                w.writerow(stock.__dict__.values())
        return list_count

    # ——————保存复盘数据——————
    # date: datetime类型
    def fupan(self, date):
        date = str(date.date())  # 将日期转换成字符串
        print(date)
        self.page = self.browser.page_source  # 得到页面源码
        self.soup = BeautifulSoup(self.page, "lxml")
        # 1.复盘数据对象
        today_data = self.get_todaydata(date)
        # 2.保存连板个股数据
        list_count = self.get_lianbandata(date)
        # 3.计算连板个数
        self.calc_lianbanamount(today_data, list_count)
        # 4.保存大盘数据
        with open(self.dapan, "a", newline="") as apdFile:
            w = csv.writer(apdFile)
            w.writerow(today_data.__dict__.values())
        print("数据已保存")

    # ——————下载指定日期复盘数据——————
    def get_fupandata(self, date):
        # try:
        self.browser.get("https://xuangubao.cn/dingpan")  # 打开盯盘页面
        # 1.得到日期DIV节点
        date_node = self.browser.find_element_by_css_selector(".ivu-date-picker")
        date_node.click()  # 点击日期DIV

        # 2.读取日历DIV中的年和月，并点击月标签切换月份
        ym = self.browser.find_elements_by_css_selector(".ivu-date-picker-header-label")
        ym[1].click()  # 点击年月标签

        # 3.读取月份列表，选择月份
        month_list = self.browser.find_elements_by_css_selector(".ivu-date-picker-cells-cell")
        for m_node in month_list:
            m_node_text = m_node.text.split("月")[0]
            if (m_node_text == str(date.month)):
                m_node.click()  # 选择月份
                break

        # 4.读取日期，并点击日期标签切换日期
        day_list = self.browser.find_elements_by_css_selector(".ivu-date-picker-cells-cell")
        for d_node in day_list:
            cls = d_node.get_attribute("class")  # 得到节点的样式属性
            if (len(d_node.text) > 0 and int(d_node.text) == date.day and
                    (str(cls) == "ivu-date-picker-cells-cell" or
                     str(cls).find("ivu-date-picker-cells-cell-today") >= 0)):
                d_node.click()  # 选择日期
                break

        # 5.读取日期DIV的数据，如果与所选日期相同，说明更新了数据
        date_m = self.browser.find_element_by_css_selector(".ban-chart-date-day")
        if (int(date_m.text) == date.day):
            time.sleep(1)  # 暂停1秒，等数据刷新
            # 得到指定日期的数据并保存
            self.fupan(date)

    # except Exception as e:
    #     print ("出错了，\t", str(e))
    #################################################
    #################################################
    # 下载指定月份的数据
    # start_month: 开始月份，end_month: 结束月份
    def start(self, start_month, end_month):
        self.login()  # 登录

        # 创建所有目录，并保存数据
        m = start_month
        while m <= end_month:
            # 修改大盘复盘数据文件名为dapan_年_月.csv
            datepath = str(datetime.now().date().year) + "_" + str(m);
            self.dapan_path = "agudata\\" + datepath
            self.dapan = self.dapan_path + "\\dapan_" + datepath + ".csv";
            self.create_path()  # 创建保存数据的目录和文件

            # 遍历指定月份的所有日期，如果是当前月份则到当前日期，下载每日数据
            date_list = do.getdatelist(m)  #类型为list，格式：2019-05-23
            for date in date_list:
                xgb.get_fupandata(date)
            print(str(date.month) + "月全部保存成功")

            m += 1
            # 如果大于当前月份则退出
            if (m > datetime.now().date().month):
                break;

        self.browser.quit()  # 关闭浏览器
    #################################################

class FuPanData:
    def __init__(self,date, up, down, limitUp, limitDown,bomb,ban1, ban2, ban3, ban4, ban5,ban6,ban7, ban8, ban9, ban10, ban10s):
        self.date = date
        self.up = up
        self.down = down
        self.limitUp = limitUp
        self.limitDown = limitDown
        self.bomb = bomb
        self.ban1 = ban1
        self.ban2 = ban2
        self.ban3 = ban3
        self.ban4 = ban4
        self.ban5 = ban5
        self.ban6 = ban6
        self.ban7 = ban7
        self.ban8 = ban8
        self.ban9 = ban9
        self.ban10 = ban10
        self.ban10s = ban10s

    def StockData(self):
        pass

if __name__ == "__main__":
    month = datetime.now().month
    xgb = XuanGuBao()
    xgb.start(month, month)  # 下载5月的所有数据
