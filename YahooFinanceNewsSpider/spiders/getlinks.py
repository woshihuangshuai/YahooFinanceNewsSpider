# -*- coding: utf-8 -*-
import scrapy
import re
from YahooFinanceNewsSpider.items import LinksItem
from selenium import webdriver
import time

class GetlinksSpider(scrapy.Spider):
    name = "getlinks"

    download_delay = 2

    start_urls = [
        "http://finance.yahoo.com/quote/BSX",
        # "http://finance.yahoo.com/quote/C"
    ]

    def parse(self, response):
        urls_list = set()

        l = 10000
        js = 'var q=document.documentElement.scrollTop=%d' %l 

        browser = webdriver.Firefox()
        browser.get(response.request.url)
        browser.execute_script(js)
        time.sleep(10)
        items_list = browser.find_elements_by_xpath('//h3/a')
        
        num_of_items = 0
        while num_of_items != len(items_list):
            num_of_items = len(items_list)
            l += 5000
            js = 'var q=document.documentElement.scrollTop=%d' %l
            browser.execute_script(js)
            time.sleep(5)
            items_list = browser.find_elements_by_xpath('//h3/a')

        for item in items_list:
            urls_list.add(item.get_attribute('href'))
        browser.quit()

        for url in urls_list:
            print url

            item = LinksItem()
            item['link'] = url
            yield item
            
        print 'total', '*'*10, len(urls_list)