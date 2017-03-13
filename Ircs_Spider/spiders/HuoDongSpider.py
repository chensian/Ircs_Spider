# -*- coding: utf-8 -*-
"""
Created on 2017-01-06 18:33
@author : chen
"""

from scrapy import Request
from scrapy import Selector
from scrapy.spiders import CrawlSpider

from Ircs_Spider.Util.MongoDB import MongoDBUtil
from Ircs_Spider.items import HuoDongItem


class HuoDongSpider(CrawlSpider):
    name = "hdSpider"

    def start_requests(self):
        """
        从数据库中获取所有公司的id 跟 index url
        """

        companys_id_url = MongoDBUtil.get_all_company__index_url()
        for id_url in companys_id_url:
            stockcode = id_url[0]
            index_url = id_url[1]
            # print interaction_url
            yield Request(url=index_url, meta={"stockcode": stockcode}, callback=self.parseIndex)

    def parseIndex(self, response):
        """
        处理company 第一页 index url
        """
        stockcode = response.meta["stockcode"]

        sel = Selector(response)
        hds = sel.xpath("//select")[0].xpath("option[@value]")
        for hd in hds:
            stockcode = stockcode
            hd_title = hd.xpath("@title").extract_first()
            hd_url = hd.xpath("@value").extract_first()
            hd_picture_url = hd.xpath("@pictureUrl").extract_first()

            huodong = HuoDongItem()
            if stockcode:
                huodong["stockcode"] = stockcode
            if hd_title:
                huodong["hd_title"] = hd_title
            if hd_url:
                huodong["hd_url"] = hd_url
            if hd_picture_url:
                huodong["hd_picture_url"] = hd_picture_url
            yield huodong
