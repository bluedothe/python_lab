#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from urllib.request import urlopen as open
from bs4 import BeautifulSoup
import re
import pymysql

'''
    module description
    date: 2020/2/4
    爬取名言网的top10标签内容
    教程来源：https://www.jb51.net/article/170013.htm
    目标网址：http://quotes.toscrape.com
'''

__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

url = "http://quotes.toscrape.com"

def find_top_ten(url):
    response = open(url)
    bs = BeautifulSoup(response,'html.parser')
    tags = bs.select('span.tag-item a')
    top_ten_href = [tag.get('href') for tag in tags]
    top_ten_tag = [tag.text for tag in tags]
    #print(top_ten_href)
    #print(top_ten_tag)
    return top_ten_href

def insert_into_mysql(records):
    con = pymysql.connect(host='localhost',user='root',password='root',database='quotes',charset='utf8',port=3306)
    cursor = con.cursor()
    sql = "insert into quotes(content,author,tags) values(%s,%s,%s)"
    for record in records:
        cursor.execute(sql, record)
        con.commit()
        cursor.close()
        con.close()

# http://quotes.toscrape.com/tag/love/
#要获取对应标签中所有的名言 所以这里要考虑分页的情况
#经过在网页上查看知道分页查询的url
#http://quotes.toscrape.com/tag/love/page/1/
#判断到那一页没有数据 div.container div.row [1]
def find_link_content(link):
    page = 1
    while True:
        new_link = "http://quotes.toscrape.com" + link + "page/"
        # print(new_link)
        new_link = new_link + str(page)
        print(new_link)
        sub_bs = open(new_link)
        sub_bs = BeautifulSoup(sub_bs,'html.parser')
        quotes = sub_bs.select('div.row div.col-md-8 span.text')
        # 如果没有数据就退出
        if len(quotes) == 0:
            break
        #名言
        quotes = [quote.text.strip('“”') for quote in quotes]
        #作者
        authors = sub_bs.select('small.author')
        authors = [author.text for author in authors]
        # 标签
        tags_list = sub_bs.select('meta.keywords')
        tags_list = [tags.get('content') for tags in tags_list]
        # print(authors)
        # print(quotes)
        #print(tags_list)
        record_list = []
        for i in range(len(quotes)):
            tags = tags_list[i]
            tags = tags.replace(',','，')
            print(tags)
            record = [quotes[i],authors[i],tags]
            record_list.append(record)
        insert_into_mysql(record_list)
        page += 1
#
def main():
    url = "http://quotes.toscrape.com/"
    parent_link = find_top_ten(url)
    for link in parent_link:
        print(link)
        find_link_content(link)

def test():
    req = requests.get("http://quotes.toscrape.com/")
    soup = BeautifulSoup(req.text,"lxml")
    for item in soup.select("span.tag-item a"):
        print(item.get('href'), item.text)
    req = requests.get("http://quotes.toscrape.com/tag/love")
    soup = BeautifulSoup(req.text, "lxml")
    for item in soup.select('div.row div.col-md-8 span.text'):
        print( item.text.strip('“”'))

if __name__ == '__main__':
    test()
    #find_top_ten(url)