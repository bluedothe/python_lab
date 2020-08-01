#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/7/26
    爬取同花顺行情中心股票信息
    参考资料：https://blog.csdn.net/weixin_44510363/article/details/105408092?utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~all~first_rank_v2~rank_v25-2-105408092.nonecase
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import requests
import time
import random
import json
from bs4 import BeautifulSoup
import pandas as pd


class Tonghuashun:
    """采集同花顺股票信息作业实例"""

    def __init__(self):
        self.page_id = ''
        self.headers = {
            'Host': 'q.10jqka.com.cn',
            'Referer': 'http://q.10jqka.com.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        # 定义代理字典
        self.proxy = [
            {'http://': '113.194.30.241:9999'},
            {'https://': '113.194.30.241:9999'},
            {'http://': '122.4.50.55:9999'},
            {'http:s//': '122.4.50.55:9999'},
            {'http://': '120.83.97.234:9999'},
            {'http:s//': '120.83.97.234:9999'},
            {'http://': '183.166.102.204:9999'},
            {'https://': '112.85.150.220:9999'},
            {'http://': '163.204.242.99:9999'},
            {'http://': '123.54.40.102:9999'},
            {'https://': '123.54.40.102:9999'}
        ]
        # self.run()

    def get_html_list(self, url):
        """请求服务器，获取源代码函数"""
        # 请求响应
        response = requests.get(url, headers=self.headers,
                                proxies=random.choice(self.proxy))
        # 选择'gbk'码显示中文
        response.encoding = 'gbk'
        return response.text

    def get_stock_details(self, url):
        """获取个股详情"""
        response = requests.get(url, headers=self.headers, proxies=random.choice(self.proxy))
        # 选择'gbk'码显示中文
        response.encoding = 'gbk'
        # 返回的是JSON格式数据
        json_str = response.text
        json_str = json_str[json_str.find('{'):-1]
        data_json = json.loads(json_str)
        # print(data_json)
        stock_details = {
            '今开价': data_json['items']['7'],
            '成交量': str(round(float(data_json['items']['13'])/10000,2))+'万',
            '最高价': data_json['items']['8'],
            '最低价': data_json['items']['9'],
            '昨收价': data_json['items']['6'],
            '总市值': str(round(float(data_json['items']['3541450'])/100000000,2))+'亿',
            '市净率': data_json['items']['592920']
        }
        # print(stock_details)
        return stock_details

    def get_data(self, text):
        """解析网页，按需抽取股票数据函数"""
        soup = BeautifulSoup(text, 'lxml')
        trs = soup.find_all('tr')[1:]  # 第一个ul不是想要的内容，从第2个开始
        stock_infos = []
        for tr in trs:
            # print(tr)
            stock_dict = {}
            tds = tr.find_all('td')  # 获取td标签所有文本内容
            # print(tds)
            a_href = tr.find('a')   # 获取包含个股详情a标签
            # 动态网页获取数据失败，此url不是真实地址
            # print(a_href['href'])
            # 经分析，以下为真实地址
            url = f'http://d.10jqka.com.cn/v2/realhead/hs_{tds[1].get_text()}/last.js'
            info = self.get_stock_details(url)

            # 将股票信息写入字典
            stock_dict['股票代码'] = tds[1].get_text()
            stock_dict['股票名称'] = tds[2].get_text()
            stock_dict['现价'] = tds[3].get_text()
            stock_dict['今开价'] = info['今开价']
            stock_dict['最高价'] = info['最高价']
            stock_dict['最低价'] = info['最低价']
            stock_dict['昨收价'] = info['昨收价']
            stock_dict['涨跌幅'] = tds[4].get_text()
            stock_dict['涨跌额'] = tds[5].get_text()
            stock_dict['涨速'] = tds[6].get_text()
            stock_dict['换手'] = tds[7].get_text()
            stock_dict['量比'] = tds[8].get_text()
            stock_dict['振幅'] = tds[9].get_text()
            stock_dict['成交额'] = tds[10].get_text()
            stock_dict['成交量'] = info['成交量']
            stock_dict['市净率'] = info['市净率']
            stock_dict['流通股'] = tds[11].get_text()
            stock_dict['流通市值'] = tds[12].get_text()
            stock_dict['总市值'] = info['总市值']
            stock_dict['市盈率'] = tds[13].get_text()
            stock_dict['个股链接'] = a_href['href']

            stock_infos.append(stock_dict)  # 将字典写入列表中
            # print(stock_infos)
        # 每一页都保存一次数据
        self.save_data(stock_infos)

    def save_data(self, stock_infos):
        """保存股票数据到本地函数"""
        stock_json = json.dumps(stock_infos)    # 使用json格式不用每次都写入表头
        with open('webscraping/requests_learn/tonghushun.json', 'w') as f:
            f.write(stock_json)
        with open('webscraping/requests_learn/tonghushun.json', 'r') as f:
            stock_data = f.read()
        stock_data = json.loads(stock_data)
        # 定义表头
        cols_list = [
            '股票代码', '股票名称', '现价', '今开价', '最高价', '最低价', '昨收价', '涨跌幅', '涨跌额', '涨速', '换手', '量比', '振幅', '成交额', '成交量', '市净率','流通股', '流通市值', '总市值', '市盈率', '个股链接'
        ]
        # 使用pandas保存到excel文件
        df_stock = pd.DataFrame(stock_data, columns=cols_list)
        df_stock.to_csv('webscraping/requests_learn/tonghushun.csv', mode='a')
        # print(df_stock)

    def run(self):
        """主运行函数"""
        print('开始采集股票数据，祝好运！')
        for i in range(1, 189):
            self.page_id = str(i)    # 设置页码
            url = f'http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/{self.page_id}/ajax/1/'
            text = self.get_html_list(url)
            self.get_data(text)
            print('', end='')
            time.sleep(random.randint(1, 10))  # 设置1-10秒睡眠
            print('\r'+'数据采集完成进度-->%.2f%%' % (i/188*100), end='')
        print('\n已成功收集所需股票数据，恭喜发财！！！')


if __name__ == "__main__":
    """测试代码"""
    myApp = Tonghuashun()
    myApp.run()
