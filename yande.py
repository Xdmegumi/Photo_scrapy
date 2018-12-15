# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 14:00:54 2018

@author: Xdmegumi
"""

from urllib.request import urlopen, quote
from geopy.geocoders import baidu
from bs4 import BeautifulSoup
import xlwt
import requests
import re
import json
import urllib

# 根据给定的网址来获取网页详细信息，得到的html就是网页的源代码
model = 'https://yande.re/post/show'
i = 499843
Max = 499876
Retry_max = 10
count = 0
    
def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/51.0.2704.63 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.text
        else:
            print(response.status_code)
            return None
    except:
        print('访问http发生错误... ')
        return None
    
def getAllImg(html):
    # 利用正则表达式把源代码中的图片地址过滤出来
    pattern = re.compile('<a class="original-file-changed" id="highres" href="(.*?)">Download.*?larger.*?version.*?</a>',re.S)
    imglist = pattern.findall(html)  # 表示在整个网页中过滤出所有图片的地址，放在imglist中
    return imglist

        # 获取网页中所有图片的地址
while i == 499843:
    url=model+'/'+str(i)
    i += 1
    html=get_one_page(url)
    imglist=getAllImg(html)
    soup = BeautifulSoup(html)
    print(soup.prettify())
    if len(imglist)!=0:
        print(imglist[0])