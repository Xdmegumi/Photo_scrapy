# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 21:16:33 2018

@author: Xdmegumi
"""

from urllib.request import urlopen, quote
from bs4 import BeautifulSoup
import xlwt
import requests
import re
import datetime
import urllib
import argparse
import time
from subprocess import call

#获取代码运行的起始时间
since = time.time()

#增加命令行参数
usage="Download images from yande"
parser = argparse.ArgumentParser()

parser.add_argument("-t","--tags",dest='tags',default='',help='The tag you want to download')
parser.add_argument("-r","--recent",dest='recent',default=20,help='download the recent images')
parser.add_argument("-p","--pages",type=int,dest='pages', default=5, help='the number of pages you want to download')

#定义参数
args = parser.parse_args()
tags=args.tags
recent=args.recent
pages=args.pages

#获取网页的html文件
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

def getlinks(html,tags):
    soup = BeautifulSoup(html,"lxml")
    pattern = re.compile('/post/show/(.*?),',re.S)
    sh=[]
    # imglist = pattern.findall(soup.find_all('li'))
    i=0
    # 搜索所有<a>
    soup_li=soup.find_all("a")
    for soup_l in soup_li:
        # 得到网页下所有'href'链接，并转换为str
        x=soup_l.get('href')
        # 将各个x拼接成list
        sh.append(x)
    # print(imglist)
    # 过滤掉所有的None
    sh = filter(None, sh)
    # 重新拼接成str
    strr = ",".join(sh)
    imgid = pattern.findall(strr)
    print(imgid)
    for i in range(len(imgid)):
        url=model+'/'+imgid[i]
        html=get_one_page(url)
        imglist=getAllImg(html)
        output=tags+'.txt'
        #if len(imglist)!=0:
            #f = open(output, "a", encoding='utf-8')
        links=imglist[0]#+'\n'
        DownPath = 'D:\FDMdownload'
        call([IDM, '/d',links, '/p',DownPath, '/n'])
            #f.write(links)
            #f.close()
    time_elapsed = time.time() - since
    #输出每一个页面的代码运行时间
    print('The code run {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
    return imgid

IDM='C:\IDM\IDMan.exe'

#yande主页
model = 'https://yande.re/post/show'
#yande的tag页
model_2 = 'https://yande.re/post?tags='
url_2=model_2+tags
if len(tags)==0:
    max=recent
    i=1
    url=model
    while i<max:
        html=get_one_page(url)
        today=datetime.date.today()
        getlinks(html,today)
    
    
else:
    html=get_one_page(url_2)
    getlinks(html,tags)
    i=2;
    while True:
        model_2='https://yande.re/post?'+'page='+str(i)+'&'+'tags='
        url_2=model_2+tags
        html=get_one_page(url_2)
        imgid=getlinks(html,tags)
        #判断是否为空页，或已经运行完所有页面
        if len(imgid)==0 or i>=pages:
            break
        i += 1
    