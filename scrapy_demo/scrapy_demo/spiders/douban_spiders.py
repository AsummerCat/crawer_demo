# -*- coding: utf-8 -*-
import scrapy


class DoubanSpidersSpider(scrapy.Spider):
    name = 'douban_spiders'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/']

    def parse(self, response):
        pass
