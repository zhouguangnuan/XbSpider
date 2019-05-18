# -*- coding: utf-8 -*-
from scrapy.cmdline import execute

__author__ = 'bobby'

import sys
import os

print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy", "crawl", "3302_25"])