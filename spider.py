#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

results =[]


def parse(response):
    for comment in response.css('div.comment-item-wrapper'):
        username = comment.xpath('.//a[@class="username"]/text()').re_first('\n\s*(.*)\s*')
        content = comment.xpath('.//div[contains(@class,"comment-item-content")]/p/text()').extract_first()
        result = {"username":username,"content":content}
        print('---------------',result)
        results.append(result)

def has_next_page(response):
    page_ex = response.xpath('//li[contains(@class,"next-page")]/@class').extract_first()
    if 'disabled' not in page_ex:
        return True
    else:
        return False

def goto_next_page(driver):
    next_page_botton = driver.find_element_by_xpath('//li[contains(@class,"next-page")]')
    next_page_botton.click()


def wait_page_return(driver,page):
    WebDriverWait(driver,10).until(
            EC.text_to_be_present_in_element(
                (By.XPATH,'//ul[@class="pagination"]/li[@class="active"]'),
                str(page)
            )
        )

def spider():
    #创建webdriver
    driver = webdriver.PhantomJS()
    #获取第一个页面
    url = 'https://www.shiyanlou.com/courses/427'
    driver.get(url)
    page = 1
    while True:
        #加载评论第一页
        wait_page_return(driver,page)
        #获取源码
        html = driver.page_source
        #构建htmlresponse对象获取评论数据
        response = HtmlResponse(url=url,body=html.encode('utf8'))
        #解析HtmlResponse对象获取评论数据
        parse(response)
        #如果是最后一页则停止获取评论数据
        if not has_next_page(response):
            break
        #进入到下一页
        page += 1
        goto_next_page(driver)
    #将results使用json序列化后写入文件
    with open('/home/shiyanlou/comments.json','w') as f:
        f.write(json.dumps(results))

if __name__ == '__main__':
    spider()
