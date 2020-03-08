#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/3/5
    从选股宝网站爬取复盘数据
    爬取网站地址：https://xuangubao.cn/dingpan
    教程地址：https://blog.csdn.net/xy229935/article/details/89246114
'''
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import bs4
import time
import csv
import os
from selenium.webdriver.support.wait import WebDriverWait
##from Items import FuPanData

headers = {
 'Accept': 'application/json, text/plain, */*',
 'Accept-Encoding': 'gzip, deflate',
 'Accept-Language': 'zh-CN,zh;q=0.8',
 'Connection': 'keep-alive',
 'Content-Length': '14',
 'Content-Type': 'application/x-www-form-urlencoded',
 'Referer': 'https://xuangubao.cn',
 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 '
               'Mobile Safari/537.36'
}

def saveFuPan():
    try:
        browser = webdriver.Chrome()
        browser.get("https://xuangubao.cn/dingpan")
        # 超时时间为30秒，每0.2秒检查1次，直到class="tt"的元素出现
        text = WebDriverWait(browser, 30, 0.2).until(lambda x: x.find_element_by_css_selector("div .ban-chart-date-container")).text
        print(text)

        #browser.refresh()  # 刷新当前页面
        page = browser.page_source
        soup = BeautifulSoup(page, "lxml")
        #print(soup)

        # 得到日期
        # today = soup.find("div", attrs={"class", "ban-chart-date-container"}).find_all("p")
        # print(today[0].get_text().strip(),today[1].get_text().strip(),"日")
        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        print(date)
        # 查询涨跌数据
        spans = soup.find("div", attrs={"class": "ban-chart"}).find_all("span")
        print(spans)
        #items = spans.find_all("span")
        #if isinstance(spans, bs4.element.Tag):
        up = spans[3].get_text().strip()
        down = spans[4].get_text().strip()
        limitUp = spans[6].get_text().strip()
        limitDown = spans[7].get_text().strip()
        bomb = spans[8].get_text().strip()
        print("涨：", up)
        print("跌：", down)
        print("涨停：", limitUp)
        print("跌停：", limitDown)
        print("炸板率：", bomb)

        # 创建每天复盘数据对象
        todayData = FuPanData(date, up, down, limitUp, limitDown, bomb, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        # 连板个股相关操作
        listCount = []  # 连板个数
        guList = soup.find("table", attrs={"class", "table hit-pool__table"}).find_all("tr")

        # 判断当天连板个股是否保存
        if os.path.exists(os.getcwd() + "/xuangubao_file/" + date + ".csv"):
            os.remove(os.getcwd() + "/xuangubao_file/" + date + ".csv")

        # 循环读取连板个股
        for gu in guList[1:]:
            tds = gu.find_all("td")
            guName = tds[1].find_all("span")[0].get_text().strip()
            guCode = tds[1].find_all("a")[0].get_text().strip()[-6:]
            # print(guName,"(",guCode,")","：",tds[12].get_text().strip())
            listCount.append(tds[12].get_text().strip())  # 将连接数据保存到list
            # 将个股保存到CSV文件
            if tds[12].get_text().strip() != "首板":
                with open(os.getcwd() + "/xuangubao_file/" + date + ".csv", "a", newline="") as apdFile:
                    w = csv.writer(apdFile)
                    w.writerow([guName, guCode, tds[12].get_text().strip()])

        # 显示不同连板的个数
        for i in set(listCount):
            print("{0}：{1}".format(i, listCount.count(i)))
            if i == "首板":
                todayData.ban1 = listCount.count(i)
            elif i == "2连板":
                todayData.ban2 = listCount.count(i)
            elif i == "3连板":
                todayData.ban3 = listCount.count(i)
            elif i == "4连板":
                todayData.ban4 = listCount.count(i)
            elif i == "5连板":
                todayData.ban5 = listCount.count(i)
            elif i == "6连板":
                todayData.ban6 = listCount.count(i)
            elif i == "7连板":
                todayData.ban7 = listCount.count(i)
            elif i == "8连板":
                todayData.ban8 = listCount.count(i)
            elif i == "9连板":
                todayData.ban9 = listCount.count(i)
            elif i == "10连板":
                todayData.ban10 = listCount.count(i)
            else:
                todayData.ban10s = listCount.count(i)

        # 判断是否保存过数据 state为True表示已保存过
        with open(os.getcwd() + "/xuangubao_file/" + "dapanData.csv", "r") as csvfile:
            line = csvfile.readlines()[-1]
            d = line.split(",")[0]
            #print(date)
            #print(d)
            state = False
            # 判断是否有历史数据，如果有历史数据，是否有今天的数据
            if (len(d.strip()) > 0):
                state = int(date.split("-")[0]) == int(d.split("-")[0]) and \
                        int(date.split("-")[1]) == int(d.split("-")[1]) and \
                       int(date.split("-")[2]) == int(d.split("-")[2])
            # 将数据保存到csv文件
            if not state:
                dapanData = [todayData.date, todayData.up, todayData.down, todayData.limitUp, todayData.limitDown,
                             todayData.bomb,
                             todayData.ban1, todayData.ban2, todayData.ban3, todayData.ban4, todayData.ban5,
                             todayData.ban6,
                             todayData.ban7, todayData.ban8, todayData.ban9, todayData.ban10, todayData.ban10s]
                # print(dapanData)
                with open(os.getcwd() + "/xuangubao_file/" + "dapanData.csv", "a", newline="") as apdFile:
                    w = csv.writer(apdFile)
                    w.writerow(dapanData)
    except Exception as e:
        print("出错了")
        print("str(e):\t", str(e))
        print(repr(e))
        print(e.args)
        browser.close()
    else:
        print("今天数据已保存")
        browser.close()

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

#通过html内容不能获取页面数据，说明数据是动态加载的
def get_body():
    url = 'https://xuangubao.cn/dingpan'
    wb_data = requests.get(url)
    print(wb_data.text)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    print(soup.prettify())
    #print(soup)
    #print(soup.find_all('span', attrs={'class': 'jumpBusiness'}))

if __name__ == "__main__":
    saveFuPan()
    #get_body()
