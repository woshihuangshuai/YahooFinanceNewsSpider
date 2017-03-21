#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
获取yahoo finance提供的股票价格数据

数据构成：日期, 开盘时间, 收盘时间, 股价列表
'''

from pymongo import MongoClient
from urllib.request import urlopen
from YahooFinanceNewsSpider.companies import S_P_500_companies
import json
import collections
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='getYahooQuote.log',
                    filemode='w')

# 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def ConnectMongoDB():
    client = MongoClient('localhost', 27017)
    db = client['Quote']
    collection = db['YahooFinanceQuote']
    return collection


def WritetoMongoDB(collection, doc):
    query = {'$and': [
            {'company':   doc['company']},
            {'date':   doc['date']}
    ]}

    cursor = collection.find_one(query)
    if cursor != None:
        print(cursor['company'], '\t', cursor['date'], '\t', 'is existed.')
        return -1

    collection.insert_one(doc)
    return 1


def GetQuote(company, url):
    company_name = company
    docs = []
    series = []
    date = []
    timestamp_min = []
    timestamp_max = []
    quote_list = []

    try:
        response = urlopen(url).read().decode(
            'utf-8').split('(')[1].split(')')[0]
        responsejson = json.loads(response)
        TimeStampRanges = responsejson.get('TimeStamp-Ranges')
        if TimeStampRanges == None:
            raise e
    except Exception as e:
        return None

    for timestamp in TimeStampRanges:
        date.append(timestamp['date'])
        timestamp_min.append(timestamp['min'])
        timestamp_max.append(timestamp['max'])

    series = responsejson.get('series')
    if series == None:
        return None

    index = 0
    for quote in series:
        try:
            if quote['Timestamp'] > timestamp_max[index]:
                document = collections.OrderedDict()
                document['company'] = company_name
                document['date'] = date[index]
                document['min'] = timestamp_min[index]
                document['max'] = timestamp_max[index]
                document['quote'] = quote_list
                docs.append(document)
                quote_list = []
                index += 1
            quote_list.append(quote)
        except Exception as e:
            print(e)
            return None

    document = collections.OrderedDict()
    document['company'] = company_name
    document['date'] = date[index]
    document['min'] = timestamp_min[index]
    document['max'] = timestamp_max[index]
    document['quote'] = quote_list
    docs.append(document)

    return docs


if __name__ == '__main__':
    collection = ConnectMongoDB()
    timerange = 20
    for company in S_P_500_companies:
        url = 'http://chartapi.finance.yahoo.com/instrument/1.0/%s/chartdata;type=quote;range=%dd/json' % (
            company, timerange)
        docs = GetQuote(company, url)
        if docs != None:
            for doc in docs:
                WritetoMongoDB(collection, doc)
        else:
            logging.debug('ERROR: Can\'t get quote of ' + company)
            print('ERROR: Can\'t get quote of', company)
