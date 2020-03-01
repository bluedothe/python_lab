#!/usr/bin/python3
# -*- coding: utf-8 -*-

from requests_html import HTMLSession
import urllib.request,os,json
from urllib.parse import quote
from tool import printHelper
from fake_useragent import UserAgent

'''
    module description
    date: 2020/2/8
    下载酷狗音乐歌曲
'''

__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

headers2 = {
        "Cookie": "kg_mid=3786e26250f01bf2c64bc515820d9752; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1559960644; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1559960644; ACK_SERVER_10015=%7B%22list%22%3A%5B%5B%22bjlogin-user.kugou.com%22%5D%5D%7D; ACK_SERVER_10016=%7B%22list%22%3A%5B%5B%22bjreg-user.kugou.com%22%5D%5D%7D; ACK_SERVER_10017=%7B%22list%22%3A%5B%5B%22bjverifycode.service.kugou.com%22%5D%5D%7D; kg_dfid=0iEqIA1uep0h0AogH30Jq1Od; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e",
        "Host": "www.kugou.com",
        "Referer": "http://www.kugou.com/",
        "UserAgent": str(UserAgent(verify_ssl=False).random)
    }

class KuGou():
    def __init__(self):
        self.get_music_url='https://songsearch.kugou.com/song_search_v2?keyword={}&platform=WebFilter'
        self.get_song_url='https://www.kugou.com/yy/index.php?r=play/getdata&hash={}'
        if not os.path.exists("d:/music"):
            os.mkdir('d:/music')

    def parse_url(self,url):
        session = HTMLSession()
        response = session.get(url)
        print(printHelper.get_cur_info(), url)
        print(printHelper.get_cur_info(),response.html.html)
        return response.content.decode()

    def parse_url2(self,url):
        session = HTMLSession()
        response = session.get(url,headers = headers2)
        print(printHelper.get_cur_info(), url)
        print(printHelper.get_cur_info(),response.html.html)
        return response.content.decode()

    def get_music_list(self,keyword):
        music_dirt=json.loads(self.parse_url(self.get_music_url.format(quote(keyword))))
        music_list=music_dirt['data']['lists']
        song_list=[]
        for music in music_list:
            song_name=music['FileName'].replace("<\\/em>", "").replace("<em>", "")
            song_list.append({'hash':music['FileHash'], 'song_name':song_name})
            print(str(len(song_list))+'---'+song_name)
        return song_list

    def download(self,song):
        print(printHelper.get_cur_info(),self.parse_url(self.get_song_url.format(song['hash'])))
        song_dirt=json.loads(self.parse_url2(self.get_song_url.format(song['hash'])))
        #print(song_dirt)
        download_url=song_dirt['data']['play_url']
        if download_url:
            try:
                # 根据音乐url地址，用urllib.request.retrieve直接将远程数据下载到本地
                urllib.request.urlretrieve(download_url, os.getcwd() + "/music_down/" + song['song_name'] + '.mp3')
                print('Successfully Download:' + song['song_name'] + '.mp3')
            except:
                print('Download wrong~')
        else:
                print('no Download wrong~')

if __name__ == '__main__':
    kugou=KuGou()
    #while True:
    #keyword=input('请输入要下载的歌曲名：')
    keyword = "王菲-我和我的祖国"
    print('-----------歌曲《'+keyword+'》的版本列表------------')
    music_list=kugou.get_music_list(keyword)
    #song_num=input('请输入要下载的歌曲序号：')
    song_num = 1
    kugou.download(music_list[int(song_num)-1])
