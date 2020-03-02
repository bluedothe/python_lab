#!/usr/bin/python3
# -*- coding: utf-8 -*-

from requests_html import HTMLSession,HTML
from crawler import html_example_file
from pprint import pprint
import json
import io
import os

'''
    module description
    date: 2020/2/9
    从天涯论坛爬取帖子
    教程地址：https://blog.csdn.net/u011054333/article/details/81055423
    案例网址：http://bbs.tianya.cn/list-stocks-1.shtml
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

# 爬取天涯论坛帖子
def get_data(url):
    session = HTMLSession()
    #url = 'http://bbs.tianya.cn/post-stocks-860147-1.shtml'
    r = session.get(url)
    # 楼主名字
    author = r.html.find('div.atl-info span a', first=True).text
    # 总页数
    div = r.html.find('div.atl-pages', first=True)
    links = div.find('a')
    total_page = 1 if links == [] else int(links[-2].text)
    # 标题
    title = r.html.find('span.s_title span', first=True).text

    with io.open(os.getcwd() + "/file_down/" + f'{title}.txt', 'x', encoding='utf-8') as f:
        for i in range(1, total_page + 1):
            s = url.rfind('-')
            r = session.get(url[:s + 1] + str(i) + '.shtml')
            # 从剩下的里面找楼主的帖子
            items = r.html.find(f'div.atl-item[_host={author}]')
            for item in items:
                content: str = item.find('div.bbs-content', first=True).text
                # 去掉回复
                if not content.startswith('@'):
                    f.write(content + "\n")
    print('=======下载结束=========')

if __name__ == '__main__':
    url = "http://bbs.tianya.cn/post-stocks-2163387-1.shtml"  #[股市论谈]大户日记&SNIPER超级证券博弈系统实战分享&账户诊断
    url = "http://bbs.tianya.cn/post-stocks-2168836-1.shtml"  #	萧九成:将低吸进行到底【3月号】
    url = "http://bbs.tianya.cn/post-stocks-2168664-3.shtml"   #走过山丘2019:股市菜鸟炒越秀金控续一
    url = "http://bbs.tianya.cn/post-stocks-2168053-1.shtml"   #年鱼溪:机构内参操盘计划 每日开盘前奉送一股 今买明卖 买入必涨
    get_data(url)