#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
获取yahoo finance提供的股票价格数据

数据构成：日期, 开盘时间, 收盘时间, 股价列表
'''

from pymongo import MongoClient
from urllib.request import urlopen
import json
import collections
from YahooFinanceNewsSpider.companies import S_P_500_companies


def ConnectMongoDB():
    client = MongoClient('localhost', 27017)
    return client

def WritetoMongoDB(collection, doc):
    if collection.find_one({'date':doc['date']}) != None:
        return -1
    collection.insert_one(doc)
    return 1

def GetQuote(url):
    docs = []
    series = []
    date = []
    timestamp_min = []
    timestamp_max = []
    quote_list = []

    try:
        response = urlopen(url).read().decode('utf-8').split('(')[1].split(')')[0]
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
    index = 0
    for quote in series:
        if quote['Timestamp'] > timestamp_max[index]:
            document = collections.OrderedDict()
            document['date']    = date[index]
            document['min']     = timestamp_min[index]
            document['max']     = timestamp_max[index]
            document['quote']   = quote_list
            docs.append(document)
            quote_list = []
            index += 1
        quote_list.append(quote)

    document = collections.OrderedDict()
    document['date']    = date[index],
    document['min']     = timestamp_min[index]
    document['max']     = timestamp_max[index]
    document['quote']   = quote_list
    docs.append(document)

    return docs

if __name__ == '__main__':
    timerange = 20 #day

    for company in S_P_500_companies:
        client = ConnectMongoDB()
        db = client['Quote']
        collection = db[company]
        url = 'http://chartapi.finance.yahoo.com/instrument/1.0/%s/chartdata;type=quote;range=%dd/json' % (company, timerange)
        docs = GetQuote(url)
        if docs != None:
            for doc in docs:
                WritetoMongoDB(collection, doc)
        else:
            print('ERROR: Can\'t get quote of', company)
        client.close()


        
