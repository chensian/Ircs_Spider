# -*- coding: utf-8 -*-
"""
Created on 2016-10-22 16:24
@author : chen
"""
from scrapy import cmdline


# cmdline.execute("scrapy crawl testSpider".split())
# cmdline.execute("scrapy crawl hdSpider".split())
# cmdline.execute("scrapy crawl IrcsSpider".split())
# cmdline.execute("scrapy crawl topicSpider".split())
# cmdline.execute("scrapy crawl roadSpider".split())
cmdline.execute("scrapy crawl bbsSpider".split())

