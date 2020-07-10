#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/7/10
'''

from docx import Document

def read_file(filename):
    doc = Document(filename)
    # 每一段的内容
    #for para in doc.paragraphs:
    #    print(para.text)

    # 每一段的编号、内容
    #for i in range(len(doc.paragraphs)):
    #    print(str(i), doc.paragraphs[i].text)

    for i, p in enumerate(doc.paragraphs):
        print(str(i) + ": " + str(p.text))

    doc.paragraphs[0].text = "ABC" + " DEF"

if __name__ == '__main__':
    filename = "G:/english/\word/短单词/测试文档.docx"
    read_file(filename)