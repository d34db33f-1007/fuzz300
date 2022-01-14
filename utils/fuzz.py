#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import wfuzz

class Fuzzer():

    def orv(url):
        sess = wfuzz.FuzzSession(url=url, method='GET')
        try:
            for r in sess.fuzz(sc=[300,301,302,303,304,305,307,308], payloads=[("file",dict(fn="data/openredirect.txt"))]):
                if r:
                    print(url)
                    print(r)
                    break
        except KeyboardInterrupt:
            sys.exit(0)
