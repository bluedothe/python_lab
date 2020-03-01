#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/2/6
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

from bs4 import BeautifulSoup
import requests
import re

def getSong():
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
    }
    url='https://songsearch.kugou.com/song_search_v2?&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1555124510574'
    url = "https://www.kugou.com/song/#hash=15568CF4D9DB1FAF260CF3A965017CD8&album_id=511051"
    #想要爬取别的网页直接修改这个json数据地址就行
    r=requests.get(url,headers=headers)
    soup=BeautifulSoup(r.text,'lxml')
    title_list=soup.select('.pc_temp_songlist ul li')
    hash=re.findall(r',"FileHash":"(.*?)"',r.text)
    hash1=re.findall(r',"FileName":"(.*?)"',r.text)
    #直接用正则匹配隐藏的数据
    print(hash)
    print(hash1)
    q=0
    for url in hash:
        url_a=f'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery1910212680783679835_1555073815772&hash={url}&album_id=18784389'
        #这个URL不用修改的
        c=requests.get(url_a,headers=headers)
        a=c.text[40:-3]
        b=re.findall('"play_url":"(.*)","authors":',a)[0]
        b1=re.sub(r"\\",'',b)
        f = requests.get(b1)
        with open(hash1[q]+'.mp3','wb')as d:
            d.write(f.content)
            print(hash1[q])
            q+=1

if __name__ == '__main__':
    getSong()