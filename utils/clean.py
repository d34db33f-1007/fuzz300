#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os

class Clean():

    def files():
<<<<<<< HEAD
        files = ['urls.txt', 'some_links.txt', 'results.txt', 
=======
        files = ['urls.txt', 'some_links.txt', 'results.txt',
>>>>>>> c610ae991c05763ca37de7d13e2bebcfe75a99e3
                 'js_webforms.txt', 'entry_points.txt']
        for file in files:
            try:
                os.remove(file)
            except:
                continue
