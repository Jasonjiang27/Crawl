import json

from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


results = []

def parse(response):
    for comment in response.css('div.CommentItem'):
        username = comment.xpath('.//a[@class="UserLink-link"]/text()').extract_first()
        contents = comment.xpath('.//div[@class="RichText ztext CommentItem-content"]/text()').extract_first()
        time = comment.xpath('.//span[@class="CommentItem-time"]/text()').extract_first()
        result = {"username":username,"contents":contents,"time":time}
        results.append(result)


def has_next_page(response):
    page_ex=response.xpath('//botton[contains(@class,"Button PaginationButton PaginationButton-next Button--plain")]/@class').extract_first()
    while page_ex:
        return True

def go_to_next_page(driver):
    next_page_botton=driver.find_element_by_css_selector('button.PaginationButton-next')
    next_page_botton.click()

def wait_page_return(driver,page):
    WebDriverWait(driver,10).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//div[@class="Pagination comments-pagination"]'),
                str(page)
            )
        )

def spider():
    driver = webdriver.PhantomJS()
    url = 'https://zhuanlan.zhihu.com/p/21479334'
    driver.get(url)

    page = 1
    while True:
        wait_page_return(driver,page)
        html = driver.page_source
        response = HtmlResponse(url=url,body=html.encode('utf8'))
        parse(response)
        if not has_next_page(response):
            break
        page+=1
        go_to_next_page(driver)
    with open('/home/shiyanlou/comments.json','w',encoding='utf-8') as f:
        f.write(json.dumps(results))

if __name__=='__main__':
    spider()

