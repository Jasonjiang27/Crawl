# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql     
import json


def dbHandle():
    #连接mysql数据库
    conn = pymysql.connect(
    host = 'localhost',
    user = 'root',   #这里注意用户是root
    db = 'project1',
    passwd = '123_Jiangyaozu',
    charset = 'utf8',
    use_unicode = True
    )
    return conn


class AutoMobilePipeline(object):

    def process_item(self, item, spider):
        # import pdb; pdb.set_trace()
        #写入json文件
        with open('data.json','a') as f:
            json.dump(dict(item),f)

        #连接数据库
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        sql = 'insert into mobile (url,brand,name,price) values (%s,%s,%s,%s)'
        try:
            #用于数据入库后去重
            cursor.execute(
                """select * from mobile where url = %s""",
                item['url'])
            repetition = cursor.fetchone()

            if repetition:
                pass
            else:
                cursor.execute(sql,(item['url'],item['brand'][0],item['name'],item['price'])) 
                dbObject.commit() 

        except Exception,e:
            print e 
            dbObject.rollback() 
        
        return item