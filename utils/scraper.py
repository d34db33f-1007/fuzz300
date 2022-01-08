#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import asyncio
import aiohttp

from urllib.parse import urljoin
from bs4 import BeautifulSoup


class Scraper():

    async def get_url(session, url):
        user_agent = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0'}
        try:
            async with session.get(url, timeout=15, headers=user_agent) as resp:
                if len(url) < 80:
                    print(url, end='\r')
                return await resp.read()
        except:
            pass

    async def get_forms(urls):
        tasks = []
        async with aiohttp.ClientSession(trust_env=True) as session:
            for url in urls:
                tasks.append(asyncio.create_task(Scraper.get_url(session, url)))
            html_list = await asyncio.gather(*tasks)

        print('\n')
        forms = []
        for i, html in enumerate(html_list, start=1):
            print(f'Trying to find forms: {i} / {len(html_list)}', end='\r')
            try:
                soup = BeautifulSoup(html, "html.parser")
                forms.append(soup.find_all("form"))
            except:
                continue
        return forms

    def form_details(form, domain):
        # returns action, method and form controls
        details =  f'{form.attrs.get("method", "POST")} '.upper()
        if (ac := form.attrs.get("action")): 
            ac = urljoin(f'https://{domain}', ac, allow_fragments=True)
            details += ac
            if form.attrs.get("action").startswith('http'):
                if domain not in form.attrs.get("action"):
                    return False
        for i, i_tag in enumerate(form.find_all("input"), start=1):
            details += f'?{i_tag.attrs.get("name")}=' if i==1 else f'&{i_tag.attrs.get("name")}='
            details += f'{i_tag.attrs.get("value", "FUZZ")}'
#            if i_tag.attrs.get("type") == "submit":
#                return False
        return details




