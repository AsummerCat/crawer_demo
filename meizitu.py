# -*- coding:utf-8 -*-
import requests
import os
import time
import threading
import re
from bs4 import BeautifulSoup

'''
开启线程获取妹子图数据
目测3个线程获取数据比较稳定

抓取流程 -> 获取列表页及其最大页数 ->(多线程)获取明细页列表及其最大页数  -> 下载数据(分块下载 stream=True) 


'''


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
        pic_list.append(data)
    print("{}获取单页数据完毕 wait3秒".format(url))
    time.sleep(3)
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

    # 获取图片地址
    link = get_detail_pic_url(soup)

    ## 遍历获取其他明细页面的pic_url
    pic_url_list = get_rosi_all_pic_url(link, pageSize)

    ## 下载
    for i, data in enumerate(pic_url_list):
        down_pic(data, title, i)


# 根据第一个图片地址获取套图所有地址
def get_rosi_all_pic_url(info_pic_url, pageSize):
    pic_url_list = []
    # 完整文件名称
    pic_name = info_pic_url[info_pic_url.rfind('/', 1) + 1:len(info_pic_url) + 1]
    # 获取后缀+标记-> 01.jpg
    bit_pic = re.search(r'[^d]+$', pic_name).group(0)
    # 获取下标
    bit_pic_index_num = bit_pic.split(".")[0]
    # 获取后缀
    pic_type_suffix = "." + bit_pic.split(".")[1]
    # 循环填充后缀
    for i in range(1, pageSize + 1):
        s_i = str(i)
        if len(str(i)) < 2:
            s_i = "0" + s_i
        pic_url_list.append(info_pic_url.replace(bit_pic, s_i + pic_type_suffix))
    return pic_url_list


## 抓取soup的pic_url
def get_detail_pic_url(soup):
    div = soup.find('div', class_="main-image")
    img = div.find('img')
    img_src = img.get('src')  # 套图链接
    return img_src


## 下载文件
def down_pic(url, title, page):
    # 转义特殊符号
    title = "".join(re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', title, re.S))
    path = 'E:\\妹子图\\{}'.format(title)
    # 判断文件夹是否存在 不存在直接makedirs 创建多级目录
    if not os.path.exists(path):
        os.makedirs(path)
    print("开始下载妹子图:{}[第{}页]".format(title, page))
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
               "Referer": url}
    # 判断文件是否存在
    data_jpg = r'{}\{}第{}页.jpg'.format(path, title, page)

    if not os.path.exists(data_jpg):
        r = requests.get(url, headers=headers, stream=True)  # 增加headers, 模拟浏览器  stream=分块下载
        if r.status_code == 200:
            with open(data_jpg, 'ab') as f:
                for content in r.iter_content():
                    f.write(content)
        time.sleep(2)
    else:
       print(data_jpg + "已存在")


# 常规抓取
def default_mian():
    print("抓取妹子图_常规抓取")
    # begin_time = time
    urlList = []
    # 获取出妹子图的总页数
    maxPage = getMaxPage("http://www.mzitu.com/xinggan/page/1/")
    for i in range(1, maxPage + 1):
        url = "http://www.mzitu.com/xinggan/page/{}/".format(i)
        urlList.append(url)

    # 线程数
    threads = []
    for data in urlList:
        ## 获取单列表的套图
        pic_list = get_pic_list(data)
        while len(pic_list) > 0:
            for thread in threads:
                if not thread.is_alive():
                    threads.remove(thread)
            while len(threads) < 5 and len(pic_list) > 0:  # 最大线程数设置为 3  测试 3个线程比较稳定
                url = pic_list.pop(0)
                thread = threading.Thread(target=get_detail_pic_list, args=(url["link"], url["title"]))
                thread.setName(url["title"] + "---->" + url["link"])
                thread.setDaemon(True)
                thread.start()
                print("开启一个线程----->" + thread.getName())
                threads.append(thread)


if __name__ == '__main__':
    default_mian()
