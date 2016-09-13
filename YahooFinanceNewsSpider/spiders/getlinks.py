# -*- coding: utf-8 -*-
import scrapy
import re
from YahooFinanceNewsSpider.items import LinksItem
from selenium import webdriver

class GetlinksSpider(scrapy.Spider):
    name = "getlinks"

    download_delay = 2

    start_urls = [
        "http://finance.yahoo.com/quote/BSX",
        # "http://finance.yahoo.com/quote/C"
    ]

    def parse(self, response):
        corp_name = response.url.split('/')[-1]
        urls_set = set()

        l = 10000
        js = 'var q=document.documentElement.scrollTop=%d' %l 

        browser = webdriver.Firefox()
        browser.get(response.request.url)
        browser.execute_script(js)
        time.sleep(10)
        # items_list = browser.find_elements_by_xpath('//h3/a')
        items_list = browser.find_elements_by_xpath('//ul[@class="Mb(0) Ov(h) P(0) Wow(bw)"]/li')

        num_of_items = 0
        while num_of_items != len(items_list):
            num_of_items = len(items_list)
            l += 5000
            js = 'var q=document.documentElement.scrollTop=%d' %l
            browser.execute_script(js)
            time.sleep(5)
            items_list = browser.find_elements_by_xpath('//ul[@class="Mb(0) Ov(h) P(0) Wow(bw)"]/li')

        for item in items_list:
            if(item.find_element_by_xpath('//div[a="Sponsored"]') != None):
                continue
                
            urls_set.add(item.find_element_by_xpath('//h3/a').get_attribute('href'))

        browser.quit()

        for url in urls_set:
            print url
            item = LinksItem()
            item[link] = url
            yield item
