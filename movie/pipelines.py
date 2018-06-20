# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# wSee: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import json
import redis
from scrapy.exceptions import DropItem


class MoviePipeline(object):
    def process_item(self, item, spider):
        item['summary'] = re.sub('\s+', ' ', item['summary'])
        if not float(item['score'])>=8.0:
            raise DropItem('score less than 8.0')
        self.redis.lpush('douban_movie:items',json.dumps(dict(item)))
        with open('data.json','w') as f:
            json.dump(dict(item),f)
        return item
    
    def open_spider(self,spider):
        self.redis = redis.StrictRedis(host='localhost',port=6379,db=0)
