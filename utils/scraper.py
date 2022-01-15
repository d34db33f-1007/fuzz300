#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import asyncio
import aiohttp

from urllib.parse import urljoin
from bs4 import BeautifulSoup


class Scraper():

    async def get_url(session, url, c, sem):
        ua = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:78.0) Gecko/20100101 Firefox/78.0'}
        try:
            async with sem, session.get(url, timeout=15, headers=ua, cookies=c, raise_for_status=True) as resp:
                if len(url) < 80:
                    print(url, end='\r')
                return await resp.read()
        except Exception as e:
            pass

    async def get_forms(urls, cookies=aiohttp.CookieJar()):
        tasks = []
        # conn = aiohttp.TCPConnector(limit=30)
        sem = asyncio.Semaphore(100)
        async with aiohttp.ClientSession(trust_env=True, raise_for_status=True) as session: # conn
            for url in urls:
                tasks.append(asyncio.create_task(Scraper.get_url(session, url, cookies, sem)))
            html_list = await asyncio.gather(*tasks, return_exceptions=True)

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

    async def form_details(forms, d):
        tasks = []
        for form in forms:
            tasks.append(asyncio.create_task(Scraper.details(form, d)))
        return await asyncio.gather(*tasks)

    async def details(form, domain):
        # returns action, method and form controls
        details =  f'{form.attrs.get("method", "GET")} '.upper()
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




