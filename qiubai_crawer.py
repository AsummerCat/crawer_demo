# -*- coding:utf-8 -*-
'''
糗百_爬虫
利用Beautiful Soup 库 和 requests
conda install -c conda-forge beautifulsoup4
conda install -c conda-forge requests
'''
import os

import requests
from bs4 import BeautifulSoup
import re
from time import *


# 发送http请求
def sendHttp(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
               "Referer": url}
    r = requests.get(url, headers=headers)  # 增加headers, 模拟浏览器
    return r.text


# 获取总页数的标记
def getMaxPage(url):
    soup = BeautifulSoup(sendHttp(url), 'html.parser')
    con = soup.find(id='position')
    ## 总页数和笑话数
    htmlPage = con.contents[6]
    ## 获取后半段数据
    data = str(htmlPage).split("，")
    pageSize = 0
    if data:
        # 具体页数
        pageText = re.findall(r'(\w*[0-9]+)\w*', data[1])
        if pageText:
            pageSize = int(pageText[0])

    return pageSize


# 查看文章
def cat_html(url, page, maxPage):
    output = """第{}页   文章名称: 糗事百科:   [{}]  \n   点击数：{} \n文章内容\n{}\n\n"""  # 最终输出格式
    tetleContentText = []
    articleContentHtmlText = []
    html = sendHttp(url).replace("<br /><br /><br />", "").replace("<br />", "\n")
    soup = BeautifulSoup(html, 'html.parser')
    ##所有文章标题html
    titleList = soup.find(id='footzoon').find_all('h3')
    ## 所有文章内容html
    contentList = soup.find(id='footzoon').find_all(id="endtext")
    ## 所有文章点击数html
    clickNum = html.split("　　Click:")
    del clickNum[0]

    ## 获取所有标题列表
    for i in titleList:
        tetleContentText.append(i.find('a').get_text())
    ## 获取所有文章内容列表
    for i in contentList:
        articleContentHtmlText.append(i)

    ## 获取出完整的文章
    if len(tetleContentText) == len(articleContentHtmlText) == len(clickNum):
        print("=======================开始下载 第{}/{}页==============================".format(page, maxPage))
        for i in range(len(tetleContentText)):
            content = output.format(page, tetleContentText[i],
                                    re.findall(r'(\w*[0-9]+)\w*',
                                               clickNum[i][0:10])[0],
                                    articleContentHtmlText[i].get_text())
            save_html(content, tetleContentText[i], page)


## 保存文章
def save_html(content, title, page):
    # 文件名称转义  emjoy
    title = str(title).replace("", "")
    # 转义特殊符号
    title = "".join(re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', title, re.S))
    path = 'E:\\糗百text\\糗事百科第{}页'.format(page)
    if not os.path.exists(path):
        os.mkdir(path)
    print("开始下载糗事百科:{}".format(title))

    for i in content:
        with open(r'{}\{}.txt'.format(path, title), 'a', encoding='utf-8') as f:
            f.write(i)


if __name__ == '__main__':
    begin_time = time()
    print("抓取糗百_主函数")
    urlList = ["http://www.lovehhy.net/Joke/Detail/QSBK/"]
    # 获取出糗百的总页数
    maxPage = getMaxPage(urlList[0])

    ## 首页单独查看下载
    cat_html(urlList[0], 1, maxPage)

    ## 遍历查看文章下载
    for i in range(1, maxPage + 1):
        url = "http://www.lovehhy.net/Joke/Detail/QSBK/{}".format(i)
        urlList.append(url)
        cat_html(urlList[i], i + 1, maxPage)

    end_time = time()
    run_time = end_time - begin_time
    print('该程序运行时间：', run_time)
