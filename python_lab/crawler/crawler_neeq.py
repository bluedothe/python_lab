#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/3/8
    爬取动态网站内容：需要分析请求的类型（post/get)、请求头信息、cookie、请求地址、请求参数、返回数据类型、返回数据结构
    教程地址：https://blog.csdn.net/guanmaoning/article/details/80158554
    案例地址：http://www.neeq.com.cn/disclosure/supervise.html
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import requests
import random
import json

# =============================================================================
# 应对网站反爬虫的相关设置
# =============================================================================
# User-Agent列表，这个可以自己在网上搜到，用于伪装浏览器的User Agent
USER_AGENTS = [
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1"
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12 "
]
# IP地址列表，用于设置IP代理
IP_AGENTS = [
    "http://58.240.53.196:8080",
    "http://219.135.99.185:8088",
    "http://117.127.0.198:8080",
    "http://58.240.53.194:8080"
]

# 设置IP代理
proxies = {"http": random.choice(IP_AGENTS)}

# =============================================================================
# 上面的设置是为了应对网站的反爬虫，与具体的网页爬取无关
# =============================================================================

# =============================================================================
# 下面这些是根据刚才第一步的分析来设置的，所以下面需要按照第一步的分析来设置对应的参数。
# 根据第一步图片的右下角部分来设置Cookie、url、headers和post参数
# =============================================================================
# 设置cookie
Cookie = "Hm_lvt_b58fe8237d8d72ce286e1dbd2fc8308c=1525162758; BIGipServerNEEQ_8000-NEW=83952564.16415.0000; JSESSIONID=E50D2B8270D728502754D4330CB0E275; Hm_lpvt_b58fe8237d8d72ce286e1dbd2fc8308c=1525165761"
# 设置动态js的url
url = 'http://www.neeq.com.cn/disclosureInfoController/infoResult.do?callback=jQuery'
# 设置requests请求的 headers
headers = {
    'User-agent': random.choice(USER_AGENTS),  # 设置get请求的User-Agent，用于伪装浏览器UA
    'Cookie': Cookie,
    'Connection': 'keep-alive',
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Host': 'www.neeq.com.cn',
    'Referer': 'http://www.neeq.com.cn/disclosure/supervise.html'
}
# 设置页面索引
pageIndex = 0
# 设置url post请求的参数
data = {
    'page': pageIndex,
    'disclosureType': 8
}

def getData():
    # requests post请求
    #req = requests.post(url, data=data, headers=headers, proxies=proxies)
    req = requests.post(url, data=data, headers=headers)   #不使用ip代理
    # print(req.content) #通过打印req.content，我们可以知道post请求返回的是json数据，而且该数据是一个字符串类型的
    # 获取包含json数据的字符串
    str_data = req.content
    print(str_data)
    # 获取json字符串数据
    str_json = str_data[8:-2]
    # print(str_json)
    # 把json数据转成dict类型
    json_Info = json.loads(str_json)
    print(type(json_Info))
    company_info = json_Info["listInfo"]["content"]
    print(company_info)
    print(len(company_info))
    for item in company_info:
        print(item["companyCd"],item["companyName"],item["disclosureTitle"])


if __name__ == '__main__':
    getData()