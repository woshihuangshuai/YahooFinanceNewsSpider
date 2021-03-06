# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from string                         import maketrans
from YahooFinanceNewsSpider.items   import IndustrynewsItem
from YahooFinanceNewsSpider.items   import CompanynewsItem
import pymongo
import re
import string


class YahoofinancenewsspiderPipeline(object):
    def process_item(self, item, spider):

        if item['content'] = None:
            return
        # intab = string.punctuation + '～！@＃¥％……&＊（）｛｝［］｜、；：‘“，。／？《》＝＋－——｀'
        # outtab = ' '*len(intab)
        # trans_tab = maketrans(intab, outtab)

        # news_content = ''
        # for line in item['content']:
        #     line = line.encode('utf8')
        #     line = line.replace('\t', '').replace('\n', '').replace('\r', '')
        #     sub_line = re.subn(r'\\u.{4}', '', line)[0]
        #     sub_line = sub_line.translate(None, intab)
        #     news_content += sub_line

        # item['content'] = news_content

        return item


class MongoPipeline(object):
    """Write items to MongoDB"""
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri  = mongo_uri
        self.mongo_db   = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri   = crawler.settings.get('MONGO_URI'),
            mongo_db    = crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client     = pymongo.MongoClient(self.mongo_uri)
        self.db         = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        http    = 'http://'
        https   = 'https://'
        url     = item['link'].split('//')[-1]
        if(isinstance(item, IndustrynewsItem)):
            if(self.db['industry_news'].find({'link': http + url}).count() != 0):
                return
            if(self.db['industry_news'].find({'link': https + url}).count() != 0):
                return
            self.db['industry_news'].insert(dict(item))
            return item      
        elif(isinstance(item, CompanynewsItem)):
            if(self.db['company_news'].find({'link': http + url}).count() != 0):
                return
            if(self.db['company_news'].find({'link': https + url}).count() != 0):
                return
            self.db['company_news'].insert(dict(item))
            return item
        else:
            return  


        