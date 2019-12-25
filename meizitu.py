# -*- coding:utf-8 -*-
import requests
import os
import time
import threading
import re
from bs4 import BeautifulSoup


# 发送http请求
def sendHttp(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
               "Referer": url}
    r = requests.get(url, headers=headers)  # 增加headers, 模拟浏览器
    return r.text


# 获取总页数的标记
def getMaxPage(url):
    soup = BeautifulSoup(sendHttp(url), 'html.parser')
    con = soup.find_all("a", class_="page-numbers")
    ## 获取最大的一个总页数
    maxPageText = []
    for i in con:
        maxPageText.append(i.get_text())

    pageSize = 0
    for i in maxPageText:
        data = re.findall(r'(\w*[0-9]+)\w*', i)
        try:
            dataNum = int(data[0])
        except:
            pass
        else:
            if pageSize <= dataNum:
                pageSize = dataNum
    return pageSize


# 获取出列表页的列表预览
def get_pic_list(url):
    pic_list = []
    html = sendHttp(url)
    soup = BeautifulSoup(html, 'html.parser')
    pull_list = soup.find(id='pins').find_all('li')
    for i in pull_list:
        linkText = i.find("a")
        picText = i.find("img")
        link = linkText.get('href')  # 套图链接
        text = picText.get('alt')  # 套图名字
        data = {"link": link, "title": text}
        # get_pic(link, text)
        pic_list.append(data)
    return pic_list


# 进入明细页
def get_detail_pic_list(url, title):
    html = sendHttp(url)
    soup = BeautifulSoup(html, 'html.parser')
    page_list = soup.find('div', class_="pagenavi").find_all('a')
    ## 获取最大的一个总页数
    maxPageText = []
    for i in page_list:
        maxPageText.append(i.get_text())

    pageSize = 0
    for i in maxPageText:
        data = re.findall(r'(\w*[0-9]+)\w*', i)
        try:
            dataNum = int(data[0])
        except:
            pass
        else:
            if pageSize <= dataNum:
                pageSize = dataNum

    # ## 获取图片地址
    pic_url_list = []
    link = get_detail_pic_url(soup)
    pic_url_list.append(link)

    ## 遍历获取其他明细页面的pic_url
    for i in range(2, pageSize + 1):
        next_url = url + "/{}".format(str(i))
        next_link = get_detail_pic(next_url)
        pic_url_list.append(next_link)

    ## 下载
    for i, data in enumerate(pic_url_list):
        down_pic(data, title, i)


# 获取当前页的pic_url
def get_detail_pic(url):
    html = sendHttp(url)
    time.sleep(0.5)
    soup = BeautifulSoup(html, 'html.parser')
    link = get_detail_pic_url(soup)
    return link


## 抓取soup的pic_url
def get_detail_pic_url(soup):
    div = soup.find('div', class_="main-image")
    img = div.find('img')
    img_src = img.get('src')  # 套图链接
    return img_src


def down_pic(url, title, page):
    # 转义特殊符号
    title = "".join(re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', title, re.S))
    path = r'E:\妹子图\{}'.format(title)
    if not os.path.exists(path):
        os.mkdir(path)
    print("开始下载妹子图:{}[第{}页]".format(title, page))
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
               "Referer": url}
    r = requests.get(url, headers=headers, stream=True)  # 增加headers, 模拟浏览器  stream=分块下载
    if r.status_code == 200:
        with open(r'{}\{}第{}页.jpg'.format(path, title, page), 'ab') as f:
            for data in r.iter_content():
                f.write(data)
    time.sleep(1)


if __name__ == '__main__':
    print("抓取妹子图_主函数")
    # begin_time = time
    urlList = ["http://www.mzitu.com/xinggan/"]
    # 获取出妹子图的总页数
    maxPage = getMaxPage(urlList[0])
    for i in range(1, maxPage + 1):
        url = "http://www.mzitu.com/xinggan/page/{}/".format(i)
        urlList.append(url)

    for i, data in enumerate(urlList):
        pic_list = get_pic_list(data)
        for i in pic_list:
            get_detail_pic_list(i["link"], i["title"])
    # end_time = time
    # run_time = end_time - begin_time
    # print('该程序运行时间：', run_time)
