#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/2/28
    爬取ip代理
    教程地址：https://blog.csdn.net/xy229935/article/details/88814979?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task
    爬取地址：http://www.66ip.cn
'''

import os
import requests
from bs4 import BeautifulSoup
import time
import random

def getIP():
    heads = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    url_master = "http://www.66ip.cn"
    for i in range(1, 2):
        url = url_master + "/" + str(i) + ".html"
        response = requests.get(url, headers=heads)
        soup = BeautifulSoup(response.content.decode("gbk"), "lxml")
        # 找到属性"bordercolor"为"#6699ff"的table中的所有tr
        trs = soup.find("table", attrs={"bordercolor": "#6699ff"}).find_all("tr")
        for tr in trs[1:]:
            ip = tr.find_all("td")[0].get_text()
            port = tr.find_all("td")[1].get_text()
            proxy = "http://" + ip + ":" + port
            print(proxy)
            # 验证代理IP是否可用，如果IP不可用会抛异常
            try:
                proxies = {"http": proxy}
                test_url = "http://blog.csdn.net"
                rsp = requests.get(test_url, headers=heads, proxies=proxies, timeout=3)
                print("check: " + proxy)
                if (response.status_code == 200):
                    # 如果可用则保存地址
                    with open(os.getcwd() + "/file_down/" + "ipList.txt", "a", encoding="utf-8") as f:
                        f.write(proxy + "\n")
                        f.close()
                    print("use: " + proxy)
                else:
                    print("no use: " + proxy)
            except Exception as e:
                print("except: " + proxy)
                print(str(e))
                print(repr(e))
                print(e.args)
            # 验证结束
        # 间隔时间为3~5秒
        time.sleep(random.randint(3, 5))




if __name__ == '__main__':
    getIP()