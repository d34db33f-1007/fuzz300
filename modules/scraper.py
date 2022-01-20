#!/usr/bin/env python3

import sys
import gc
import asyncio

from urllib.parse import urljoin, urlencode
from bs4 import BeautifulSoup
from typing import List, Any
from strongtyping.strong_typing import match_typing

from modules.aopener import session, aget


async def get_forms(urls: List, c: Any):
    html_list = await session(urls, cookies=c)
    print('\n')
    forms = []
    for i, html in enumerate(html_list, start=1):
        print(f'Trying to find forms: {i} / {len(html_list)}', end='\r')
        try:
            soup = BeautifulSoup(html, "html.parser")
            forms.append(soup.find_all("form"))
        except:
            continue
    # collecting garbage
    del html_list
    gc.collect()
    return forms

@match_typing
async def form_details(forms: List, d: str):
    # get all forms details
    tasks = []
    for form in forms:
        tasks.append(asyncio.create_task(details(form, d)))
    return await asyncio.gather(*tasks)

@match_typing
async def details(form: Any, domain: str):
    # returns action, method and form controls
    details =  f'{form.attrs.get("method", "GET")} '.upper()
    if (ac := form.attrs.get("action")): 
        ac = urljoin(f'https://{domain}', ac, allow_fragments=True)
        details += ac
        if form.attrs.get("action").startswith('http'):
            if domain not in form.attrs.get("action"):
                return False
    for i, i_tag in enumerate(form.find_all("input"), start=1):
        delim = '?' if i == 1 else '&'
        details += f'{delim}{i_tag.attrs.get("name")}='
        details += i_tag.attrs.get("value", "FUZZ")
#       if i_tag.attrs.get("type") == "submit":
#           return False
    return details




