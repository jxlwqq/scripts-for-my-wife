#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 下载美剧,命令行运行脚本时,必须带一个参数:剧名,第二个参数是下载类型,默认为ed2k(电驴)
# 例如:
# python download_us_drama.py 生活大爆炸 ed2k

import requests
import sys
from lxml import etree
import re

key_words = sys.argv[1]
if len(sys.argv) < 3:
    type = 'ed2k'
else:
    type = sys.argv[2]

print '您将下载: ' + key_words
type_list = ('ed2k', 'magnet')
if type not in type_list:
    type = 'ed2k'
print '下载类型: ' + type

url = "http://cili07.com/?topic_title3=%s" % (key_words,)
tree = etree.HTML(requests.get(url).text)
max_page_url = tree.xpath('//div[@class="pages"]/a[last()]/@href')
if len(max_page_url) == 0:
    max_page = 1
else:
    pattern = re.compile('^\/\?topic_title3=.*?\&p=(\d)+$', re.S)
    max_page = re.findall(pattern, max_page_url[0])[0]

for i in range(1, int(max_page) + 1):
    url = "http://cili07.com/?topic_title3=%s&p=%d" % (key_words, i)
    res = requests.get(url)
    tree = etree.HTML(res.text)
    nodes = tree.xpath('//dl[@class="list-item"]/dd/@%s' % type)
    for node in nodes:
        print node
