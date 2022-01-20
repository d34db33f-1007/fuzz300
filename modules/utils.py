#!/usr/bin/env python3

import os
import re

def clear():
    files = ['urls.txt', 'some_links.txt', 'results.txt', 
            'js_webforms.txt', 'entry_points.txt']
    for file in files:
        try:
            os.remove(file)
        except:
            continue

def filter_links(link, domain):
    if domain in link.split('?')[0]:
        if len(link) < 150:
            r = re.compile('(?<=\=)', re.DOTALL)
            link = r.sub('FUZZ,', link)
            return link
        else:
            with open('some_links.txt', 'a') as f:
                f.write(f'{link}\n')
            return False
