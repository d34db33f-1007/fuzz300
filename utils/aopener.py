#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import asyncio
import aiohttp

class Aiohttp():

	async def get(session, url, sem):

		ua = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:78.0) Gecko/20100101 Firefox/78.0'}

		try:
			async with sem, session.get(url, timeout=8, headers=ua, raise_for_status=True) as resp:
				return await resp.read()
		except Exception as e:
#			print(e)
			pass

	async def session(urls):
		# conn = aiohttp.TCPConnector(limit=30)
		sem = asyncio.Semaphore(500)
		tasks = []
		async with aiohttp.ClientSession(trust_env=True, raise_for_status=True) as session:
			for url in urls:
				tasks.append(asyncio.create_task(Aiohttp.get(session, url, sem)))
			doc = await asyncio.gather(*tasks, return_exceptions=True)
			return doc
