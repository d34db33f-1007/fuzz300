#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import wfuzz

class Fuzzer():

    def orv(url):
        try:
            print(f'\n{url}\n')
            for result in wfuzz.fuzz(url=url, sc=[300,301,302,303,304,305,307,308], payloads=[("file",dict(fn="data/openredirect.txt"))]):
                print(result)
        except KeyboardInterrupt:
            sys.exit(0)
