#!/usr/bin/env python3

import os

from urllib.parse import urlsplit, parse_qs, quote

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
            query = urlsplit(link).query
            params = parse_qs(query, keep_blank_values=True)
            for k, v in params.items():
                link = link.replace(f'{k}={quote(v[0], safe="")}', f'{k}=FUZZ')
                link = link.replace(f'{k}={quote(v[0]}', f'{k}=FUZZ')
                link = link.replace(f'{k}={v[0]}', f'{k}=FUZZ')
#            r = re.compile('(?<=\=)', re.DOTALL)
#            link = r.sub('FUZZ,', link)
            return link
        else:
            with open('some_links.txt', 'a') as f:
                f.write(f'{link}\n')
            return False
