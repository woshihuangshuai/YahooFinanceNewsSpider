# -*- coding: utf-8 -*-
import scrapy

from YahooFinanceNewsSpider.items import YahoofinancenewsspiderItem

class YahoofinanceSpider(scrapy.Spider):
    name = "yahoofinance"

    download_delay = 2 

    start_urls = [
        "http://finance.yahoo.com/q/h?s=BSX",
        "http://finance.yahoo.com/q/h?s=C"
    ]

    def parse(self, response):
        for sel in response.xpath('//table[@id="yfncsumtab"]//ul//li'):
            urls = sel.xpath('a/@href').extract()
            for url in urls:
                print url.split('*')[-1]
                yield scrapy.Request(url.split('*')[-1], callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        sel = response.xpath('//header')

        item = YahoofinancenewsspiderItem()
        item['title'] = sel.xpath('h1/text()').extract()[0]
        item['datetime'] = sel.xpath('..//abbr/text()').extract()[0]
        item['content'] = sel.xpath('../div/p/text() | ../div/p/strong/text()').extract()
        item['link'] = response.url
        yield item
