# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from douban_movie.items import MovieItem


class AwesomeMovieSpider(scrapy.Spider):
    name = 'awesome_movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/subject/3011091/']
    rules= (
            Rule(LinkExtract(allow='https://movie.douban.com/subject/\d+/?from=subject-page'),callback='parse_item',follow=True), 
            )

    def parse_movie_item(self,response):
        item=PageItem()
        item['url']=response.url
        item['name']=response.xpath('//span[@property="v=itemreviewed"/text()').extract_first()
        item['summary']=response.xpath('span[@class="all hidden"]/text()').extract_first()
        item['score']=response.xpath('//strong[@class=ll rating_num]/text()').extract_first()
        if int(item['score'])>=8.0:
            return item
    def parse_start_url(self,response):
        yield self.parse_movie_item(response)


    def parse_page(self, response):
        yield self.parse_movie_item(response)

