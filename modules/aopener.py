#!/usr/bin/env python3

import asyncio
import aiohttp

from typing import List

async def aget(session, url: str, sem, c):
    ua = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:78.0) Gecko/20100101 Firefox/78.0'}
    try:
        async with sem, session.get(url, timeout=8, headers=ua, cookies=c, raise_for_status=True) as resp:
            if len(url) < 80:
                print(url, end='\r')
                return await resp.read()
    except Exception as e:
        pass

async def session(urls: List, cookies=aiohttp.CookieJar(), sem: int=100):
    # conn = aiohttp.TCPConnector(limit=30)
    sem = asyncio.Semaphore(sem)
    tasks = []
    async with aiohttp.ClientSession(trust_env=True, raise_for_status=True) as session:
        for url in urls:
            tasks.append(asyncio.create_task(aget(session, url, sem, cookies)))
        doc = await asyncio.gather(*tasks, return_exceptions=True)
        return doc
