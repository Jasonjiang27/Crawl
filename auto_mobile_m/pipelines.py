# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from model import CarPrice
#import pymongo


class AutoMobileMPipeline(object):

    '''def __init__(self):

    # pymongo 链接数据库
    self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
    # 数据库登录需要帐号密码的话
    # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
    self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
    self.coll = self.db[settings['MONGO_COLL']]  # 获得collection的句柄'''

    def process_item(self, item, spider):
        #postItem = dict(item)  #把item转化成字典形式
        cp = CarPrice()#实例化对象
        cp['url'] = item['url']
        cp['brand'] = item['brand'][0]
        cp['name'] = item['name']
        cp['price'] = item['price']
        cp.save()  #最后必须save