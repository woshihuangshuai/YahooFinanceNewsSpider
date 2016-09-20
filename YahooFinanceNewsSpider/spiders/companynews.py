# -*- coding: utf-8 -*-
import scrapy
import re
from YahooFinanceNewsSpider.items import CompanynewsItem
from selenium import webdriver
import time
from YahooFinanceNewsSpider.companies import S_P_500_companies

'''
    3 kinds of links:

        https://finance.yahoo.com/news/...
        https://finance.yahoo.com/m/...
        https://finance.yahoo.com/video/...

        Other links are advertisements.

    News Providers:

        NORMAL:
            Capital Cube(eg: http://www.capitalcube.com/blog/index.php/tal-education-group-price-momentum-supported-by-strong-fundamentals/)
            CNBC(eg: http://www.cnbc.com/2016/09/17/explosion-injuries-reported-in-nycs-chelsea-section.html?__source=yahoo%7Cfinance%7Cheadline%7Cheadline%7Cstory&par=yahoo&doc=103948195)
            Engadget(eg: https://www.engadget.com/2016/09/07/nintendo-loses-a-little-piece-of-its-identity-with-super-mario/?ncid=txtlnkusaolp00000589)
            Fortune(eg: http://fortune.com/2015/11/04/tech-job-buzzwords/?xid=yahoo_fortune)
            Gigaom(eg: https://gigaom.com/2016/09/12/fluke-briefing-report-closing-the-gap-between-things-and-reality/?utm_medium=content&utm_campaign=syndication&utm_source=yfinance&utm_content=fluke-briefing-report-closing-the-gap-between-things-and-reality_950831
            https://gigaom.com/2016/09/07/welcome-to-the-post-email-enterprise-what-skype-teams-means-in-a-slack-centered-world/?utm_medium=content&utm_campaign=syndication&utm_source=yfinance&utm_content=welcome-to-the-post-email-enterprise-what-skype-teams-means-in-a-slack-centered-world_950811)
            Investopedia(eg: http://www.investopedia.com/articles/company-insights/091816/how-blockchain-technology-could-free-billions-banks-ubs-bk.asp?partner=YahooSA)
            Investor's Business Daily(eg: http://www.investors.com/news/technology/apple-supplier-cirrus-logic-delivers-perfect-example-of-a-reversal/
            http://www.investors.com/politics/editorials/will-terrorist-attacks-be-the-new-normal/)
            Kiplinger(eg: http://www.kiplinger.com/article/investing/T018-C008-S001-3-dividend-paying-tech-stocks-selling-at-a-bargain.html?rid=SYN-yahoo&rpageid=15473
            http://wealth.kiplinger.com/reader/kiplinger/do-low-volatility-products-belong-in-your-portfolio)
            Los Angeles Times(eg: http://www.latimes.com/entertainment/envelope/cotown/la-et-ct-sully-blair-witch-bridget-jones-20160908-snap-story.html)
            Market Realist(eg: http://marketrealist.com/2016/09/clarcor-to-become-sole-supplier-for-ge-filtration-system/?utm_source=yahoo&utm_medium=feed)
            MarketWatch(eg: http://www.marketwatch.com/story/the-points-guy-brian-kelly-once-you-fly-first-class-you-cant-go-back-to-coach-2016-09-15?siteid=yhoof2
            http://www.marketwatch.com/video/bodyhackers-implant-rfid-chips-to-customize-themselves/3CCB4569-D6FF-4D05-A5A0-CB63BB9D295A.html)     
            Moody's(eg: https://www.moodys.com/research/Moodys-assigns-Aa2-rating-to-Lexington-Fayette-Urban-County-Airport--PR_903546105?WT.mc_id=AM~WWFob29fRmluYW5jZV9TQl9SYXRpbmcgTmV3c19BbGxfRW5n~20160916_PR_903546105)
            Morningstar(eg: http://news.morningstar.com/articlenet/article.aspx?id=769337&SR=Yahoo)   
            San Jose Mercury News(eg: http://www.siliconbeat.com/2016/09/16/proposed-oakland-school-wins-10m-national-contest-backed-laurene-powell-jobs/)
            Selerity Global Insight(eg: https://sgi.seleritycorp.com/earnings-preview-bed-bath-beyond-q2-2016-bbby/)
            TechCrunch(eg: https://techcrunch.com/2016/09/18/higher-education-goes-hollywood/?ncid=txtlnkusaolp00000591)
            TechRepublic(eg: http://www.techrepublic.com/article/an-excel-conditional-format-that-expands-with-grouped-data/#ftag=YHF87e0214)
            USA TODAY(eg: http://www.usatoday.com/story/money/2016/06/14/chick-fil-a-opens-on-sunday-to-feed-orlando-blood-donors/85868494/
            http://247wallst.com/special-report/2016/06/15/50-mcdonalds-menu-items-with-the-most-calories/)
            ZD Net(eg: http://www.zdnet.com/article/new-relic-hires-its-first-chief-information-officer/#ftag=YHFb1d24ec)
            TheStreet(WARNING: need change USER_AGENT as a explore. 
            eg: http://realmoney.thestreet.com/articles/09/18/2016/cracks-are-widening-financials-charts?puc=yahoo&cm_ven=YAHOO)

        ERROR:
            American City Business Journals(ERROR:Access To Website Blocked.)
            Barrons.com(WARNING: need login. eg: http://www.barrons.com/articles/home-builder-calatlantics-shares-have-room-to-grow-1474096055?mod=yahoobarrons&ru=yahoo)
            Bloomberg(ERROR: There is nothing on this website.)
            CNNMoney.com（ERROR: GFW）
            Money(ERROR: GFW)
            The Wall Street Journal(ERROR: GFW)
            Financial Times(ERROR: need login. eg: https://www.ft.com/content/a879bd44-7df8-11e6-8e50-8ec15fb462f4?ftcamp=traffic/partner/feed_headline/us_yahoo/auddev)
            Forbes(ERROR: get nothing by spider. eg: http://www.forbes.com/sites/panosmourdoukoutas/2016/09/18/indias-semi-soviet-semi-latin-model/?utm_source=yahoo&utm_medium=partner&utm_campaign=yahootix&partner=yahootix#3b9995ee6d45)

        urls of these website start with http(s)://finance.yahoo.com/news/...
            Accesswire(Collected by Yahoo)
            AP(Collected by Yahoo)
            The Atlantic(Collected by Yahoo)
            Bankrate.com(Collected by Yahoo)
            Benzinga(Collected by Yahoo)
            Business Insider(Collected by Yahoo)
            Business Wire(Collected by Yahoo)
            BusinessWeek(Collected by Yahoo)
            CBS Moneywatch(Collected by Yahoo)
            CNW Group(Collected by Yahoo)
            Consumer Reports(Collected by Yahoo)
            Credit.com(Collected by Yahoo)
            CreditCards.com(Collected by Yahoo)
            DailyFX(Collected by Yahoo)
            DailyWorth(Collected by Yahoo)
            Entrepreneur(Collected by Yahoo)
            ETF Trends(Collected by Yahoo)
            ETFguide(Collected by Yahoo)
            The Fiscal Times(Collected by Yahoo)
            Fox Business(Collected by Yahoo)
            GlobeNewswire(Collected by Yahoo)
            GuruFocus(Collected by Yahoo)
            Marketwired(Collected by Yahoo)
            Money Talks News(Collected by Yahoo)
            MrTopStep(Collected by Yahoo)
            optionMONSTER(Collected by Yahoo)
            PR Newswire(Collected by Yahoo)
            Reuters(Collected by Yahoo)
            Thomson Reuters ONE(Collected by Yahoo)
            US News & World Report(Collected by Yahoo)
            Zacks(Collected by Yahoo)
            Zacks Small Cap Research(Collected by Yahoo)
'''

class CompanynewsSpider(scrapy.Spider):
    name = "companynews"

    download_delay = 2

    # start_urls = [
    #     "https://finance.yahoo.com/quote/BSX", 
    #     "https://finance.yahoo.com/quote/C"
    # ]

    start_urls = ['https://finance.yahoo.com/quote/' + company for company in S_P_500_companies]

    def parse(self, response):
        corp_name = response.url.split('/')[-1]
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
            if re.match(r'https?://finance.yahoo.com/news/.*', url) != None: 
                request = scrapy.Request(url, callback=self.parse_yahoo_news_contents)
                request.meta['corp_name'] = corp_name
                yield request
            elif re.match(r'https?://finance.yahoo.com/video/.*', url) != None:
                request = scrapy.Request(url, callback=self.parse_yahoo_video_contents)
                request.meta['corp_name'] = corp_name
                yield request
            elif re.match(r'https?://finance.yahoo.com/m/.*', url) != None:
                request = scrapy.Request(url, callback=self.parse_outside_url)
                request.meta['corp_name'] = corp_name
                yield request
            else:
                continue
# ---------------------------------- Major Component of  this Spider is over -----------------------------------

    # parse the news content from finance.yahoo.com/news/
    def parse_yahoo_news_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//header/h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//time[@class="date D(ib) Fz(11px) Mb(4px)"]/@datetime').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@id="Col1-0-ContentCanvas-Proxy"]/descendant::text()').extract()[:-1]
        return item
        
    # parse the news content from finance.yahoo.com/video/
    def parse_yahoo_video_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.xpath('//time[@class="date D(ib) Fz(11px) Mb(4px)"]/@datetime').extract_first()
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//p/descendant::text()').extract()
        return item

# ---------------------------------- get urls link to other website. START ------------------------------------
    def parse_outside_url(self, response):
        url = response.xpath('//a[span="Read More"]/@href').extract_first()
        print 'Parsing:', url

        datetime = response.xpath('//time[@class="date D(ib) Fz(11px) Mb(4px)"]/@datetime').extract_first()
        corp_name = response.meta['corp_name']

        # http://www.capitalcube.com
        if re.match(r'https?://www.capitalcube.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_capitalcube_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request

        # http://www.cnbc.com
        elif re.match(r'https?://www.cnbc.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_cnbc_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request

        # http://www.engadget.com
        elif re.match(r'https?://www.engadget.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_engadget_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request

        # https://www.forbes.com/
        elif re.match(r'https?://www.forbes.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_ft_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request

        # https://gigaom.com
        elif re.match(r'https?s://gigaom.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_gigaom_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request

        # http://www.investopedia.com
        elif re.match(r'https?://www.investopedia.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_investopedia_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request

        # http://www.investors.com
        elif re.match(r'https?://www.investors.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_investors_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request

        # http://portal.kiplinger.com
        elif re.match(r'https?://.*.kiplinger.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_kiplinger_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request

        # http://www.latimes.com
        elif re.match(r'https?://www.latimes.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_latimes_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request

        # http://marketrealist.com
        elif re.match(r'https?://marketrealist.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_marketrealist_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request

        # http://www.marketwatch.com/
        elif re.match(r'https?://www.marketwatch.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_marketrealist_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request

        # http://www.moodys.com
        elif re.match(r'https?://www.moodys.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_moodys_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request

        # http://news.morningstar.com/
        elif re.match(r'https?://news.morningstar.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_morningstar_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request

        # http://www.siliconbeat.com
        if re.match(r'https?://www.siliconbeat.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_siliconbeat_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request

        # https://sgi.seleritycorp.com
        elif re.match(r'https?s://sgi.seleritycorp.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_seleritycorp_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request

        # https://techcrunch.com/
        elif re.match(r'https?s://techcrunch.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_techcrunch_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request

        # http://www.techrepublic.com/
        elif re.match(r'https?s://www.techrepublic.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_techcrunch_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request

        # http://www.usatoday.com
        elif re.match(r'https?://www.usatoday.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_usatoday_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request

        # http://247wallst.com
        elif re.match(r'https?://247wallst.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_247wallst_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request

        # http://www.zdnet.com/
        elif re.match(r'https?://www.zdnet.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_zdnet_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request

        # http://realmoney.thestreet.com
        elif re.match(r'https?://realmoney.thestreet.com/.*', url) != None: 
            request = scrapy.Request(url, callback=self.parse_thestreet_contents)
            request.meta['corp_name'] = corp_name
            request.meta['datetime'] = datetime
            yield request
        else:
            return

# ---------------------------------- get urls link to other website. END --------------------------------------


# ------------------------------------- parse() for NEWS PROVIDERS START --------------------------------------
    #http://www.capitalcube.com
    def parse_capitalcube_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//header[@class="entry-header"]/h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.meta['datetime']
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@class="entry-content"]/descendant::text()').extract()
        return item 

    # http://www.cnbc.com
    def parse_cnbc_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1[@class="title"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.meta['datetime']
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@class="story"]/descendant::text()').extract()
        return item

    # http://www.engadget.com
    def parse_engadget_contents(self, response):
        if response.status != 200: 
            redirect_url = response.urljoin(response.headers['Location'])
            request = scrapy.Request(redirect_url, callback=self.parse_engadget_contents)
            request.meta['corp_name'] = response.meta['corp_name']
            return request
        else:
            item = CompanynewsItem()
            item['title'] = response.xpath('//h1[@class="t-h4@m- t-h1-b@tp t-h1@tl+ mt-20 mt-15@tp mt-0@m-"]/text()').extract_first()
            item['link'] = response.url
            item['datetime'] = response.meta['datetime']
            item['corp_name'] = response.meta['corp_name']
            item['content'] = response.xpath('//div[@class="article-text c-gray-1"]/descendant::text()|//div[@class="article-text c-gray-1 no-review"]/descendant::text()').extract()
            return item

    # http://fortune.com
    def parse_fortune_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.meta['datetime']
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//article/descendant::text()').extract()
        return item  

    # https://gigaom.com
    def parse_gigaom_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1[@itemprop="headline"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.meta['datetime']
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//section[@itemprop="articleBody"]/descendant::text()').extract()
        return item

    # http://www.investopedia.com
    def parse_investopedia_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//div[@id="Content"]/div[1]/h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.meta['datetime']
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//article/div[@class="content-box"]/descendant::text()').extract()
        return item

    # http://www.investors.com
    def parse_investors_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1[@class="header1"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.meta['datetime']
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//article/div/descendant::text()').extract()
        return item

    # http://portal.kiplinger.com
    def parse_kiplinger_contents(self, response):
        if response.status == 301: 
            redirect_url = response.urljoin(response.headers['Location'])
            request = scrapy.Request(redirect_url, callback=self.parse_kiplinger_contents)
            request.meta['corp_name'] = response.meta['corp_name']
            request.meta['datetime'] = response.meta['datetime']
            return request
        else:
            item = CompanynewsItem()
            item['title'] = response.xpath('//h1/text()').extract_first()
            item['link'] = response.url
            item['datetime'] = response.meta['datetime']
            item['corp_name'] = response.meta['corp_name']
            item['content'] = response.xpath('//div[@class="kip-column-content kip-column-page1"]/descendant::text()').extract()
            return item

    # http://www.latimes.com
    def parse_latimes_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1[@itemprop="headline"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.meta['datetime']
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@itemprop="articleBody"]/descendant::text()').extract()
        return item

    # http://marketrealist.com
    def parse_marketrealist_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1/span/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.meta['datetime']
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@class="article"]/descendant::text()').extract()
        return item   

    # http://www.marketwatch.com    
    def parse_marketwatch_contents(self, response):
        if response.status == 301: 
            redirect_url = response.urljoin(response.headers['Location'])
            request = scrapy.Request(redirect_url, callback=self.parse_marketwatch_contents)
            request.meta['corp_name'] = response.meta['corp_name']
            request.meta['datetime'] = response.meta['datetime']
            return request
        else:
            item = CompanynewsItem()
            item['title'] = response.xpath('//h1/text()').extract_first()
            item['link'] = response.url
            item['datetime'] = response.meta['datetime']
            item['corp_name'] = response.meta['corp_name']
            item['content'] = response.xpath('//article//descendant::text()').extract()
            return item 

    # http://www.moodys.com
    def parse_moodys_contents(self, response):
        if response.status == 301: 
            redirect_url = response.urljoin(response.headers['Location'])
            request = scrapy.Request(redirect_url, callback=self.parse_moodys_contents)
            request.meta['corp_name'] = response.meta['corp_name']
            request.meta['datetime'] = response.meta['datetime']
            return request
        else:
            item = CompanynewsItem()
            item['title'] = response.xpath('//span[@class="mdcPageTitle"]/text()').extract_first()
            item['link'] = response.url
            item['datetime'] = response.meta['datetime']
            item['corp_name'] = response.meta['corp_name']
            item['content'] = response.xpath('//div[@id="wcoArticleCenter"]/descendant::text()').extract()
            return item

    # http://news.morningstar.com
    def parse_morningstar_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.meta['datetime']
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@id="mstarContent"]/descendant::text()').extract()
        return item

    # http://www.siliconbeat.com
    def parse_siliconbeat_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.meta['datetime']
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@class="post-content"]/p/descendant-or-self::text()').extract()
        return item

    # https://sgi.seleritycorp.com
    def parse_seleritycorp_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1[@class="single-post-title"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.meta['datetime']
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@class="entry-content"]/descendant::text()').extract()
        return item

    # https://techcrunch.com/
    def parse_techcrunch_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.meta['datetime']
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@class="l-main"]//p/descendant-or-self::text()').extract()
        return item

    # http://www.techrepublic.com/
    def parse_techcrunch_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.meta['datetime']
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@class="content"]/descendant::text()').extract()
        return item

    # http://www.usatoday.com
    def parse_usatoday_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1[@class="asset-headline"]/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.meta['datetime']
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@itemprop="articleBody"]/p/descendant-or-self::text()').extract()
        return item

    # http://247wallst.com
    def parse_247wallst_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.meta['datetime']
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@class="entry-content"]/p/descendant-or-self::text()').extract()
        return item  

    # http://www.zdnet.com/
    def parse_zdnet_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//h1/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.meta['datetime']
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//article//p/descendant-or-self::text()').extract()
        return item  

    # http://realmoney.thestreet.com
    # need set USER_AGENT
    def parse_thestreet_contents(self, response):
        item = CompanynewsItem()
        item['title'] = response.xpath('//div[@class="headline"]/h2/text()').extract_first()
        item['link'] = response.url
        item['datetime'] = response.meta['datetime']
        item['corp_name'] = response.meta['corp_name']
        item['content'] = response.xpath('//div[@class="content"]/p/descendant-or-self::text()').extract()
        return item 

# ------------------------------------- parse() for NEWS PROVIDERS END ----------------------------------------