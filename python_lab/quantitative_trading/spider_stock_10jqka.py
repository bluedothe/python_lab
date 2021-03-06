#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/3/25
    Python 爬取同花顺行业板块日K线数据
    教程地址：https://www.jianshu.com/p/5961ed3da338
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time,os

# 所有行业代码
# [881148,
# 881129,881130,881166,881121,881138,881151,881134,
# 881123,881149,881136,881157,881124,881109,881119,
# 881133,881127,881117,881131,881118,881139,881120,
# 881102,881106,881155,881126,881110,881152,881163,
# 881107,881111,881122,881103,881144,881142,881159,
# 881158,881145,881105,881147,881164,881146,881116,
# 881143,881113,881115,881104,881128,881161,881132]


class AnalysisIndustry:
    def __init__(self):
        self.industry_codes = []   #行业代码数组
        self.industry_codes_dict = []   #行业代码名称字典

    # 获取动态cookies
    def get_cookie(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        url = "http://q.10jqka.com.cn/thshy/"
        driver.get(url)
        # 获取cookie列表
        cookie = driver.get_cookies()
        driver.close()
        return cookie[0]['value']

    # 获取网页详情页
    def get_page_detail(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Referer': 'http://q.10jqka.com.cn/thshy/detail',
            'Cookie': 'v={}'.format(self.get_cookie())
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.text.encode('utf-8')
            return None
        except RequestException:
            print('请求页面失败', url)
            return None

    # 获取行业列表的html数据 名称title、代码code、链接url
    def get_industry_list(self, url):
        html = self.get_page_detail(url)
        bs = BeautifulSoup(html, "html.parser")
        #print(bs.prettify())  # 缩进格式
        return bs

    #同花顺行业数据
    def get_indusrty_codes(self):
        instury_index_url = 'http://q.10jqka.com.cn/thshy/'
        instury_index_url = 'http://q.10jqka.com.cn/thshy/index/field/199112/order/desc/page/3/ajax/1/'

        bs = self.get_industry_list(instury_index_url)
        list = bs.find('tbody').find_all("a", target="_blank")  # 龙虎榜的stock
        print(list)
        print(len(list))
        for line in list:
            href = str((line.get('href')))
            if (href.find('thshy') == -1) is False:
                ret = href.split("/")[-2]
                self.industry_codes.append(ret)
                self.industry_codes_dict.append({"code":ret,"name":line.get_text()})
        print(self.industry_codes)
        #print(len(self.industry_codes))
        #print(self.industry_codes_dict)

    def get_one_data(self, code_industry):
        url = 'http://d.10jqka.com.cn/v4/line/bk_' + code_industry + '/01/last.js'
        html = self.get_page_detail(url).decode('gbk')
        print(html)
        return html

    def get_all_data(self):
        with open(os.getcwd() + "/ths_file/" + 'all_industry_data.txt', 'w') as f:
            for code in self.industry_codes:
                data = self.get_one_data(str(code))
                f.write(str(data) + "\n")
                time.sleep(1)

if __name__ == '__main__':
    s = AnalysisIndustry()
    #s.get_indusrty_codes()
    #s.get_all_data()
    s.get_one_data("881101")  #881101种植业与林业
    #s.get_industry_list('http://d.10jqka.com.cn/v4/line/bk_' + '881101' + '/01/last.js')