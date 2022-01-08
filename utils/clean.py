#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os

class Clean():

    def files():
        files = ['urls.txt', 'some_links.txt', 
                 'js_webforms.txt', 'entry_points.txt']
        for file in files:
            try:
                os.remove(file)
            except:
		pass
