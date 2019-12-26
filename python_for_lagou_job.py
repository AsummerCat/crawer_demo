# -*- coding:utf-8 -*-
## Python爬虫——Python岗位分析报告 导出到xlsx
'''
conda install -c conda-forge openpyxl
'''

import random
import time

import requests
from openpyxl import Workbook
import urllib.parse


def get_json(url, page, lang_name, i):
    index_url = 'https://www.lagou.com/jobs/list_{}?city={}&cl=false&fromSearch=true&labelWords=&suginput='.format(lang_name, urllib.parse.quote(i))
    # 消息头
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.lagou.com/jobs/list_{}?city={}&cl=false&fromSearch=true&labelWords=&suginput='.format(urllib.parse.quote(lang_name), urllib.parse.quote(i)),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }


    data = {'first': 'true', 'pn': str(page), 'kd': lang_name}
    s = requests.Session()
    s.get(index_url, headers=headers, timeout=3)  # 请求首页获取cookies
    cookie = s.cookies  # 为此次获取的cookies
    json = s.post(url, data=data, headers=headers, cookies=cookie, timeout=3).json()  # 获取此次文本
    time.sleep(5)
    list_con = json['content']['positionResult']['result']
    info_list = []
    for i in list_con:
        info = []
        info.append(i.get('companyShortName', '无'))  # 公司名
        info.append(i.get('companyFullName', '无'))
        info.append(i.get('industryField', '无'))  # 行业领域
        info.append(i.get('companySize', '无'))  # 公司规模
        info.append(i.get('salary', '无'))  # 薪资
        info.append(i.get('city', '无'))
        info.append(i.get('education', '无'))  # 学历
        info_list.append(info)
    return info_list  # 返回列表





def main():
    lang_name = 'python'
    wb = Workbook()  # 打开 excel 工作簿
    for i in ['北京', '上海', '广州', '深圳', '杭州']:  # 五个城市
        print("开始获取{}的{}岗位".format(i,lang_name))
        page = 1
        ws1 = wb.active
        ws1.title = lang_name
        url = 'https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false'.format(i)
        while page < 2:  # 每个城市30页信息
            print("开始获取{}的{}岗位,第{}页".format(i, lang_name,page))
            info = get_json(url, page, lang_name, i)
            page += 1
            time.sleep(random.randint(10, 20))
            for row in info:
                ws1.append(row)
        print("结束获取{}的{}岗位".format(i, lang_name))
    print("输出xlsx")
    wb.save('E:\\{}职位信息.xlsx'.format(lang_name))


if __name__ == '__main__':
    main()


