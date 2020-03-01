#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
from crawler import html_example_file
import bs4
'''
    module description
    date: 2020/1/31
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

soup = BeautifulSoup(html_example_file.html_doc, 'lxml')   #'lxml'   "html5lib"   "html.parser"   , from_encoding='utf-8'

"""
1BeautifulSoup对象:soup 对象本身比较特殊，它的 name 即为 [document]，对于其他内部标签，输出的值便为标签本身的名称，attrs值为空字典。
2tag对象:其中两个属性就是name和attributes(attrs),.contents 和 .children 属性仅包含tag的直接子节点，.descendants 属性可以对所有tag的子孙节点进行递归循环，和 children类似
Tag.String：Tag只有一个String子节点时，可以这么访问，否则返回None.如果一个标签里面没有标签了，那么 .string 就会返回标签里面的内容。如果标签里面只有唯一的一个标签了，那么 .string 也会返回最里面的内容。如果超过一个标签的话，那么就会返回None。
Tag.parent：父节点，标签内容是末级节点，也有父级
Tag.parents：父到根的所有节点 
3NavigableString对象:利用.string属性表示包含在tag中的文字。注意！如果tag中包含子tag，navigableString对象会是None.一个 NavigableString 字符串与Python中的str字符串相同，通过str() 方法可以直接将 NavigableString 对象转换成str字符串
4Comment对象:用来查找HTML里的注释标签。是一个特殊的NavigableString，其实输出的内容仍然不包括注释符号，但是如果不好好处理它，可能会对我们的文本处理造成意想不到的麻烦。
查找数据的几种方法：标签名称、id、class、属性、文本、父、子、兄弟
"""

def test_tag():
    print('*' * 40, " tag ", '*' * 40)
    print(soup.title)  # 输出第一个 title 标签
    print(soup.title.name)  # 输出第一个 title 标签的标签名称
    print(soup.title.string)  # 输出第一个 title 标签的包含内容
    print(soup.title.parent.name)  # 输出第一个 title 标签的父标签的标签名称
    print(soup.a['href'])  # 输出第一个 a 标签的  href 属性内容
    print(soup.p.contents)  #输出第一个 p 标签的所有子节点,以列表形式返回所有子节点。
    print(soup.get_text())  # 获取所有文字内容
    print(soup.a.attrs)  # 输出第一个  a 标签的所有属性信息
    print(soup.p.get('class'))  #等价于soup.p['class']
    print(soup.meta)  #取第一个tag
    list = soup('meta') #取所有tag，返回列表
    print(len(list),list)
    print(soup.meta.get('charset'),"=",soup.meta['charset'])  #取tag标签的指定属性值
    #print(soup.meta.get('name'),"=",soup.meta['name']) #name是关键字，不能使用
    #print(soup.meta.get('content'),"=",soup.meta['content'])  #content是关键字，不能使用
    print(soup.link.get('href'),"=",soup.link['href']) #取第一个满足的值
    print(soup.link['href'])
    for child in soup.p.children:  # 对soup.p的子节点进行循环输出,生成器可用于循环访问：for child in Tag.children
        print("对soup.p的子节点进行循环输出", child)

    if type(soup.h2.string) == bs4.element.Comment:  #首先判断了它的类型，是否为 Comment 类型，然后再进行其他操作
        print(soup.h2.string)    #h2标签里的内容实际上是注释，但是如果我们利用 .string 来输出它的内容，我们发现它已经把注释符号去掉了

    for string in soup.strings:   #获取多个内容，需要遍历获取
        print(repr(string))
    for string in soup.stripped_strings:  #获取多个内容，需要遍历获取,输出的字符串中可能包含了很多空格或空行,使用 .stripped_strings 可以去除多余空白内容
        print(repr(string))

    tag = soup.p
    print(tag)
    print(tag.name)
    print(tag.attrs)
    print(tag['class'])
    print(tag.previous_sibling)  #上一个兄弟
    print(tag.next_sibling)   #下一个兄弟

def test_find():
    print(soup.find(name='p'))
    print(soup.find('meta'))  # 获取第一个标签
    print(soup.find(['meta', 'p']))  # 获取符合任一标签的结果
    print(soup.find({'head': True, 'body': True}))
    print(soup.find(re.compile('^p')))  # 搜索以p开头的tag
    # print(soup.find(lambda name: if len(name) == 1))  #搜索长度为1的tag  # 搜索函数返回结果为true的tag
    print(soup.find(attrs={'id': True, 'algin': None}))  # 寻找有id属性但是没有algin属性的
    print(soup.find('meta', attrs={'name': 'location'}))  # 获取第一个标签，根据属性过滤获取
    print(soup.find('div', {'id': 'nav_menu'}))  # 取id为nav_menu的div
    print(soup.find('a', class_='icon'))  # 查找a标签 class=icon
    print(soup.find(id='job'))  # 查找id=job
    print(soup.find("span", class_="cate-img", id="car"))  # 根据指定多个属性值获取特定标签
    print(soup.find(attrs={"class": "cate-img"}))
    print(soup.find(class_="adsf").get_text())  # 获取标签的文本内容
    print(soup.find(class_="title1").get_text("|",
                                              strip=True))  # 获取文本内容时可以指定不同标签之间的分隔符，也可以选择是否去掉前后的空白。只获取到第一个标签的内容，没有得到分隔符的效果
    print(soup.find(class_="title1").get("id"))  # 获取class为title的标签的id
    print(soup.find(href="www.sina.com"))  # 根据标签属性查找标签，获取href = "www.sina.com"的标签
    print(soup.find('div', {'id': 'nav_menu'}).children)  # 取id为nav_menu的div中的a标签，返回list_iterator
    print(soup.find('a', {"alog-action": "qb-ask-uname"}).get_text())  # 如果标签里既没有class也没有id，可以根据其属性来定义获取规则
    print(soup.find(attrs={"alog-action": "qb-ask-uname"}))  # 如果标签里既没有class也没有id，可以根据其属性来定义获取规则
    for item in soup.find('div', {'id': 'nav_menu'}).children:
        print(type(item))
        if type(item) == 'bs4.element.Tag':
            print(item['href'])  # 得到a标签的文本内容，比如新浪、搜狐，为什么不是href的值
        else:  # type='bs4.element.NavigableString'
            print(item.string)  # 得到多行空值，不知为何

    soup.find_previous("p")  # 获取前头的标签
    soup.find_next("p")  # 获取后头的标签
    soup.find_parent("div")  # 找父标签
    tag = soup.find(attrs={'href': "www.sohu.com"})
    print(tag)
    print(
        tag.previous_sibling)  # 上一个兄弟,previous_siblings得到兄弟们。需要注意的是，很可能直接相邻的上一个下一个兄弟节点并不是Tag而是一个换行符啊标点符号啊等NavigableString对象（字符串节点）
    print(
        tag.next_sibling)  # 下一个兄弟,next_siblings得到兄弟们。需要注意的是，很可能直接相邻的上一个下一个兄弟节点并不是Tag而是一个换行符啊标点符号啊等NavigableString对象（字符串节点）
    print(tag.parent)  # 元素父节点
    print(tag.parents)  # 递归得到所有的父节点，得到迭代对象，可以用list函数转换为list
    print(
        tag.previous_element)  # 元素前节点，previous_elements获取前所有节点。与 .next_sibling .previous_sibling 不同，它并不是针对于兄弟节点，而是在所有节点，不分层次
    print(tag.next_element)  # 元素后节点，next_elements获取前所有节点。与 .next_sibling .previous_sibling 不同，它并不是针对于兄弟节点，而是在所有节点，不分层次


def test_find_all():
    # name
    print(soup.find_all("span"))
    print(soup.find_all('meta'))  # 获取所有标签，返回list
    print(soup.find_all(["a", "h3"]))  # 寻找a标签和h3标签，满足一个即可
    print(soup.html.find_all("ul",recursive=False))  # recursive参数是否递归，默认true，recursive=False时，只find当前标签的第一级子标签的数据，为False是取不到值，不知道为何

    print(soup.find_all(attrs={"id":"link1"}))
    print(soup.find_all(attrs={"class": "sister"}))
    print(soup.find_all(id="link1"))
    print(soup.find_all(class_="sister"))
    print(soup.find_all(rel = "external nofollow"))
    print(soup.find_all('div', id='nav_menu'))
    print(soup.find_all('p','title1'))   #第一个参数必须是标签名,第二个参数必须是class,  title1是class
    print(soup.find_all(attrs={"alog-action":"qb-ask-uname"}))
    print(soup.find_all(attrs={"name":"location"}))
    print(soup.find_all(rel="external nofollow",target="_blank"))
    print(soup.find_all(text="Elsie"))  #必须完全匹配
    print(soup.find_all(text=re.compile("全选")))
    print(soup.find_all(text=["Tillie", "Elsie", "Lacie"]))
    print(soup.find_all(text=re.compile("Dormouse")))
    print(soup.find_all(attrs={'style': r'outline:none;'}))  # 用来查找属性中有style='outline:none;的标签体
    print(soup.find_all(onclick='document.location...'))
    print(soup.find_all('meta', attrs={'name': 'format-detection'}))  # 根据属性过滤获取所有满足条件的标签，返回list
    print(soup.find_all(class_=re.compile("tit")))  # 对class名称正则
    print(soup.find_all(name='img', attrs={'src': re.compile("[a-z]*.png")})[0])  # 对src属性正则

    for tag in soup.find_all(re.compile(r"b")):  # 正则匹配，名字中带有b的标签
        print(tag.name)
    for item in soup.find_all(tongji_tag=re.compile('^m_home_')):    #对tongji_tag属性正则
        print(item.find('span', {'class': 'cate-desc'}).string)
    print(soup.find_all('div', 'cate-scroller'))   #获取class为cate-scroller的div标签内容
    for item in soup.find_all('div', 'cate-scroller'):
        print(item.ul.li.a['href'])
        print(item.ul.li.a['tongji_tag'])
    for item in soup.find_all('div', 'post_item_body'):
        print(item.h3.a['href'])
        print(item.h3.a.string)
        print(item.p.get_text().strip())   # strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）
        print(item.div.a.string)
        print(item.div.a.next_sibling.replace('发布于', '').strip())
    for item in soup.find_all('a'):
        if item:
            # print(item.attrs)
            print(item.attrs['href'])  # dict类型
    for i in soup.find_all(class_="title1"):   #获取所有class为title1的标签
        print(i.get_text())
    for i in soup.find_all(class_="title1", limit=1):  #获取特定数量的class为title1的标签
        print(i.get_text())
    for img in soup.find_all(png_image):   #自定义png_image函数作为参数，满足函数的要求则返回标签
        print(img)

    soup.find_all_previous("p")     #获取前头的标签
    soup.find_all_next("p")   #获取后头的标签
    soup.find_parents("div")  #找父标签

def test_select():
    print(soup.select("title"))  # 标签名
    print(soup.select("html head title"))  # 多级标签名
    print(soup.select("p > a"))  # p内的所有a标签
    print(soup.select("p > #link1"))  # P标签内，按id查标签
    print(soup.select("p #link1"))  # P标签内，按id查标签，同上
    print(soup.select("p > .sister"))  # P标签内，按class查标签
    print(soup.select("p .sister"))  # P标签内，按class查标签，同上
    print(soup.select("p.title"))   #  P标签内，按class查标签
    print(soup.select("#link1 ~ .sister"))  # 查找相同class的兄弟节点，不包括link1自己
    print(soup.select("#link1 + .sister"))  #
    print(soup.select(".sister"))  # 按class名称查
    print(soup.select("#link1"))  # 按id名称查
    print(soup.select('a[class="sister"]'))  #注意属性和标签属于同一节点，所以中间不能加空格
    print(soup.select('a[href="http://example.com/elsie"]'))
    print(soup.select('p a[href="http://example.com/elsie"]'))  #同一节点的空格隔开，同一节点的不加空格
    #print(soup.select('a[href="http://example.com/elsie"  rel="external nofollow"]'))  # 按标签的属性查，加第二个属性查询时报错
    print(soup.select('a[href$="tillie"]'))   #匹配href属性的部分值
    print(soup.select_one(".sister"))  #获取第一个标签
    print(soup.select('title')[0].get_text())
    print(soup.select('div#nav_menu a'))  #获取id为nav_menu的div中的a标签，返回list
    for item in soup.select('div#nav_menu a'): #遍历 这里注意，a标签不限制必须是div的子级，也可以是子级的子级
        print(item.get('href'), item.string)
    print(soup.select('ul.cate-wrap'))  # 获取class为cate-wrap的ul，返回list
    print(soup.select('ul.cate-wrap li'))  # 获取class为cate-wrap的ul下的li，返回list
    print(soup.select('ul.cate-wrap li a'))  # 获取class为cate-wrap的ul下的li下的a，返回list
    print(soup.select('ul.cate-wrap li a span'))  # 获取class为cate-wrap的ul下的li下的a下的span，返回list
    for item in soup.select('ul.cate-wrap li'):
        print(item.find('a').get('href'), item.find('a').string)
    for title in soup.select('title'):   #select 方法返回的结果都是列表形式
        print(title.get_text())

def png_image(tag):
    return tag.name == "img" and re.compile("[a-z]*da.png").search(tag.attrs["src"])

def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')

def test():
    print(soup.find(text='招商加盟'))
    print(soup.select("p.title"))

if __name__ == '__main__':
    #print(soup.prettify())
    #test_tag()
    test()
    #test_find_all()