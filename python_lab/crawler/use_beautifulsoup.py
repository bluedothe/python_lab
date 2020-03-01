#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2019/11/5
    学习BeautifulSoup处理网页数据
'''

from bs4 import BeautifulSoup
import requests
import pprint
import lxml
import re
from tool import printHelper

__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2019"

def test1():
    url = 'http://www.fhdq.com'
    rsp = requests.get(url)
    if rsp.status_code == 200:
        rsp.encoding = 'utf-8'
        html = rsp.text
        soup = BeautifulSoup(html,'html.parser')
        print(soup.title)
        print(soup.body)
        printHelper.printStar(soup.body.div)
        print(soup.a)
        print(soup.find_all('a.href'))

'''标签和属性'''
def test2():
    file = open('templates/richinfo.html', 'rb')
    html = file.read()
    bs = BeautifulSoup(html, "lxml")
    print(bs.prettify())  # 缩进格式
    print(bs.title)  # 获取title标签的所有内容
    print(bs.title.name)  # 获取title标签的名称
    print(bs.title.string)  # 获取title标签的文本内容
    print(bs.head)  # 获取head标签的所有内容
    print(bs.div)  # 获取第一个div标签中的所有内容
    print(bs.div["id"])  # 获取第一个div标签的id的值
    print(bs.a)  # 获取第一个a标签中的所有内容
    print(bs.a.name)
    print(bs.a['name'])
    bs.a['name'] = 'newname'  #赋予新值
    print(bs.a.get('name'))
    del bs.a['class'] #删除某个属性
    print(bs.find_all("a"))  # 获取所有的a标签中的所有内容
    print(bs.find(id="u1"))  # 获取id="u1"
    print(bs.attrs)

    print('---')
    for item in bs.find_all("a"):  # 获取所有的a标签，并遍历打印a标签中的href的值
        print(item.get("href"))
    print('====')
    for item in bs.find_all("a"): # 获取所有的a标签，并遍历打印a标签的文本值
        print(item.get_text())
        print(item.string)


'''遍历文档树'''
def test3():
    file = open('templates/richinfo.html', 'rb')
    html = file.read()
    bs = BeautifulSoup(html, "lxml")
    print(bs.prettify())  # 缩进格式
    print(bs.head.contents)
    print(bs.head.contents[3])

    for child in bs.body.div.div.div.div.children:
        print(child)

    list1 = bs.find_all(re.compile("div")) #正则表达式
    for item in list1:
        print(item)
    print('----')
    list2 = bs.find_all(["link","div"])
    for item in list2:
        print(item)

    print('---传入方法-')
    def name_is_exists(tag):
        return tag.has_attr("name")
    list3 = bs.find_all(name_is_exists)
    for item in list3:
        print(item)

'''遍历文档树,kwargs参数'''
def test4():
    file = open('templates/richinfo.html', 'rb')
    html = file.read()
    bs = BeautifulSoup(html, "lxml")
    print(bs.prettify())  # 缩进格式
    # 查询id=head的Tag
    t_list = bs.find_all(id="head")
    print(t_list)
    # 查询href属性包含ss1.bdstatic.com的Tag
    t_list = bs.find_all(href=re.compile("http://news.baidu.com"))
    print(t_list)
    # 查询所有包含class的Tag(注意：class在Python中属于关键字，所以加_以示区别)
    t_list = bs.find_all(class_=True)
    for item in t_list:
        print(item)


'''遍历文档树,attrs参数'''
def test5():
    file = open('templates/richinfo.html', 'rb')
    html = file.read()
    bs = BeautifulSoup(html, "lxml")
    #print(bs.prettify())  # 缩进格式
    t_list = bs.find_all(class_="head_wrapper")
    print(t_list)

    t_list = bs.find_all(attrs={"name": "tj_trnews"}) #t_list = bs.find_all(name="tj_trnews"),注释的这条语句不能取到值
    for item in t_list:
        print(item)


'''遍历文档树,text参数'''
'''通过text参数可以搜索文档中的字符串内容，与name参数的可选值一样，text参数接受 字符串，正则表达式，列表'''
def test6():
    file = open('templates/richinfo.html', 'rb')
    html = file.read()
    bs = BeautifulSoup(html, "html.parser")
    #print(bs.prettify())  # 缩进格式
    t_list1 = bs.find_all(attrs={"name": "tj_trnews"}) #取不到值，为什么
    for item in t_list1:
        print(item)
    print('==1==')
    t_list2 = bs.find_all(text="hao123") #取不到值，为什么
    for item in t_list2:
        print(item)
    print('==2==')
    t_list3 = bs.find_all(text=["hao123", "地图", "贴吧"]) #取不到值，为什么
    for item in t_list3:
        print(item)
    print('==3==')
    t_list = bs.find_all(text=re.compile("\d"))
    for item in t_list:
        print(item)
    print('==4==')
    t_list = bs.find_all(string='123') #取不到值，为什么
    for item in t_list:
        print(item)
    print('==5==')
    t_list = bs.find_all('a',class_="bri")
    for item in t_list:
        print(item)
    print('==6==')
    #传入方法
    def length_is_two(text):
        return text and len(text) == 2
    t_list = bs.find_all(text=length_is_two)
    for item in t_list:
        print(item)

'''简写'''
def test7():
    file = open('templates/richinfo.html', 'rb')
    html = file.read()
    bs = BeautifulSoup(html, "html.parser")
    # print(bs.prettify())  # 缩进格式
    t_list = bs("a")  # t_list = bs.find_all("a") => t_list = bs("a")  两者是相等
    for item in t_list:
        print(item)
    t_list = bs.a(text="新闻")  # t_list = bs.a.find_all(text="新闻") => t_list = bs.a(text="新闻") 两者是相等
    for item in t_list:
        print(item)

    print(bs.html.head.title)
    print(bs.body.div.div.div.div)
    t_list = bs.body.children
    for item in t_list:
        print(item)

'''CSS选择器'''
def test8():
    file = open('templates/richinfo.html', 'r', encoding='utf-8')
    html = file.read()
    bs = BeautifulSoup(html, "html.parser")
    # print(bs.prettify())  # 缩进格式
    print(bs.select('title'))  #通过标签名查找
    print(bs.select('a'))  #通过标签名查找
    print(bs.select('.mnav'))  #通过类名查找
    print(bs.select('#u1'))  #通过id查找
    print(bs.select('div .bri'))  #组合查找
    print(bs.select('a[class="bri"]'))  #属性查找
    print(bs.select('a[href="http://tieba.baidu.com"]'))  #属性查找
    t_list = bs.select("head > title")  #直接子标签查找
    print(t_list)
    t_list = bs.select(".mnav ~ .bri")  #兄弟节点标签查找
    print(t_list)
    t_list = bs.select("title")  #获取内容
    print(bs.select('title')[0].get_text())


if __name__ == '__main__':
    test1()