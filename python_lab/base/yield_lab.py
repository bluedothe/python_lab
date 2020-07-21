#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
一个带有 yield 的函数就是一个 generator，它和普通函数不同，生成一个 generator 看起来像函数调用，
但不会执行任何函数代码，直到对其调用 next()（在 for 循环中会自动调用 next()）才开始执行。
虽然执行流程仍按函数的流程执行，但每执行到一个 yield 语句就会中断，并返回一个迭代值，下次执行时从 yield 的下一个语句继续执行。
看起来就好像一个函数在正常执行的过程中被 yield 中断了数次，每次中断都会通过 yield 返回当前的迭代值。

程序遇到yield关键字，然后把yield想想成return,return之后，程序停止;
next就相当于“下一步”,从上次return后的语句开始执行，再一次的next接着上一次的next停止的地方执行的；
所以调用next的时候，生成器并不会从函数的开始执行，只是接着上一步停止的地方开始，然后遇到yield后，return出要生成的数，此步就结束；
send函数会把参数带给生成器；
由于send方法中包含next()方法，所以程序会继续向下运行执行；
'''

'''
    module description
    date: 2020/7/15
'''

from config import config

#参考：https://blog.csdn.net/mieleizhi0522/article/details/82142856/
def foo1():
    print("starting...")
    while True:
        res = yield 4
        print("res:",res)

def test_foo1():
    g = foo1()
    print(next(g))
    print("*"*20)
    print(next(g))
    print(g.send(7))

def foo2(num):
    print("starting...")
    while num<10:
        num=num+1
        yield num

def test_foo2():
    for n in foo2(0):
        print(n)

    for n in range(1000):   #range就是一个生成器
        a = n

#生成斐波那契數列
def fab(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1

def test_fab():
    for n in fab(5):   #调用 fab(5) 不会执行 fab 函数，而是返回一个 iterable 对象
        print(n)

    print("*" * 20)
    f = fab(5)
    print(next(f))
    print(next(f))

def read_file(filename):
    BLOCK_SIZE = 1024
    with open(filename, 'rb') as f:
        while True:
            block = f.read(BLOCK_SIZE)
            if block:
                yield block
            else:
                return

def test_read_file():
    filename = config.sample_file_path + "/演示功能点要求.txt"
    for text in read_file(filename):
        print(text)


if __name__ == '__main__':
    test_read_file()