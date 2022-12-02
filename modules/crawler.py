#!/usr/bin/env python3

import re
import gc
import asyncio
import logging

from urllib.parse import urljoin
from bs4 import BeautifulSoup

from typing import List
from strongtyping.config import SEVERITY_LEVEL
from strongtyping.strong_typing import match_typing

from modules.aopener import session, aget


class Crawler():

    @match_typing(severity=SEVERITY_LEVEL.WARNING)
    def __init__(self, urls: List):
        logging.disable(50)
        # safe extensions
        self.ext = ['html', 'php', 'asp', 'aspx', 'jsp', 'cgi']
        self.domain = urls[0].split('//')[-1].split('www.')[-1]
        self.finished = False
        self.depth = 0       # recursion
        self.visited = []    # main list
        self.lst = []        # to_visit next
        self.lst += urls     # base_url

    @match_typing
    def check(self, path: str):
        # checking for full link
        if path and path.startswith('/'):
            path = urljoin(self.domain, path)
        # filtering out non-relative websites
        if self.domain in path:
            # checking for extensions
            if len(path[:-1].split('//')[1].split('/')) > 2:
                if re.match('.*.*', path):
                    # filtering out website asset files
                    return self.recheck(path)
            return path

    @match_typing
    def recheck(self, path: str):
        for e in self.ext:
            if path.endswith(e):
                return path
        # filtering extensions that are out the list
        _ = path.split('?')
        for n in range(-7, -2):
            try:
                if len(_) > 2:
                    if any(c == '.' for c in [_[-1][n], _[-2][n]]):
                        return False
                else:
                    if any(c == '.' for c in _[0][n]):
                        return False
            except:
                continue
        return path

    @match_typing
    async def run(self, urls: List):
        # main crawl function
        print(f'Now crawling:\n') 
        while not self.finished:
            # recursion
            self.depth += 1
            # cycle exit rules
            if (len(self.visited)) > 3000:
                self.finished = True
            elif len(self.lst) == 0:
                self.finished = True
            elif self.depth > 3:
                self.finished = True
            # release to_visit list
            doc = await session(self.lst, sem=500)
            self.visited += self.lst
            for _ in self.lst:
                self.lst.remove(_)

            # parse all links
            for html in doc:
                try: # method #1
                    soup = BeautifulSoup(html, 'html.parser')
                    for link in soup.find_all('a'):
                        path = link.get('href')
                        if path and (_ := self.check(path)) not in self.visited:
                            self.lst.append(_)
                except Exception as e:
                    pass

                try: # method #2
                    for link in re.findall('(?<=href=["\'])https?://.+?(?=["\'])', html.decode('utf-8')):
                        if link and (_ := self.check(link)) not in self.visited:
                            self.lst.append(_)
                except Exception as e:
                    pass
            del doc
            # collecting garbage
            gc.collect()
            self.lst = list(set(self.lst))

        # write all crawled links to the file
        with open('urls.txt', 'w') as f:
            for l in list(set(self.visited)):
                f.write(f'{l}\n')
        print(f'\nTotal crawled: {len(self.visited)} urls\n')
