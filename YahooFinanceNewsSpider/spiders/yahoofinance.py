# -*- coding: utf-8 -*-
import scrapy
import re

from YahooFinanceNewsSpider.items import YahoofinancenewsspiderItem

class YahoofinanceSpider(scrapy.Spider):
    name = "yahoofinance"

    download_delay = 2 

    start_urls = [
        # "http://finance.yahoo.com/q/h?s=A ",
        # "http://finance.yahoo.com/q/h?s=AA",
        # "http://finance.yahoo.com/q/h?s=AAPL",
        # "http://finance.yahoo.com/q/h?s=ABC",
        # "http://finance.yahoo.com/q/h?s=ABT",
        # "http://finance.yahoo.com/q/h?s=ACE",
        # "http://finance.yahoo.com/q/h?s=ACN ",
        # "http://finance.yahoo.com/q/h?s=ADBE",
        # "http://finance.yahoo.com/q/h?s=ADI",
        # "http://finance.yahoo.com/q/h?s=ADM",
        # "http://finance.yahoo.com/q/h?s=ADP",
        # "http://finance.yahoo.com/q/h?s=ADSK",
        # "http://finance.yahoo.com/q/h?s=AEE",
        # "http://finance.yahoo.com/q/h?s=AEP",
        # "http://finance.yahoo.com/q/h?s=AES",
        # "http://finance.yahoo.com/q/h?s=AET",
        # "http://finance.yahoo.com/q/h?s=AFL",
        # "http://finance.yahoo.com/q/h?s=AGN",
        # "http://finance.yahoo.com/q/h?s=AIG",
        # "http://finance.yahoo.com/q/h?s=AIV",
        # "http://finance.yahoo.com/q/h?s=AIZ",
        # "http://finance.yahoo.com/q/h?s=AKAM",
        # "http://finance.yahoo.com/q/h?s=AKS",
        # "http://finance.yahoo.com/q/h?s=ALL",
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

    #parse the news content from finance.yahoo.com
    def parse_yahoo_finance_contents(self, response):
        sel = response.xpath('//section[@id="mediacontentstory"]')
        try:
            item = YahoofinancenewsspiderItem()
            item['title'] = sel.xpath('//header/h1[@class="headline"]/text()').extract_first()
            item['link'] = response.url
            item['datetime'] = sel.xpath('//abbr/text()').extract()_first()
            item['content'] = sel.xpath('//div/p/descendant::text()').extract()
            return item
            
        except IndexError, e:
            print '*'*15, 'error start', '*'*15
            print 'response.headers:', response.headers
            print 'response.status:', response.status 
            print 'response.body:', response.body
            print sel.xpath('//header/h1[@class="headline"]/text()')
            print '*'*15, 'error   end', '*'*15

    #parse the news content from www.thestreet.com
    #Error 403 Forbidden
    def parse_thestreet_contents(self,response): 

        item = YahoofinancenewsspiderItem()
        item['title'] = response.xpath('//header[@id="article-header"]/h1/text()').extract_first()

        return item

    #http://www.siliconbeat.com
    def parse_siliconbeat_contents(self, response):
        item = YahoofinancenewsspiderItem()
        item['title'] = response.xpath('//div[@class="wrapper-content"]/h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//div[@class="wrapper-content"]//time/text()').extract_first()
        item['content'] = response.xpath('//div[@class="wrapper-content"]/div[@class="post-content"]//descendant-or-self::text()').extract()
        return item

    #error code 301
    def parse_moodys_contents(self, response):
        pass

    #forbbid by GFW
    #http://www.mercurynews.com
    def parse_mercurynews_contents(self, response):
        item = YahoofinancenewsspiderItem()
        item['title'] = response.xpath('//h1[@id="articleTitle"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//div[@id="articleDate"]/text()').extract_first().split('\t')[-1]
        item['content'] = response.xpath('//div[@id="articleBody"]/descendant::text()').extract()
        return item

    #error code 301
    def parse_marketwatch_contents(self, response):

    #http://www.latimes.com
    def parse_latimes_contents(self, response):
        item = YahoofinancenewsspiderItem()
        item['title'] = response.xpath('//h1[@itemprop="headline"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//time[@itemprop="datePublished"]/@datetime').extract_first()
        item['content'] = response.xpath('//div[@itemprop="articleBody"]/descendant::text()').extract()
        return item

    #http://www.investors.com
    def parse_investors_contents(self, response):
        item = YahoofinancenewsspiderItem()
        item['title'] = response.xpath('//h1[@class="header1"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//li[@class="post-time"]/text()').extract_first()
        item['content'] = response.xpath('//article/div/descendant::text()').extract()
        return item

    #http://www.investopedia.com
    def parse_investopedia_contents(self, response):
        item = YahoofinancenewsspiderItem()
        item['title'] = response.xpath('//div[@id="Content"]/div[1]/h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//span[@class="by-author "]/text()').extract()[-1].split('|')[-1]
        item['content'] = response.xpath('//article/div[@class="content-box"]/descendant::text()').extract()
        return item

    #http://www.insidermonkey.com
    def parse_insidermonkey_contents(self, response):
        item = YahoofinancenewsspiderItem()
        item['title'] = response.xpath('//article/div[2]/h1/a/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//h6[@class="by-line"]/text()').extract_first().split('on')[-1]
        item['content'] = response.xpath('//div[@class="content-without-wrap entry single-content"]/descendant::text()').extract()
        return item

    #http://www.ft.com
    #error code 301
    def parse_ft_contents(self, response):
        pass

    #http://www.foxbusiness.com
    #error code 301
    def parse_foxbusiness_contents(self, response):
        pass

    #http://www.forbes.com
    #can't get content
    def parse_forbes_contents(self, response):
        pass

    #http://www.fool.com
    #no published datetime
    def parse_fool_contents(self, response):
        pass

    #http://www.cnet.com
    #http://www.engadget.com
    #http://www.cnbc.com/id
    #http://sgi.seleritycorp.com
    #http://portal.kiplinger.com
    #http://news.investors.com
    #error code 301

    #http://www.capitalcube.com
    def parse_capitalcube_contents(self, response):
        item = YahoofinancenewsspiderItem()
        item['title'] = response.xpath('//header[@class="entry-header"]/h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//abbr[@class="published"]/@title').extract_first()
        item['content'] = response.xpath('//div[@class="entry-content"]/descendant::text()').extract()
        return item        


    #http://www.bloomberg.com
    #can't receive response

    #http://www.bizjournals.com
    #error code 456, Access To Website Blocked

    #http://www.barrons.com
    #http://qz.com
    #no precise datetime

    #http://realmoney.thestreet.com
    #error code 403

    #http://marketrealist.com
    def parse_marketrealist_contents(self, response):
        item = YahoofinancenewsspiderItem()
        item['title'] = response.xpath('//h2[@class="multipart-article-title"]/span/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//span[@class="authored_date"]/text()').extract()[-1]
        item['content'] = esponse.xpath('//div[@class="article"]/descendant::text()').extract()
        return item         

    #http://fortune.com
    #no content 
    def parse_fortune_contents(self, response):
        item = YahoofinancenewsspiderItem()
        item['title'] = response.xpath('//h1[@class="entry-title"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//time[@itemprop="datePublished"]/text()').extract_first()
        item['content'] = esponse.xpath('//div[@class="article"]/descendant::text()').extract()
        return item  
