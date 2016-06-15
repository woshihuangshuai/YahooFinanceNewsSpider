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
                yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        sel = response.xpath('//section[@id="mediacontentstory"]')

        # print sel.xpath('//header/h1/text()').extract()
        # print sel.xpath('//abbr/text()').extract()
        # print sel.xpath('//div[@class = "body yom-art-content clearfix"]/text()').extract()
        # print response.url


        item = YahoofinancenewsspiderItem()
        item['title'] = sel.xpath('//header/h1/text()').extract()
        item['datetime'] = sel.xpath('//abbr/text()').extract()
        item['content'] = sel.xpath('//div[@class = "body yom-art-content clearfix"]/text()').extract()
        item['link'] = response.url
        yield item
