#!/usr/bin/env python3

import os
import sys
import asyncio
import argparse

from itertools import chain
from urllib.parse import urlparse
from typing import List, Any

from modules.cli import parser
from modules.utils import *
from modules.scraper import *
from modules.crawler import Crawler
from modules.fuzzer import fuzz

banner = '''
                __ 
              .'  '.        .-''-.
             | 301  |      ;  ,-> :
              '.__.'       :  |   ; 
                ||          '-..-'
                ||
                ||
              \\||///
         ^^^^^^^^^^^^^^^'''

e_points = []

def crawl(url: List):
    crawl = Crawler(url)
    asyncio.run(crawl.run(url))

def scrap(domain: List, _: str, cookies):
    global e_points

    urls = open('urls.txt', 'r')
    links = urls.readlines()
    links.append(_)
    links = sorted(links, key=len)
    links = list(map(lambda a: a.strip(), links))
    urls.close()
    os.remove('urls.txt')

    # filter urls for data-urls
    _ = []
    data_urls = []
    for link in links:
        if len(urlparse(link).query) > 0:
            link = filter_links(link, domain[0])
            if link and link not in data_urls:
                if (a := link.split('?')[0]) not in _:
                    data_urls.append(link)
                    _.append(a)

    e_points += data_urls
    if len(data_urls) > 0:
        print('Found links with data inside:\n')
        for url in data_urls:
            print(url)
        print('\n\n')


    # get all form tags
    print('Starting to scrape urls for web-forms!\n')
    forms = asyncio.run(get_forms(links[:800], cookies))
    # iterate over forms
    data = []
    for form in chain.from_iterable(forms):
        data.append(form)

    # get form details
    det = []
    weburls = []
    details = asyncio.run(form_details(data, domain[0]))
    for d in details:
        if not d or len(d) > 350:
            continue
        elif d.split('&')[0] in det:
            continue
        weburls.append(d)
        det.append(d.split('&')[0])

    # remove duplicates
    weburls = list(set(weburls))

    # filter results
    for webf in weburls:
        if webf.lstrip('GET ').startswith('http'):
            webf = filter_links(webf.lstrip('GET '), domain[0])
            e_points.append(webf)
        else:
            with open('js_webforms.txt', 'a') as f:
                f.write(f'{webf}\n')

    if len(e_points) == 0:
        print("Haven't found any valid url or web-form to start fuzzing. Exiting..")
        sys.exit(0)
    else:
        # write all valid entry points to the file
        with open('entry_points.txt', 'w') as f:
            for p in e_points:
                f.write(f'{p}\n')

def openredirect():
    global e_points

    par = ['away', 'out', 'next', 'dest', 'target', 'url', 'rurl', 'redir', 
        'destination', 'redirect_uri', 'redirect_url', 'redirect', 'view', 
        'login', 'image_url', 'go', 'return','checkout', 'continue', 'path']

    print('Starting to fuzz urls to find open-redirect vulnerability\n')
    for url in e_points:
        try:
            fuzz(url, ['data/openredirect.json'], 'data/openredirect.txt')
        except KeyboardInterrupt:
            sys.exit(0)


if __name__ == '__main__':
    args = parser.parse_args()
    print(banner)
    clear()

    url = args.url.split()
    domain = url[0].split('//')[-1].split('www.')[-1]
    domain = domain.split()

    crawl(url)
    scrap(domain, args.url, args.cookies)
    openredirect()


