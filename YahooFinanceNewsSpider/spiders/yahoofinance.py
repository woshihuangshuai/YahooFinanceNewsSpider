# -*- coding: utf-8 -*-
import scrapy
import re

from YahooFinanceNewsSpider.items import YahoofinancenewsspiderItem

class YahoofinanceSpider(scrapy.Spider):
    name = "yahoofinance"

    download_delay = 2 

    start_urls = [
        "http://finance.yahoo.com/q/h?s=BSX",
        "http://finance.yahoo.com/q/h?s=C"
    ]

    def parse(self, response):
        for sel in response.xpath('//table[@id="yfncsumtab"]//ul//li/a/@href'):
            news_content_url = sel.extract()
            if re.match('http://finance.yahoo.com/news/.*', news_content_url) != None: #onlycrawl news post by yahoo finance
                print 'news_content_url:', news_content_url
                yield scrapy.Request(news_content_url, callback=self.parse_yahoo_finance_contents)

        next_page_url = response.xpath('//b[a=\'Older Headlines\']/a/@href').extract_first()
        if next_page_url != None:
            next_page_url = 'http://finance.yahoo.com' + next_page_url
            print 'next_page_url:', next_page_url
            yield scrapy.Request(next_page_url,callback=self.parse)

    def parse_yahoo_finance_contents(self, response):
        sel = response.xpath('//header')

        item = YahoofinancenewsspiderItem()
        item['title'] = sel.xpath('h1/text()').extract()[0]
        item['datetime'] = sel.xpath('..//abbr/text()').extract()[0]
        item['content'] = sel.xpath('../div/p/text() | ../div/p/strong/text()').extract()
        item['link'] = response.url
        yield item
