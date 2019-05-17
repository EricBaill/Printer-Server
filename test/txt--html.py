# -*- coding: utf-8 -*-
# util.py
def lines(file):
    # 遍历文本文件，用生成器保存每行
    for line in file: yield line  # 此时获取到第一行的值后，会暂停，返回到被调用的地方，即blocks函数语句中
    # 在文件最后添加空行
    yield '\n'


def blocks(file):
    block = []
    # lines函数返回的yield存储值，拿来每行遍历，根据是否有空行找出段落
    for line in lines(file):
        # 判断是否为字符串，字符串才有split()方法，如果有，追加到block里,开始回到lines中进入到下一次循环，
        if line.strip():
            block.append(line)
        # 如果不是字符串，那么将block里的内容去空格并追加到空字符串''后，然后清空block，避免重复内容
        elif block:
            yield ''.join(block).strip()
            block = []


# simple_markup.py
import sys, re
# from util import *

print('...')
title = True

for block in blocks(sys.stdin):
    block = re.sub(r'\*(.+?)\*', r'<em>\1</em>', block)
    if title:
        print('<h1>')
        print(block)
        print('</h1>')
        title = False
    else:
        print('<p>')
        print(block)
        print('</p>')
    print('')