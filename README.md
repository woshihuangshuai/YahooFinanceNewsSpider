# YahooFinanceNewsSpider
A web spider written based Scrapy.This spider is aimed to scrape news on Yahoo Finance.

The news is divided into three categories:

 * Sector news

 * Industry news

 * News about companies in S&P500

# Environment

 * Python 2.7
  
 * MongoDB
  
 * Firefox 45.3.0 (The newest Firefox is not supported by Selenium.)
  
 * Scrapy

    [sudo] pip install scrapy / apt install python-scrapy
  
 * Selenium

    [sudo] pip install -U selenium
  
 * Pymongo

    [sudo] pip install pymongo

# News Links

 * Sector News:

    http://finance.yahoo.com/news/sector-basic-materials/?bypass=true
        
 * Industry News:

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
    
    total: 12

 * Company News:

    Companies in S&P 500:
    http://finance.yahoo.com/quote/ + company abbreviations.(eg: BSX; C; )

