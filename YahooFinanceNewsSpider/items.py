# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanynewsItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    datetime = scrapy.Field()
    corp_name = scrapy.Field()
    content = scrapy.Field()


class SectornewsItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    datetime = scrapy.Field()
    sector = scrapy.Field()
    content = scrapy.Field()


class IndustrynewsItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    datetime = scrapy.Field()
    sector = scrapy.Field()
    industry = scrapy.Field()
    content = scrapy.Field()
        
    
