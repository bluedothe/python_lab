#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/2/2
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

class MyClass:
    name =""
    age = 18

    def welcome(self):
        return "Hello World!"

class Animal:
    name = ""
    leg = 4
    canFly = False
    canRun = True
    canSwime = False

    def __init__(self,name,leg):
        self.name = name
        self.leg = leg
        self.color = "black"

    def run(self):
        pass

    def fly(self):
        pass

    def printSelf(self):
        print(self)

class CatCalalog(Animal):
    pass

def test_myclass():
    x = MyClass()
    x.name = "zhangsan"
    print(x.name,x.age)
    print(x.welcome())

def test_animal():
    x = Animal("hen",2)
    print(x.name,x.leg,x.color)
    print(x)
    print(x.printSelf())

if __name__ == '__main__':
    test_myclass()
    test_animal()