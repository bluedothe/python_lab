#!/usr/bin/python3
# -*- coding: utf-8 -*-

from requests_html import HTMLSession,HTML
from crawler import html_example_file
from pprint import pprint
import json
import pyppeteer.chromium_downloader

'''
    module description
    date: 2020/2/9
    requests库的作者又发布了一个新库，叫做requests-html，看名字也能猜出来，这是一个解析HTML的库
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

html = HTML(html=html_example_file.html_doc)

def test_css_selector():
    print(html.html)
    print(html.links)   #获取全部a标签的href属性值
    print(html.absolute_links)   #获取所有的路径都会转成绝对路径返回
    print(html.find('div#nav_menu', first=True).text)  #获取文本
    print(html.find('div#nav_menu a'))    #获取元素
    print(html.find('div#nav_menu a',first=True).attrs)  #获取属性
    print(html.find('div.post_item_body p.post_item_summary a img',first=True).attrs['src'])
    print(list(map(lambda x: x.text, html.find('div.cate-scroller span.cate-desc'))))
    print(html.search("蜗{}宋")[0])
    print(html.search_all("蜗{}宋")[0])

def test_xpath():
    print(html.xpath("//div[@id='nav_menu']", first=True).text)
    print(html.xpath("//div[@id='nav_menu']/a"))
    print(html.xpath("//div[@id='nav_menu']/a",first=True).attrs)
    print(html.xpath("//div[@id='nav_menu']/a", first=True).html)
    print(html.xpath("//div[@class='cate-scroller']/span[@class='cate-desc']"))

def test_ua():
    session = HTMLSession()
    r = session.get('http://httpbin.org/get')
    pprint(json.loads(r.html.html))
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
    r = session.get('http://httpbin.org/get', headers={'user-agent': ua})
    pprint(json.loads(r.html.html))

def test_login():
    session = HTMLSession()
    r = session.post('http://httpbin.org/post', data={'username': 'yitian', 'passwd': 123456})
    pprint(json.loads(r.html.html))

def test_render():
    session = HTMLSession()
    response = session.get('http://python-requests.org/')
    response.html.render()    # 动态渲染页面
    print(response.html.html)  # 输出渲染之后的页面


def test_render_js():
    session = HTMLSession()
    response = session.get('https://www.baidu.com')
    script = '''
    ()=>{
    Object.defineProperties(navigator,{
            webdriver:{
            get: () => undefined
            }
        })}'''
    print(response.html.render(script=script))


def test():
    print('默认版本是：{}'.format(pyppeteer.__chromium_revision__))
    print('可执行文件默认路径：{}'.format(pyppeteer.chromium_downloader.chromiumExecutable.get('win64')))
    print('win64平台下载链接为：{}'.format(pyppeteer.chromium_downloader.downloadURLs.get('win64')))

if __name__ == '__main__':
    #test()
    #test_css_selector()
    #test_xpath()
    #test_ua()
    #test_login()
    test_render()
    #test_render_js()