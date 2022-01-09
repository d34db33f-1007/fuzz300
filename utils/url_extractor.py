#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging

#from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from scrapy.utils.log import configure_logging

configure_logging(install_root_handler=True)
logging.disable(50)

class Spider(CrawlSpider):

    name = 'extractor'

    custom_settings = {
        'DEPTH_LIMIT': 1,
        'DEPTH_PRIORITY': 1,
        'LOG_ENABLED': False,
        #'MAX_REQUESTS_PER_DOMAIN': 20,
        #'CONCURRENT_REQUESTS': 101
        }

### When writing crawl spider rules, avoid using parse as callback, 
### since the CrawlSpider uses the parse method itself to implement its logic. 
### So if you override the parse method, the crawl spider may no longer work.

    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=False,
            callback="parse_url"
        )
    ]

    def parse_url(self, response):
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        for link in links:
            print(f'Total crawled: {len(links)} links', end='\r')
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    with open('urls.txt', 'a') as f:
                        f.write(link.url + '\n')
                        f.write(response.url + '\n')

if __name__ == '__main__':

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:90.0) Gecko/20100101 Firefox/90.0'
        })

    urls = ['https://example.com']
    allowed_domains = ['example.com']

    Spider.allowed_domains = allowed_domains
    Spider.start_urls = urls
    process.crawl(Spider)
    process.start()


