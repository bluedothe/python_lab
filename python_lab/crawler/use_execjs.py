#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/7/11
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import execjs
import requests

#没有调试通过，未完成
def get_baidu_phon(word):
    url = 'https://fanyi.baidu.com/v2transapi'
    headers={
        u'Cookie':u'BAIDUID=EDB5DF3F6B45AB4D135EE53B6713B986:FG=1; BIDUPSID=EDB5DF3F6B45AB4D135EE53B6713B986; PSTM=1573902206; BDUSS=g2M2JiS2xYbzJCN2daNDZ1UWlnSHNSOS10aEhQWndYR1ZWUHRWNXdwZXpJd0plRVFBQUFBJCQAAAAAAAAAAAEAAADlZq8KYmx1ZWRvdGhlAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALOW2l2zltpdd1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; PSINO=2; H_PS_PSSID=32190_1450_32139_32045_32230_32295_31640; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1594454121; Hm_lvt_246a5e7d3670cfba258184e42d902b31=1594454126; Hm_lpvt_246a5e7d3670cfba258184e42d902b31=1594454126; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1594455207; __yjsv5_shitong=1.0_7_89064e487c75b0ca7319b5ef602b707ec332_300_1594455199953_123.116.60.238_d874825c; yjs_js_security_passport=3d7d8ec5b93e9e104a3edbc81c3f844a5ffbb265_1594455201_js',
        u'User-Agent':u'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    }
    postdata={
        u'from':u'en',
        u'to':u'zh',
        u'query':str(word),
        u'transtype':u'translang',
        u'simple_means_flag':u'',
        u'sign':u'109802.348123',
        u'token':u'46a978ccdb52aef6171ebea3e776f192'
    }
    response = requests.post(url,headers=headers,data=postdata,timeout=60)
    response.encoding='utf-8'

    print(response)
    print(response.content.decode('unicode_escape'))  # 中文转码

    content = response.text

def test1():
    # 方法一：通过eval直接执行js脚本
    e = execjs.eval('a = new Array(1,2,3)')  # 可以直接执行JS代码
    print(e)
    #方法二：通过complie加载js脚本，构建一个JS的环境
    x = execjs.compile('''
            function add(x,y){
                return x+y;
                };
            ''')
    print(x.call('add', '1', '2'))  # execjs.compile用于执行更复杂的js代码
    #方法三：加载js文件
    filename = 'templates/test.js'
    with open(filename) as f:
        jsdata = f.read()
    ctx = execjs.compile(jsdata)
    #ctx = execjs.compile(open(filename, encoding="utf-8").read())  #简略写法，解决编码问题
    print(x.call('add', '3', '4'))

if __name__ == '__main__':
    test1()