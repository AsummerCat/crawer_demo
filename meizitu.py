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
            print("忽略")
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


if __name__ == '__main__':
    print("抓取妹子图_主函数")
    begin_time = time
    urlList = ["http://www.mzitu.com/xinggan/"]
    # 获取出妹子图的总页数
    maxPage = getMaxPage(urlList[0])
    # for i in range(1, maxPage + 1):
    #     url = "http://www.mzitu.com/xinggan/page/{}/".format(i)
    #     urlList.append(url)

    for i, data in enumerate(urlList):
        pic_list = get_pic_list(data)
        for i in pic_list:
            print(i["link"] + i["title"])
