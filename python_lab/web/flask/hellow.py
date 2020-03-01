#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask

'''
    module description
    date: 2019/10/29
    Flask实现BS交互
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2019"

app = Flask(__name__, static_url_path="")
app.debug= True

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()