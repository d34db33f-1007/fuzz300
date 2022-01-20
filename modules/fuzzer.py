#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import wfuzz

from typing import List

def fuzz(url: str, rec: List, payload: str):
    sess = wfuzz.FuzzSession(url=url, recipe=rec)
    try:
        for r in sess.fuzz(payloads=[("file",dict(fn=payload))]):
            if r:
                break
    except KeyboardInterrupt:
        sys.exit(0)

