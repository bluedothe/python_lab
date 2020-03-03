#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/3/3
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import urllib
import requests
from bs4 import BeautifulSoup
import time
import random
from db.mysqlHelper import mysqlHelper
import threading

host = "localhost"
username = "root"
password = "root123"
dbname = "kdata"
DBHelper = mysqlHelper(host,username,password,dbname)

heads = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

def downIP(startPage, endPage):
    for i in range(startPage, endPage):
        #####################################################################################################
        # 爬66ip网的免费代理IP
        url = "http://www.66ip.cn/" + str(i) + ".html"
        response = requests.get(url, headers=heads)
        soup = BeautifulSoup(response.content.decode("gbk"), "lxml")
        # 找到属性"bordercolor"为"#6699ff"的table中的所有tr
        trs = soup.find("table", attrs={"bordercolor": "#6699ff"}).find_all("tr")
        for tr in trs[1:]:
            address = tr.find_all("td")[2].get_text().strip()
            if ("市" in address):
                ip = tr.find_all("td")[0].get_text().strip()
                port = tr.find_all("td")[1].get_text().strip()
                proxy = "http://" + ip + ":" + port
                # print(proxy+"  "+address)
                if len(DBHelper.select("select * from iptbl where ipurl='" + proxy + "'")) == 0:
                    DBHelper.exec("insert into iptbl(ipurl) values('" + proxy + "')");
        #####################################################################################################
        # 爬快代理网的免费代理IP
        url = "https://www.kuaidaili.com/free/inha/" + str(i) + "/"
        response = requests.get(url, headers=heads)
        soup = BeautifulSoup(response.content.decode("utf-8"), "lxml")
        # 找到属性"class"为"table table-bordered table-striped"的table中的所有tr
        trs = soup.find("table", attrs={"class": "table table-bordered table-striped"}).find_all("tr")
        for tr in trs[1:]:
            address = tr.find_all("td")[4].get_text().strip()
            if ("市" in address):
                ip = tr.find_all("td")[0].get_text().strip()
                port = tr.find_all("td")[1].get_text().strip()
                proxy = "http://" + ip + ":" + port
                # print("快代理："+proxy+"  "+address)
                if len(DBHelper.select("select * from iptbl where ipurl='" + proxy + "'")) == 0:
                    DBHelper.exec("insert into iptbl(ipurl) values('" + proxy + "')");
        #####################################################################################################
        # 爬快89ip网的免费代理IP
        url = "http://www.89ip.cn/index_" + str(i) + ".html"
        response = requests.get(url, headers=heads)
        soup = BeautifulSoup(response.content.decode("utf-8"), "lxml")
        # 找到属性"class"为"layui-table"的table中的所有tr
        trs = soup.find("table", attrs={"class": "layui-table"}).find_all("tr")
        for tr in trs[1:]:
            address = tr.find_all("td")[2].get_text().strip()
            if ("市" in address):
                ip = tr.find_all("td")[0].get_text().strip()
                port = tr.find_all("td")[1].get_text().strip()
                proxy = "http://" + ip + ":" + port
                # print("89ip："+ proxy+"  "+address)
                if len(DBHelper.select("select * from iptbl where ipurl='" + proxy + "'")) == 0:
                    DBHelper.exec("insert into iptbl(ipurl) values('" + proxy + "')");

        #####################################################################################################
        # 爬快西刺网的免费代理IP
        url = "https://www.xicidaili.com/nn/" + str(i)
        response = requests.get(url, headers=heads)
        soup = BeautifulSoup(response.content.decode("utf-8"), "lxml")
        # 找到属性"id"为"ip_list"的table中的所有tr
        trs = soup.find("table", attrs={"id": "ip_list"}).find_all("tr")
        for tr in trs[1:]:
            address = tr.find_all("td")[3].get_text().strip()
            # if ("市" in address):
            ip = tr.find_all("td")[1].get_text().strip()
            port = tr.find_all("td")[2].get_text().strip()
            proxy = "http://" + ip + ":" + port
            # print("西刺ip：" + proxy + "  " + address)
            if len(DBHelper.select("select * from iptbl where ipurl='" + proxy + "'")) == 0:
                DBHelper.exec("insert into iptbl(ipurl) values('" + proxy + "')");
        #####################################################################################################
        # 间隔时间为3~5秒
        time.sleep(random.randint(3, 5))


def valiIP(x):
    # 每次验证10条记录
    result = DBHelper.select("select ipurl from iptbl where state=0 limit " + str(x) + ",1")
    for row in result:
        proxy = row[0]
        # 验证代理IP是否可用，如果IP不可用会抛异常
        try:
            proxies = {"http": proxy}
            urlList = ["http://www.qq.com", "http://www.jd.com", "http://www.baidu.com", "http://www.csdn.net",
                       "http://www.qidian.com", "http://www.51cto.com"]
            tmpUrl = random.choice(urlList)
            rsp = requests.get(tmpUrl, headers=heads, proxies=proxies, timeout=3)
            # 如果不可用则删除
            if (rsp.status_code != 200):
                sql = "delete from iptbl where ipurl='" + proxy + "'"
                DBHelper.exec(sql)
                print("删除了" + proxy)
            else:
                sql = "update iptbl set state=1 where ipurl='" + proxy + "'"
                DBHelper.exec(sql)
                print(proxy + "可用")
        except Exception as e:
            sql = "delete from iptbl where ipurl='" + proxy + "'"
            DBHelper.exec(sql)
            print("删除了" + proxy)
            pass
        # 验证结束

def create_table():
    sql = "drop table if exists iptbl;"
    DBHelper.exec(sql)
    sql = """
    create table iptbl
(
   id                   bigint not null auto_increment,
   ipurl           varchar(32),
   state           integer(2) default  0 comment '0未校验；1已校验通过', 
   primary key (id)
);
    """
    DBHelper.exec(sql)
    print("建表完成")

def test_mysql():
    result = DBHelper.select("select * from t_kdata")
    for row in result:
        field_value = row[1]
        print(field_value)

def run_thread():
    # 下载IP
    t1 = threading.Thread(target=downIP, args=[1, 100])
    t1.start()
    x = 0
    while True:
        # 验证IP
        t2 = threading.Thread(target=valiIP, args=[x])
        t2.start()
        x += 1
        if x > 1000:
            x = 0
        time.sleep(0.2)

if __name__ == "__main__":
    #create_table()
    #test_mysql()
    run_thread()
