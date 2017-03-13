# -*- coding: utf-8 -*-
"""
Created on 2017-01-06 18:33
@author : chen
"""
from scrapy import Request
from scrapy.spiders import CrawlSpider


class TestSpider(CrawlSpider):
    name = "testSpider"
    start_urls = [
        "http://irm.p5w.net/gszz/coplatform.html"
    ]

    def start_requests(self):
        """
        """
        # "http://zsptbs.p5w.net/bbs/chatbbs/bbs.asp?code=600019&web=www.baosteel.com&selcode=1153"
        url = "http://zsptbs.p5w.net/bbs/chatbbs/left.asp?boardid=1153"
        yield Request(url=url,
                      callback=self.parseIndex)

    def parseIndex(self, response):
        response.replace(body=response.body.decode('gbk').encode('utf-8'))
        content = response.body
        if content.find("gb2312"):
            content = content.decode('gb2312').encode('utf-8')
            content = content.replace('gb2312', 'utf-8')
        print content
