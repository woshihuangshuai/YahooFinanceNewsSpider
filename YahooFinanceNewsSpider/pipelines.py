# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import string
from string import maketrans

class YahoofinancenewsspiderPipeline(object):
    def process_item(self, item, spider):

        intab = string.punctuation + '～！@＃¥％……&＊（）｛｝［］｜、；：‘“，。／？《》＝＋－——｀'
        outtab = ' '*len(intab)
        trans_tab = maketrans(intab, outtab)

        news_content = ''
        for line in item['content']:
            line = line.encode('utf8')
            line = line.replace('\t', '').replace('\n', '').replace('\r', '')
            sub_line = re.subn(r'\\u.{4}', '', line)[0]
            sub_line = sub_line.translate(None, intab)
            news_content += sub_line

        item['content'] = news_content

        return item