# -*- coding: utf-8 -*-
import scrapy

from auto_mobile_m.items import AutoMobileMItem


class MobileSpider(scrapy.spiders.Spider):
    name = 'mobile'
    #allowed_domains = ['pcauto.com.cn']
    start_urls = ['http://www.pcauto.com.cn/']

    #解析初始页面，获得进一步追随页面
    def parse(self, response):
        item_urls = response.xpath('//dl[@id="slide-hots1"]//a[@class="hots-tab-carName"]/@href').extract()#获得所有需进入的url
        for url in item_urls:  
            yield scrapy.Request(url, callback=self.parse_item)
    
    #解析内容页面
    def parse_item(self, response):

        items = AutoMobileMItem()
        items['url'] = response.url
        bd=response.xpath('//div[@class="title"]/h1/text()').extract_first()
        #print bd
        #print '-----------------------------------------------------'
        items['brand'] = bd.split("-")[:-1]#吃出应该是[0]，只提取第一个，否则结果还是一个列表
        items['name'] = bd.split("-")[-1]
        #text_price = response.xpath('//p[@class="p1"]/em/text()').extract_first()
        #items['price'] = text_price[:-1]
        items['price'] = response.xpath('//p[@class="p1"]/em/text()').extract_first()
        yield items
        
