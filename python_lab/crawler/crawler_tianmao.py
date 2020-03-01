#!/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib
import urllib.request
import re
from bs4 import BeautifulSoup
import time
import random
import json
import math

'''
    module description
    date: 2020/2/2
    抓取天猫的一个女装的评论
    来源：https://blog.csdn.net/weixin_36604953/article/details/78592943
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

# 创建一个文件存储评论及其他数据
myfile = open("tm_fz_gn_1_1_1.txt","a")
# 共获取四个变量，评论者昵称，是否超级会员，评论时间，评论内容
print("评论者昵称","是否超级会员","评论时间","comment",sep='|',file=myfile)
stop = random.uniform(0.5,2)

# 获取页数
try:
    url0 = "https://rate.tmall.com/list_detail_rate.htm?itemId=544442011638&spuId=718591114&sellerId=196993935&order=3&currentPage=1&append=0&content=1&tagId=&posi=&picture=&ua=025UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockp3S39AeU13QnhDeC4%3D%7CU2xMHDJ7G2AHYg8hAS8XIw0tA18%2BWDRTLVd5L3k%3D%7CVGhXd1llXWBcaFduWmBVb1RvWGVHe0Z9SXRLc05zRnlDfkZ6VAI%3D%7CVWldfS0TMww1CioWIgIsCCNMMWwyVDlrME8iakFhXn5BZEocSg%3D%3D%7CVmhIGCUFOBgkGiMXNwwzBzsbJxkiGTkDOA0tES8ULw81Cj9pPw%3D%3D%7CV2xMHDIcPAA%2FASEcPAM4Az9pPw%3D%3D%7CWGBAED4QMGBaZ1p6RXBKc1NoXWBCfUh0S3NTbVBqSnROblBkMhIvDyEPLxciGSx6LA%3D%3D%7CWWBdYEB9XWJCfkd7W2VdZ0d%2BXmBdfUF0Ig%3D%3D&isg=AnBwr9DL3fao4YAwe7Eb61VPQT4CEVRrBvSVMGrBPUueJRHPEskkk8YHCxu-&needFold=0&_ksTS=1501924984733_1070&callback=jsonp1071"
    req0 = urllib.request.Request(url0)
    req0.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    html0 = urllib.request.urlopen(req0,timeout=500).read()
    html0 = bytes.decode(html0,encoding="gbk")
    # print(type(html0))
    '''
    下面这一步是因为这个json不是标准的json，json是一个完完全全的字典，而这个json是在类似json1234()这个结构的括号中，打开看看这个json你就懂了，所以需要用正则表达式去获取真实的json（即字典）
    '''
    js0 = re.search('{"rateDetail(.*)',html0).group()[:-1]
    # 将json主要内容存入content
    content0 = json.loads(js0)
    content = content0['rateDetail']
    # print(content.keys())
    # print(json.dumps(content0, sort_keys=True, indent=2))
    #尾页
    lastpage = int(content['paginator']['lastPage'])
except:
    print("获取尾页失败，默认爬取99页")
    lastpage = 99

# 构造循环遍历每一页
for i in range(1,lastpage):
    try:
        url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=544442011638&spuId=718591114&sellerId=196993935&order=3&currentPage='+str(i)+'&append=0&content=1&tagId=&posi=&picture=&ua=025UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockp3S39AeU13QnhDeC4%3D%7CU2xMHDJ7G2AHYg8hAS8XIw0tA18%2BWDRTLVd5L3k%3D%7CVGhXd1llXWBcaFduWmBVb1RvWGVHe0Z9SXRLc05zRnlDfkZ6VAI%3D%7CVWldfS0TMww1CioWIgIsCCNMMWwyVDlrME8iakFhXn5BZEocSg%3D%3D%7CVmhIGCUFOBgkGiMXNwwzBzsbJxkiGTkDOA0tES8ULw81Cj9pPw%3D%3D%7CV2xMHDIcPAA%2FASEcPAM4Az9pPw%3D%3D%7CWGBAED4QMGBaZ1p6RXBKc1NoXWBCfUh0S3NTbVBqSnROblBkMhIvDyEPLxciGSx6LA%3D%3D%7CWWBdYEB9XWJCfkd7W2VdZ0d%2BXmBdfUF0Ig%3D%3D&isg=AnBwr9DL3fao4YAwe7Eb61VPQT4CEVRrBvSVMGrBPUueJRHPEskkk8YHCxu-&needFold=0&_ksTS=1501924984733_1070&callback=jsonp1071'
        req = urllib.request.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
        html = urllib.request.urlopen(req,timeout=500).read()
        html = bytes.decode(html,encoding="gbk")
        js = re.search('{"rateDetail(.*)', html).group()[:-1]
        infos0 = json.loads(js)
        infos = infos0['rateDetail']['rateList']
        tiaoshu = 0
        for info in infos:
            try:
                tiaoshu += 1
                time.sleep(stop)
                ss = "正在爬取第%d页的第%d条评论,共%d页" % (i,tiaoshu,lastpage)
                print(ss)
                # 用户姓名
                try:
                    user_name = info['displayUserNick'].strip().replace('\n','')
                except:
                    user_name = ""
                # 是否黄金会员
                try:
                    user_status = info['goldUser'].strip().replace('\n','')
                except:
                    user_status = ""
                # 评论时间
                try:
                    comment_date = info['rateDate'].strip().replace("\n","")
                except:
                    comment_date = ""
                # 评论内容
                try:
                    comment = info['rateContent'].strip().replace("\n","").replace('\t','')
                except:
                    comment = ""
                print(user_name,user_status,comment_date,comment,sep='|',file=myfile)
            except:
                sss = '爬取第%d页的第%d条评论失败,跳过爬取' % (i,tiaoshu)
                print(sss)
                pass
    except:
        print("该产品url获取失败，请检查")
myfile.close()

if __name__ == '__main__':
    pass