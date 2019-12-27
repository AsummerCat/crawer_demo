# -*- coding:utf-8 -*-
'''
chromedriver
http://npm.taobao.org/mirrors/chromedriver/

火狐
https://github.com/mozilla/geckodriver



 conda install -c conda-forge selenium

'''
from selenium import webdriver


def test():
    # driver = webdriver.Chrome()  # 创建一个 Chrome WebDriver 实例
    driver = webdriver.Firefox()  # 创建一个 Chrome WebDriver 实例
    driver.get('https://www.baidu.com/')  # 打开网址


if __name__ == '__main__':
    test()
