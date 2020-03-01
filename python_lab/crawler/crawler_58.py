#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tool import printHelper
from bs4 import BeautifulSoup
import requests
import time
import json
import re
from fake_useragent import UserAgent  #代理


'''
    module description
    date: 2020/1/30
    爬取58同城,里面主要用到BeautifulSoup 的select()方法
    来源：https://www.jianshu.com/p/698c50f734a9
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

headers = {
 'Accept': 'application/json, text/plain, */*',
 'Accept-Encoding': 'gzip, deflate',
 'Accept-Language': 'zh-CN,zh;q=0.8',
 'Connection': 'keep-alive',
 'Content-Length': '14',
 'Content-Type': 'application/x-www-form-urlencoded',
 'Referer': 'https://bj.58.com',
 'User-Agent': str(UserAgent(verify_ssl=False).random)
 #'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
 #              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 '
 #              'Mobile Safari/537.36'
}

def get_body():
    url = 'http://bj.58.com'
    wb_data = requests.get(url,headers = headers)
    #print(wb_data.text)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    print(soup.prettify())
    #print(soup)
    #print(soup.find_all('span', attrs={'class': 'jumpBusiness'}))

#获取每件商品的URL
def get_links_from(who_sells):
    urls = []
    list_view = 'http://bj.58.com/pbdn/pn{}/'.format(str(who_sells))
    print('list_view:{}'.format(list_view) )
    wb_data = requests.get(list_view)
    soup = BeautifulSoup(wb_data.text,'lxml')
    #for link in soup.select('td.t > a.t'):
    for link in soup.select('td.t  a.t'):  #跟上面的方法等价
        print(link)
        urls.append(link.get('href').split('?')[0])
    return urls

#获取58同城每一类商品的url  比如平板电脑  手机 等
def get_classify_url():
    url58 = 'https://bj.58.com'
    wb_data = requests.get(url58, headers = headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    #print(soup.body)

    #for link in soup.select('div.link a'):  #span.jumpBusiness a
    for link in soup.find_all(attrs={'tongji_tag': re.compile("^pc_home_*")}):
        classify_href = link.get('href')
        classify_url = url58 + classify_href
        print(classify_url,link.string)


# 获取每件商品的具体信息
def get_item_info(who_sells=0):
    urls = get_links_from(who_sells)
    for url in urls:
        print
        url
        wb_data = requests.get(url)
        # print wb_data.text
        soup = BeautifulSoup(wb_data.text, 'lxml')
        # print soup.select('infolist > div > table > tbody > tr.article-info > td.t > span.pricebiao > span')   ##infolist > div > table > tbody > tr.article-info > td.t > span.pricebiao > span
        print
        soup.select('span[class="price_now"]')[0].text
        print
        soup.select('div[class="palce_li"]')[0].text
        # print list(soup.select('.palce_li')[0].stripped_strings) if soup.find_all('div','palce_li') else None,  #body > div > div > div > div > div.info_massege.left > div.palce_li > span > i
        data = {
            'title': soup.title.text,
            'price': soup.select('span[class="price_now"]')[0].text,
            'area': soup.select('div[class="palce_li"]')[0].text if soup.find_all('div', 'palce_li') else None,
            'date': soup.select('.look_time')[0].text,
            'cate': '个人' if who_sells == 0 else '商家',
        }
        print(data)
        result = json.dumps(data, encoding='UTF-8', ensure_ascii=False)  # 中文内容仍然无法正常显示。 使用json进行格式转换，然后打印输出。
        print
        result

if __name__ == '__main__':
    #printHelper.printStar()
    # get_item_info(url)
    # get_links_from(1)
    #get_item_info(2)
    #get_classify_url()
    get_body()