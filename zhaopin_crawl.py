
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests  
import jieba
import csv
from bs4 import BeautifulSoup
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt

def get_one(num):  

   my_headers = {  
   'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',  
   'Host':'www.job910.com'
   }  
 
   url = "http://www.job910.com/search.aspx?funtype=11&sortField=1&sort=0&pageSize=20&pageIndex="+str(num)+"&salary=&maxSalary=&minSalary=&workMethod=&education=&experience=&uptime=0&keyword=%E6%95%B0%E5%AD%A6&area=310000"
   try:
       res = requests.get(url, headers = my_headers, timeout=10)
       if res.status_code == 200:
           return res.text

   except:
       return None

def parse_page(html):
    soup = BeautifulSoup(html,"html.parser")
    infos = soup.find('ul',{'class':"search-result-list"}).find_all('li')
    job_items = []
    for info in infos:
        job_name = info.find('div',{'class':"info-col-1st"}).a.string.strip()
        detail_info_link = "http://www.job910.com"+info.find('div',{'class':"info-col-1st"}).a["href"]
        detail = requests.get(detail_info_link)
        soup1 = BeautifulSoup(detail.text, "lxml")
        welfares = soup1.find('div',{"class":"jobs-desc"}).find_all('div',{'class':'desc-wrap'})[1].strings
        li1 = []
        for i in welfares:
            li1.append(i)
        welfare = ",".join(li1[2:-1]).strip()
        
        ziges = soup1.find('div',{"class":"jobs-desc"}).find_all('div',{'class':'desc-wrap'})[0].strings
        li2 = []
        for i in ziges:
            li2.append(i)
        zige = ",".join(li2).strip()
        
        area = info.find('div',{'class':"info-col-1st"}).find('div',{"class":"area title2"}).string.strip()
        salary = info.find('div',{'class':"info-col-2nd"}).find('div',{"class":"salary title"}).string.strip()
        publish_time = info.find('div',{'class':"info-col-2nd"}).find('div',{"class":"time title2"}).string.strip()
        company_name = info.find('div',{'class':"info-col-3rd"}).a.string.strip()
        company_info_link = "http://www.job910.com"+info.find('div',{'class':"info-col-3rd"}).a["href"]
        demand = info.find('div',{'class':"info-col-3rd"}).find('div',{'class':"exp title2"}).string.strip()
        job_dict = {
                "学校名称":company_name,
                "工作名称":job_name,
                "详细情况链接":detail_info_link,
                "学校地点":area,
                "工资":salary,
                "福利":welfare,
                "发布日期":publish_time,
                "学校介绍链接":company_info_link,
                "应聘要求":demand
        }
        job_items.append(job_dict)
    return job_items,zige

def generate_wordcloud(txt):
    cut_text = ' '.join(jieba.cut(txt))  
    color_mask = plt.imread('C:\\Users\\jyz\\Desktop\\timg.jpg')  #设置背景图  
    print('加载图片成功！')
    cloud = WordCloud(  
            font_path = 'simhei.ttf',   
            background_color = 'white',  
            mask = color_mask,
            max_words = 1000,  
            max_font_size = 100          
            )  
    
    cloud.generate_from_text(cut_text)
    img_colors = ImageColorGenerator(color_mask)
    cloud.recolor(color_func=img_colors)

    # 保存词云图片 
    cloud.to_file('C:\\Users\\jyz\\Desktop\\word_cloud.jpg')
    
def write_csv_headers(path, headers):
   '''
   写入表头
   '''
   with open(path, 'a', encoding='gb18030', newline='') as f:
       f_csv = csv.DictWriter(f, headers)
       f_csv.writeheader()
    
def write_csv_rows(path, headers, rows):
    with open(path, 'a', encoding='gb18030', newline='') as f:
       f_csv = csv.DictWriter(f, headers)
       f_csv.writerows(rows)
       
def main():
   '''
   主函数
   '''
   filename = 'C:\\Users\\jyz\\Desktop\\上海中小学数学教师求职信息.csv'
   headers = [ "学校名称","工作名称", "详细情况链接", "学校地点", "工资","福利", "发布日期","学校介绍链接","应聘要求"]
   write_csv_headers(filename, headers)
   jobs = []
   txt_list = []
   for i in range(1,7):
       '''
       获取该页中所有职位信息，写入csv文件
       '''
       
       html = get_one(i)
       items = parse_page(html)[0]
       txt = parse_page(html)[1]
       print(txt)
       for item in items:
           jobs.append(item)
       
    
       txt_list.append(txt)
       print("完成第%d页".format(i))
   generate_wordcloud(','.join(txt_list))
   print("加载图片完成")
   write_csv_rows(filename, headers, jobs)
       

if __name__ == '__main__':
        main()
        

