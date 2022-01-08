#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from utils.url_extractor import Spider
from scrapy.crawler import CrawlerProcess


class Crawler():

    def __init__(self, url, domain):
        self.url = url
        self.domain = domain

    def start(self):
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0'
            })

        Spider.allowed_domains = self.domain
        Spider.start_urls = self.url
        process.crawl(Spider)
        process.start()
        self.clean()

    def clean(self):
        uniqlines = set(open('urls.txt').readlines())
        open('urls.txt', 'w').writelines(set(uniqlines))
        print(f'Total crawled: {len(uniqlines)} links\n')
