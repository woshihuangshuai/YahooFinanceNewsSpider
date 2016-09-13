# -*- coding: utf-8 -*-
import scrapy
import re
from YahooFinanceNewsSpider.items import CompanynewsItem
from selenium import webdriver
import time

'''
    Sector News:
        http://finance.yahoo.com/news/sector-basic-materials/?bypass=true
        
    Industry News:
        http://finance.yahoo.com/industries/energy
        http://finance.yahoo.com/industries/financial
        http://finance.yahoo.com/industries/healthcare
        http://finance.yahoo.com/industries/business_services
        http://finance.yahoo.com/industries/telecom_utilities
        http://finance.yahoo.com/industries/hardware_electronics
        http://finance.yahoo.com/industries/software_services
        http://finance.yahoo.com/industries/industrials
        http://finance.yahoo.com/industries/manufacturing_materials
        http://finance.yahoo.com/industries/consumer_products_media
        http://finance.yahoo.com/industries/diversified_business
        http://finance.yahoo.com/industries/retailing_hospitality
        # total: 12

    Company News:
        S&P 500
        http://finance.yahoo.com/quote/<company_name>

    websites can't be scrapyed:
        # need login
        http://news.investors.com
        http://www.ft.com
        http://news.morningstar.com 
        # can't connect
        http://bits.blogs.nytimes.com
        http://blogs.wsj.com
        # PAGE UNAVAILABLE
        http://online.wsj.com  
        # error code 456, Access To Website Blocked
        http://www.bizjournals.com
        # no content
        http://www.forbes.com/
        # twisted.internet.error.ConnectionLost
        http://www.bloomberg.com
        http://www.bloombergview.com
    
'''

class CompanynewsSpider(scrapy.Spider):
    name = "companynews"

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
        "https://finance.yahoo.com/quote/BSX",
        "https://finance.yahoo.com/quote/C"
    ]

    def parse(self, response):
        corp_name = response.url.split('/')[-1]
        urls_list = []

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
            urls_list.append(item.get_attribute('href'))
        browser.quit()

        for url in urls_list:
            print url
        print 'total', len(urls_list)

        for url in urls_list:
            # http://finance.yahoo.com/news/.*
            if re.match(r'http://finance.yahoo.com/news/.*', url) != None: 
                request = scrapy.Request(url, callback=self.parse_yahoo_news_contents)
                request.meta['corp_name'] = corp_name
                yield request
            # http://finance.yahoo.com/video/.*
            elif re.match(r'http://finance.yahoo.com/video/.*', url) != None:
                request = scrapy.Request(url, callback=self.parse_yahoo_video_contents)
                request.meta['corp_name'] = corp_name
                yield request
            # parse other web
            else:
                request = scrapy.Request(url, callback=self.parse_other_url)
                request.meta['corp_name'] = corp_name
                yield request

    # parse the news content from finance.yahoo.com/news/
    def parse_yahoo_news_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//header/h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//span[@class="date D(ib) Fz(11px) Mb(4px)"]/text()').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@id="Col1-0-ContentCanvas-Proxy"]/descendant::text()').extract()[:-1]
        return item
        
    # parse the news content from finance.yahoo.com/video/
    def parse_yahoo_video_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//span[@class="date D(ib) Fz(11px) Mb(4px)"]/text()').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//p/descendant::text()').extract()
        return item

    # get url which links to other website.
    def parse_other_url(self, response):
        url = response.xpath('//a[span="Read More"]/@href').extract_first()
        corp_name = response.meta['corp_name']

        # http://www.siliconbeat.com
        if re.match(r'http://www.siliconbeat.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_siliconbeat_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://www.latimes.com
        elif re.match(r'http://www.latimes.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_latimes_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://www.investors.com
        elif re.match(r'http://www.investors.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_investors_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://www.investopedia.com
        elif re.match(r'http://www.investopedia.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_investopedia_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://www.insidermonkey.com
        elif re.match(r'http://www.insidermonkey.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_insidermonkey_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://www.fool.com
        elif re.match(r'http://www.fool.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_fool_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://www.capitalcube.com
        elif re.match(r'http://www.capitalcube.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_capitalcube_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://realmoney.thestreet.com
        elif re.match(r'http://realmoney.thestreet.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_thestreet_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://marketrealist.com
        elif re.match(r'http://marketrealist.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_marketrealist_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://247wallst.com
        elif re.match(r'http://247wallst.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_247wallst_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://blogs.barrons.com
        elif re.match(r'http://blogs.barrons.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_barrons_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://fortune.com
        elif re.match(r'http://fortune.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_fortune_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://money.cnn.com
        elif re.match(r'http://money.cnn.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_moneycnn_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://news.investornetwork.com
        elif re.match(r'http://news.investornetwork.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_investornetwork_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://seekingalpha.com
        elif re.match(r'http://seekingalpha.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_seekingalpha_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # https://sgi.seleritycorp.com
        elif re.match(r'https://sgi.seleritycorp.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_seleritycorp_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://www.capitalcube.com
        elif re.match(r'http://www.capitalcube.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_capitalcube_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://www.cnbc.com
        elif re.match(r'http://www.cnbc.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_cnbc_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # https://gigaom.com
        elif re.match(r'https://gigaom.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_gigaom_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://www.usatoday.com
        elif re.match(r'http://www.usatoday.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_usatoday_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://www.moodys.com
        elif re.match(r'http://www.moodys.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_moodys_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://www.mercurynews.com
        elif re.match(r'http://www.mercurynews.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_mercurynews_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://qz.com
        elif re.match(r'http://qz.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_qz_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://www.foxbusiness.com
        elif re.match(r'http://www.foxbusiness.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_foxbusiness_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://www.engadget.com
        elif re.match(r'http://www.engadget.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_engadget_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://www.cnet.com
        elif re.match(r'http://www.cnet.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_cnet_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://wallstcheatsheet.com
        elif re.match(r'http://wallstcheatsheet.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_wallstcheatsheet_contents)
            request.meta['corp_name'] = corp_name
            yield request
        # http://portal.kiplinger.com
        elif re.match(r'http://portal.kiplinger.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_kiplinger_contents)
            request.meta['corp_name'] = corp_name
            yield request
        else:
            return

    # http://www.siliconbeat.com
    def parse_siliconbeat_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//header/h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//span[@class="date D(ib) Fz(11px) Mb(4px)"]/text()').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@id="Col1-0-ContentCanvas-Proxy"]/descendant::text()').extract()[:-1]
        return item

    # http://www.latimes.com
    def parse_latimes_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1[@itemprop="headline"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//time[@itemprop="datePublished"]/@datetime').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@itemprop="articleBody"]/descendant::text()').extract()
        return item

    # http://www.investors.com
    def parse_investors_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1[@class="header1"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//li[@class="post-time"]/text()').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//article/div/descendant::text()').extract()
        return item

    # http://www.investopedia.com
    def parse_investopedia_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//div[@id="Content"]/div[1]/h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//span[@class="by-author "]/text()').extract()[-1].split('|')[-1]
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//article/div[@class="content-box"]/descendant::text()').extract()
        return item

    # http://www.insidermonkey.com
    def parse_insidermonkey_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//article/div[2]/h1/a/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//h6[@class="by-line"]/text()').extract_first().split('on')[-1]
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@class="content-without-wrap entry single-content"]/descendant::text()').extract()
        return item

    # http://www.fool.com
    def parse_fool_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//ul[@class="topic-list"]/li/text()').extract()[1]
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//span[@class="article-content"]/descendant::text()').extract()
        return item

    #http://www.capitalcube.com
    def parse_capitalcube_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//header[@class="entry-header"]/h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//abbr[@class="published"]/@title').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@class="entry-content"]/descendant::text()').extract()
        return item        

    # http://realmoney.thestreet.com
    # need set USER_AGENT
    def parse_thestreet_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//div[@class="headline"]/h2/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//div[@class="date"]/text()').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@class="content"]/descendant::text()').extract()
        return item 

    # http://marketrealist.com
    def parse_marketrealist_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h2[@class="multipart-article-title"]/span/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//span[@class="authored_date"]/text()').extract()[-1]
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@class="article"]/descendant::text()').extract()
        return item         

    # http://247wallst.com
    def parse_247wallst_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1[@class="entry-title"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//span[@class="timestamp"]/text()').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@class="entry-content"]/descendant::text()').extract()
        return item  

    # http://blogs.barrons.com
    def parse_barrons_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//div[@class="articleHeadlineBox headlineType-newswire"]/h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//li[@class="dateStamp first"]/small/text()').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@class="articlePage"]/descendant::text()').extract()
        return item  

    # http://fortune.com
    def parse_fortune_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//time/text()').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//article/descendant::text()').extract()
        return item  

    # http://money.cnn.com
    def parse_moneycnn_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1[@class="article-title"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//span[@class="cnnDateStamp"]/text()').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@id="storytext"]/descendant::text()').extract()
        return item

    # http://news.investornetwork.com
    def parse_investornetwork_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1[@class="entry-title"]/a/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//header[@class="entry-header"]/p/text()').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@class="entry-content"]/descendant::text()').extract()
        return item

    # http://seekingalpha.com
    def parse_seekingalpha_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1[@itemprop="headline"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//time[@itemprop="datePublished"]/text()').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@class="entry-content"]/descendant::text()').extract()
        return item

    # https://sgi.seleritycorp.com
    # http://sgi.seleritycorp.com/4545-2/ OK
    # http://sgi.seleritycorp.com/earnings-preview-adobe-q2-2015-adbe/ error 301
    def parse_seleritycorp_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1[@class="single-post-title"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//div[@class="entry-meta"]/p/text()').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@itemprop="articleBody"]/descendant::text()').extract()
        return item

    # http://www.capitalcube.com
    def parse_capitalcube_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1[@class="entry-title"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//abbr[@class="published"]/@title').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@class="entry-content"]/descendant::text()').extract()
        return item

    # http://www.cnbc.com
    def parse_cnbc_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1[@class="title"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//time[@class="datestamp"]/text()').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@class="story"]/descendant::text()').extract()
        return item

    # https://gigaom.com
    def parse_gigaom_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1[@itemprop="headline"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//time[@itemprop="datePublished"]/text()').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//section[@itemprop="articleBody"]/descendant::text()').extract()
        return item

    # http://www.usatoday.com
    def parse_usatoday_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1[@class="asset-headline"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//span[@class="asset-metabar-time asset-metabar-item nobyline"]/text()').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@itemprop="articleBody"]/descendant::text()').extract()
        return item

    # http://www.moodys.com
    # not precise datetime
    def parse_moodys_contents(self, response):
        if response.status == 301: 
            redirect_url = response.urljoin(response.headers['Location'])
            request = scrapy.Request(redirect_url, callback=self.parse_moodys_contents)
            request.meta['corp_name'] = response.meta['corp_name']
            return request
        else:
            item = CompanynewsItem()
            item['title'] = response.xpath('//span[@class="mdcPageTitle"]/text()').extract_first()
            item['link'] = response.url
            item['datetime'] = response.xpath('//div[@class="mdcBodyHeader"]/text()').extract_first().split('-')[-1]
            item['corp_name'] = response.meta['corp_name']
            item['content'] = response.xpath('//div[@id="wcoArticleCenter"]/descendant::text()').extract()
            return item

    # http://www.mercurynews.com
    def parse_mercurynews_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1[@class="articleTitle"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//div[@id="articleDate"]/text()').extract()[0].split('\t')[-1]
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@id="articleBody"]/descendant::text()').extract()
        return item

    # http://qz.com
    def parse_qz_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1[@itemprop="headline"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//span[@class="timestamp"]/text()').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@class="item-body"]/descendant::text()').extract()
        return item

    # http://www.marketwatch.com    
    def parse_marketwatch_contents(self, response):
        if response.status == 301: 
            redirect_url = response.urljoin(response.headers['Location'])
            request = scrapy.Request(redirect_url, callback=self.parse_marketwatch_contents)
            request.meta['corp_name'] = response.meta['corp_name']
            return request
        else:
            item = CompanynewsItem()
            item['title'] = response.xpath('//h1[@id="article-headline"]/text()').extract_first()
            item['link'] = response.url
            item['datetime'] = response.xpath('//p[@id="published-timestamp"]/span/text()').extract_first()
            item['corp_name'] = response.meta['corp_name']
            item['content'] = response.xpath('//div[@id="article-body"]/descendant::text()').extract()
            return item

    # http://www.foxbusiness.com
    def parse_foxbusiness_contents(self, response):
        if response.status == 302: 
            redirect_url = response.urljoin(response.headers['Location'])
            request = scrapy.Request(redirect_url, callback=self.parse_foxbusiness_contents)
            request.meta['corp_name'] = response.meta['corp_name']
            return request
        else:
            item = CompanynewsItem()
            item['title'] = response.xpath('//h1[@itemprop="headline"]/text()').extract_first()
            item['link'] = response.url
            item['datetime'] = response.xpath('//time[@itemprop="datePublished"]/@datetime').extract_first()
            item['corp_name'] = response.meta['corp_name']
            item['content'] = response.xpath('//div[@class="article-content content"]/descendant::text()').extract()
            return item

    # http://www.engadget.com
    def parse_engadget_contents(self, response):
        if response.status == 301: 
            redirect_url = response.urljoin(response.headers['Location'])
            request = scrapy.Request(redirect_url, callback=self.parse_engadget_contents)
            request.meta['corp_name'] = response.meta['corp_name']
            return request
        else:
            item = CompanynewsItem()
            item['title'] = response.xpath('//h1[@class="t-h4@m- t-h1-b@tp t-h1@tl+ mt-20 mt-15@tp mt-0@m-"]/text()').extract_first()
            item['link'] = response.url
            item['datetime'] = response.xpath('//div[@class="th-meta"]/text()').extract_first()
            item['corp_name'] = response.meta['corp_name']
            item['content'] = response.xpath('//div[@class="article-text c-gray-1"]/descendant::text()|//div[@class="article-text c-gray-1 no-review"]/descendant::text()').extract()
            return item

    # http://www.cnet.com
    def parse_cnet_contents(self, response):
        if response.status == 301: 
            redirect_url = response.urljoin(response.headers['Location'])
            redirect_url = redirect_url.replace('\\', '/')
            request = scrapy.Request(redirect_url, callback=self.parse_cnet_contents)
            request.meta['corp_name'] = response.meta['corp_name']
            return request
        else:
            item = CompanynewsItem()
            item['title'] = response.xpath('//div[@class="articleHead"]/h1/text()').extract_first()
            item['link'] = response.url
            item['datetime'] = response.xpath('//time[@class="timeStamp"]/@content').extract_first()
            item['corp_name'] = response.meta['corp_name']
            item['content'] = response.xpath('//div[@itemprop="articleBody"]/div[@class="col-8"]/descendant::text()').extract()
            return item

    # http://wallstcheatsheet.com
    def parse_wallstcheatsheet_contents(self, response):
        if response.status == 301: 
            redirect_url = response.urljoin(response.headers['Location'])
            request = scrapy.Request(redirect_url, callback=self.parse_wallstcheatsheet_contents)
            request.meta['corp_name'] = response.meta['corp_name']
            return request
        else:
            item = CompanynewsItem()
            item['title'] = response.xpath('//h1[@class="title--article"]/text()').extract_first()
            item['link'] = response.url
            item['datetime'] = response.xpath('//div[@class="pubdate"]/text()').extract_first()
            item['corp_name'] = response.meta['corp_name']
            item['content'] = response.xpath('//section[@class="article__body entry groupclicktrack"]/descendant::text()').extract()
            return item

    # http://portal.kiplinger.com
    def parse_kiplinger_contents(self, response):
        if response.status == 301: 
            redirect_url = response.urljoin(response.headers['Location'])
            request = scrapy.Request(redirect_url, callback=self.parse_kiplinger_contents)
            request.meta['corp_name'] = response.meta['corp_name']
            return request
        else:
            item = CompanynewsItem()
            item['title'] = response.xpath('//h1/text()').extract_first()
            item['link'] = response.url
            item['datetime'] = response.xpath('//meta[@name="PublishDate"]/@content').extract_first()
            item['corp_name'] = response.meta['corp_name']
            item['content'] = response.xpath('//div[@class="kip-slideshow-content"]/descendant::text()').extract()
            return item

#---------------------------------------------parse() for NEWS PROVIDERS end--------------------------------------------    