#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2019/11/3
    爬取符号大全网站的内容
'''

import requests
import re
import os

__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2019"

'save text'
def crawler_test1():
    url = 'http://www.fhdq.net/' #符合大全
    req = requests.get(url)
    req.encoding = 'utf-8'  #如果遇到中文乱码可以通过这里重新指定编码
    html = req.text
    print('status_code: ', req.status_code)
    print('status_ok: ', req.ok)
    print('encoding: ', req.encoding)
    print('url: ', req.url)
    print(html)

    with open(os.getcwd() + "/file_down/" + 'fhdq1.html', 'w', encoding="utf-8") as f:
        f.write(html)

'save content'
def crawler_test2():
    url = 'http://www.fhdq.net/' #符合大全
    req = requests.get(url)
    req.encoding = 'utf-8'  #如果遇到中文乱码可以通过这里重新指定编码
    html = req.content
    print('status_code: ', req.status_code)
    print('status_ok: ', req.ok)
    print('encoding: ', req.encoding)
    print('url: ', req.url)
    print(html)

    with open(os.getcwd() + "/file_down/" + 'fhdq2.html', 'wb') as f:
        f.write(html)

'save content'
def crawler_test3():
    url = 'http://www.fhdq.net/' #符合大全
    req = requests.get(url)
    req.encoding = 'utf-8'  #如果遇到中文乱码可以通过这里重新指定编码
    html = req.content
    print('status_code: ', req.status_code)
    print('status_ok: ', req.ok)
    print('encoding: ', req.encoding)
    print('url: ', req.url)
    print(html)

    html_doc = str(html, 'utf-8')  # html_doc=html.decode("utf-8","ignore")
    # print(html_doc)
    with open(os.getcwd() + "/file_down/" + 'fhdq3.html', 'w', encoding="utf-8") as f:
        f.write(html_doc)

'save content and pic'
'以上的方法虽然不会出现乱码，但是保存下来的网页，图片不显示，只显示文本。而且打开速度慢，找到了一篇博客，提出了一个终极方法，非常棒'
def crawler_test4():
    url = 'http://www.fhdq.net/' #符合大全
    req = requests.get(url)

    print('status_code: ', req.status_code)
    print('status_ok: ', req.ok)
    print('encoding: ', req.encoding)
    print('url: ', req.url)
    print(req.content)

    if req.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(req.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = req.apparent_encoding

        # encode_content = req.content.decode(encoding, 'replace').encode('utf-8', 'replace')
        global encode_content
        encode_content = req.content.decode(encoding, 'replace')  # 如果设置为replace，则会用?取代非法字符；

    print(encode_content)

    with open(os.getcwd() + "/file_down/" + 'fhdq4.html', 'w', encoding='utf-8') as f:
        f.write(encode_content)

'extra_text'
def extra_text():
    url = 'http://www.fhdq.net/'  # 符合大全
    req = requests.get(url)
    if req.status_code == 200:
        req.encoding = 'utf-8'  # 如果遇到中文乱码可以通过这里重新指定编码
        html = req.text
        pattern = re.compile(r'<li><a href="(.*?)" target="_blank">(.*?)</a>')
        results = pattern.findall(html)
        print(results)
        with open(os.getcwd() + "/file_down/" + 'fhdq5.txt', 'w' ,encoding='utf-8') as f:
            for result in results:
                f.write(f'{url}{result[0][1:]}  {result[1]}\n')

if __name__ == '__main__':
    extra_text()