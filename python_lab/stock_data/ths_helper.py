#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/3/28
    从同花顺网页爬取板块数据
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re
from lxml import etree

class ThsHelper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        url = "http://q.10jqka.com.cn/thshy/"
        driver.get(url)
        # 获取cookie列表
        cookies = driver.get_cookies()
        driver.close()
        self.cookie = cookies[0]['value']

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Referer': 'http://q.10jqka.com.cn/thshy/detail',
            'Cookie': 'v={}'.format(self.cookie)
        }

    # 获取网页详情页
    def get_page_detail(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                html = response.text.encode('utf-8')
                bs = BeautifulSoup(html, "html.parser")
                return bs
            return None
        except RequestException:
            print('请求页面失败', url)
            return None

    # 获取网页详情页
    def get_page_html(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                html = response.text.encode('utf-8')
                return html
            return None
        except RequestException:
            print('请求页面失败', url)
            return None

    # 同花顺行业数据
    def get_block_thshy(self):
        thshy_code_name = []  # 行业代码数组
        thshy_codes_href = []  # 行业代码名称字典
        url = "http://q.10jqka.com.cn/thshy/index/field/199112/order/desc/page/{}/ajax/1/"
        page_no = 1
        while True:
            bs = self.get_page_detail(url.format(page_no))
            if bs is None:
                print("page_no",page_no)
                break
            list = bs.find('tbody').find_all("a", target="_blank", href=re.compile("q.10jqka.com.cn/thshy"))
            if len(list) == 0:
                print("page_no", page_no)
                break
            #print(list)
            #print(len(list))
            for line in list:
                href = str((line.get('href')))
                block_name = line.get_text
                block_code = href.split("/")[-2]
                thshy_code_name.append({"code": block_code, "name": block_name})
                thshy_codes_href.append({"code": block_code, "href": href})
            page_no = page_no + 1
        print(thshy_code_name)
        print(len(thshy_code_name))
        print(thshy_codes_href)
        print(len(thshy_codes_href))

    # 同花顺行业成分股数据
    def get_block_member_thshy(self,block_code):
        url = "http://q.10jqka.com.cn/thshy/detail/code/{}/"
        url = "http://q.10jqka.com.cn/thshy/detail/field/199112/order/desc/page/{}/ajax/1/code/{}"
        page_no = 1
        while True:
            bs = self.get_page_html(url.format(page_no,block_code))
            if bs is None:
                print("page_no(none): ", page_no)
                break
            #//*[@id="maincont"]/table/tbody/tr[1]/td[2]/a
            #list = bs.find('tbody').find_all("a", target="_blank", href=re.compile("q.10jqka.com.cn/thshy"))
            selector = etree.HTML(bs)
            list = selector.xpath('//*[@id="maincont"]/table/tbody/tr[1]/td[2]/a')
            if len(list) == 0:
                print("page_no(0): ", page_no)
                break
            print(list)
            print(len(list))
            page_no = page_no + 1

if __name__ == '__main__':
    ths = ThsHelper()
    ths.get_block_member_thshy('881116')