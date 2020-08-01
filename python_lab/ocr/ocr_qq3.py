#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/7/27
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import requests
import hmac
import hashlib
import base64
import time
import random
import re
from config import bluedothe

appid = " "
secret_id = bluedothe.qq_SecretId
secret_key = bluedothe.qq_SecretKey
expired = time.time() + 2592000
onceExpired = 0
current = time.time()
rdm = ''.join(random.choice("0123456789") for i in range(10))
userid = "0"
fileid = "tencentyunSignTest"

info = "a=" + appid + "&b=" + bucket + "&k=" + secret_id + "&e=" + str(expired) + "&t=" + str(current) + "&r=" + str(
 rdm) + "&u=0&f="

signindex = hmac.new(bytes(secret_key,'utf-8'),bytes(info,'utf-8'), hashlib.sha1).digest() # HMAC-SHA1加密
sign = base64.b64encode(signindex + bytes(info,'utf-8')) # base64转码，也可以用下面那行转码
#sign=base64.b64encode(signindex+info.encode('utf-8'))

url = "http://recognition.image.myqcloud.com/ocr/general"
headers = {'Host': 'recognition.image.myqcloud.com',
   "Authorization": sign,
   }
files = {'appid': (None,appid),
 'bucket': (None,bucket),
 'image': ('00022.jpg',open('00022.jpg','rb'),'image/jpeg')
 }

r = requests.post(url, files=files,headers=headers)

responseinfo = r.content
data = responseinfo.decode('utf-8')

r_index = r'itemstring":"(.*?)"'
result = re.findall(r_index, data)
for i in result:
     print(i)


if __name__ == '__main__':
    pass