#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, render_template, make_response, session, url_for
from datetime import datetime
from datetime import timedelta
import os

'''
    module description
    date: 2019/10/29

'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2019"

app = Flask(__name__, static_url_path="")
app.config.from_pyfile('config.ini')
app.config['SECRET_KEY'] = os.urandom(24)                       #使用一组随机数对session进行加密
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)   #修改session 过期时间 --> session.permanent = True
app.debug= True

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/reg')
def user_reg():
    return render_template('reg.html')

@app.route('/get_data', methods=['POST', 'GET'])
def get_data():
    data = {}
    if request.method == 'GET':
        data['username'] = request.args.get('username',None)
        data['email'] = request.args.get('email', None)
        data['edu'] = request.args.get('edu', None)
    else:
        data['info'] = "requst method is error, not get!"
    return str(data)

@app.route('/post_data', methods=['POST', 'GET'])
def post_data():
    data = {}
    if request.method == 'POST':
        data['username'] = request.form.get('username',None)
        data['email'] = request.form.get('email', None)
        data['edu'] = request.form.get('edu', None)
    else:
        data['info'] = "requst method is error,not post!"
    return str(data)

#max_age设置有效期， 单位是秒,在IE8一下的浏览器是不支持的
#expires参数在新版本的http协议中视为被废弃的
#domain默认只在主域名有效，如果想在子域名下使用，要在前面加点，参考下面的示例
#set_cookie('login', 'yes',max_age=3600,expires=expires,domain='.hy.com')
@app.route('/info',  methods=['POST', 'GET'])
def info():
    if request.cookies.get('login') == 'yes':
        resp = make_response(render_template('info.html', login_info='欢迎您又回来！'))
    else:
        resp = make_response(render_template('info.html', login_info='欢迎光临！'))
        resp.set_cookie('login', 'yes')
    return resp

'use session'
@app.route('/test_session', methods=['POST', 'GET'])
def test_session():
    return render_template('test_session.html')

'use session'
@app.route('/set_session', methods=['POST', 'GET'])
def set_session():
    session.permanent = True    # permanent：持久化(默认过期时间是31天)
    session['username'] = request.form.get('username',None)
    session['email'] = request.form.get('email', None)
    session['edu'] = request.form.get('edu', None)
    return redirect(url_for('get_session'))

'use session'
@app.route('/get_session', methods=['POST', 'GET'])
def get_session():
    username = session['username']
    email = session['email']
    edu = session['edu']
    return render_template('info.html', username = username, email = email, edu = edu)

if __name__ == '__main__':
    app.run()
