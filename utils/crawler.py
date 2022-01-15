#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import gc
import asyncio
import logging

from urllib.parse import urljoin
from bs4 import BeautifulSoup

from utils.aopener import Aiohttp


class Crawler():

    def __init__(self, urls):
        logging.disable(50)
        self.finished = False
        self.depth = 0
        self.domain = urls[0].split('//')[-1].split('www.')[-1]
        self.visited = []
        self.lst = []
        self.lst += urls
#        self.run(urls)

    def check(self, path):
        if path and path.startswith('/'):
            path = urljoin(self.domain, path)
        if self.domain in path:
            if len(path.split('//')[1].split('/')) > 2:
                if re.match('.*.*', path):
                    if not path.endswith('.html'):
                        if not path.endswith('.php'):
                            for n in range(-7, -2): # if not path.endswith('/'):
                                if ((_ := path.split('?'))[-1][n] or _[-2][n]) == '.':
                                    return False
            return path

    async def run(self, urls):
        while not self.finished:
            print(f'Now crawling: {len(self.lst)} links', end='\r')
            self.depth += 1
            gc.collect()
            if (len(self.visited)) > 3000:
                self.finished = True
            elif len(self.lst) <=0:
                self.finished = True
            elif self.depth > 3:
                self.finished = True
            doc = await Aiohttp.session(self.lst)
            self.visited += self.lst
            for _ in self.lst:
                self.lst.remove(_)

            for i, html in enumerate(doc, start=1):
                try:
                    soup = BeautifulSoup(html, 'html.parser')
                    for link in soup.find_all('a'):
                        path = link.get('href')
                        path = self.check(path)
                        if path and path not in self.visited:
#                            print(path)
                            self.lst.append(path)
                except Exception as e:
                    # print(e)
                    pass

                try:
                    for link in re.findall('(?<=href=["\'])https?://.+?(?=["\'])', html.decode('utf-8')):
                        path = link
                        path = self.check(path)
                        if path and path not in self.visited:
#                            print(path)
                            self.lst.append(path)
                except Exception as e:
                    # print(e)
                    pass
                self.lst = list(set(self.lst))

        with open('urls.txt', 'w') as f:
            for l in list(set(self.visited)):
                f.write(f'{l}\n')
        print(f'Total crawled: {len(self.visited)} urls\n')
