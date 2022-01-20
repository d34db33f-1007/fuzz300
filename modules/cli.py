#!/usr/bin/env python3

import sys
import aiohttp
import argparse

from typing import Any

def cookies(value: str):
    c = value
    c = c.split(':')
    try:
        value = dict()
        value[c[0]] = c[1:]
        return value
    except Exception as e:
        print('Not valid Cookie format')
        sys.exit(0)

parser = argparse.ArgumentParser(
    prog="fuzz300",
    description="Robust and blazing fast web-security vulnerability scanner"
)

parser.add_argument(
    "-u",
    "--url",
    type=str,
    required=True,
    help="the target on which to crawl data-urls and test them",
)

parser.add_argument(
    "-c",
    "--cookies",
    type=str,
    required=False,
    default=aiohttp.CookieJar(),
    help="cookies to use while crawling for urls. format: 'Cookie: user=admin'",
)
