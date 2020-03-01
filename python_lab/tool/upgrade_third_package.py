#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2019/12/1
'''

import pip
from subprocess import call
from pip._internal.utils.misc import get_installed_distributions

__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2019"

#过期的第三方包列表
def outdated_third_package():
    num = 0
    for dist in get_installed_distributions():
        print(dist)
        num = num + 1
    print("num: ", num)

def install_third_package(package_name):
    call("pip install " + package_name, shell=True)

# 更新所有过期的第三方包
def upgrade_third_package():
    num = 0
    for dist in get_installed_distributions():
        num = num + 1
        print("num: ", num)
        print("",dist)
        call("pip install --upgrade " + dist.project_name, shell=True)
        print("",dist)

if __name__ == '__main__':
    #upgrade_third_package()
    outdated_third_package()
    #install_third_package("pywin32_bootstrap")