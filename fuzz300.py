#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import sys
import re
import asyncio

from utils.clean import Clean
from utils.crawler import Crawler
from utils.scraper import Scraper
from utils.fuzz import Fuzzer

banner = '''
                __ 
              .'  '.        .-''-.
             | 303  |      ;  ,-> :
              '.__.'       :  |   ; 
                ||          '-..-'
                ||
                ||
              \\||///
         ^^^^^^^^^^^^^^^'''

print(banner)
Clean.files()
e_points = []

## crawler
url = sys.argv[1].split()
domain = url[0].split('//')[-1].split('www.')[-1]
domain = domain.split()

crawl = Crawler(url, domain) 
crawl.start()


## scraper
links = open('urls.txt', 'r').readlines()
links.append(url[0])
links = sorted(links, key=len)
links = list(map(lambda a: a.strip(), links))

_ = []
data_urls = []
for link in links:
    if ('?' or '=') in link:
        if domain[0] in (a := link.split('?')[0]):
            if len(link) < 150:
                if a not in _:
                    reg = "(?<=%s)" % ('=')
                    r = re.compile(reg,re.DOTALL)
                    link = r.sub('FUZZ', link)
                    data_urls.append(link)
                    _.append(a)
            else:
                with open('some_links.txt', 'a') as f:
                    f.write(f'{link}\n')


e_points += data_urls
if len(data_urls) > 0:
    print('Found links with data inside:\n')
    for url in data_urls:
        print(url)
    print('\n\n')


# get all form tags
print('Starting to scrape urls for web-forms!\n')
forms = asyncio.run(Scraper.get_forms(links[:800]))

# iteratte over forms
det = []
weburls = []
for data in forms:
    for line in data:
        # get form details
        details = Scraper.form_details(line, domain[0])
        if not details:
            continue
        if len(details) > 350:
            continue
        if details.split('&')[0] in det:
            continue
        weburls.append(details)
        det.append(details.split('&')[0])

# remove duplicates
weburls = list(set(weburls))

# filter results
for webf in weburls:
    if webf.lstrip('GET ').startswith('http'):
        e_points.append(webf.lstrip('GET '))
    else:
        with open('js_webforms.txt', 'a') as f:
            f.write(f'{webf}\n')

# remove initial urls file
try:
    os.remove('urls.txt')
except:
    pass

if len(e_points) == 0:
    print("Haven't found any valid url or web-form to start fuzzing. Exiting..")
    sys.exit(0)
else:
    # write all valid entry points to the file
    with open('entry_points.txt', 'w') as f:
        for p in e_points:
            f.write(f'{p}\n')

par = ['away', 'out', 'next', 'dest', 'target', 'url', 'rurl', 'redir', 
        'destination', 'redirect_uri', 'redirect_url', 'redirect', 'view', 
        'login', 'image_url', 'go', 'return','checkout', 'continue', 'path']

print('Starting to fuzz urls to find open-redirect vulnerability\n')
suc = False
for url in e_points:
    for item in par:
        if item in url:
            try:
                Fuzzer.orv(url)
                suc = True
            except:
                continue

if not suc:
    for url in e_points:
        Fuzzer.orv(url)
































