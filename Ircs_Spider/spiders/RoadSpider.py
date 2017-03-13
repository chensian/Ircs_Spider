# -*- coding: utf-8 -*-
"""
Created on 2017-01-06 18:33
@author : chen
"""
import re
import xml.etree.ElementTree as Etree

from os.path import dirname

import time

import sys

from scrapy import FormRequest
from scrapy import Request
from scrapy import Selector
from scrapy.spiders import CrawlSpider

from Ircs_Spider.Util.MongoDB import MongoDBUtil, random_str
from Ircs_Spider.items import NewzsptBBSItem, ZsptbsBBSItem


class RoadSpider(CrawlSpider):
    name = "roadSpider"

    def start_requests(self):
        """
        从数据库中获取所有活动的id 跟 index url
        """
        # roadshow 类型
        roadshow_hds = MongoDBUtil.get_hd_type_roadshow()
        for hd in roadshow_hds:
            hd_id = hd[0]
            hd_url = hd[1]
            stockcode = hd[2]
            roadshow_hds_url = hd_url[0:hd_url.find("bbs.asp")] + "question_page.asp?"
            yield FormRequest(url=roadshow_hds_url,
                              meta={"hd_id": hd_id, "stockcode": stockcode, "pageNo": '1',
                                    "roadshow_hds_url": roadshow_hds_url},
                              formdata={'pageNo': str(1)},
                              callback=self.parse_newzspt_bbs)

    def parse_newzspt_bbs(self, response):
        content = response.body

        if content.find("gbk"):
            content = content.decode('gbk').encode('utf-8')
            content = content.replace('gbk', 'utf-8')
        # print content

        hd_id = response.meta["hd_id"]
        stockcode = response.meta["stockcode"]
        roadshow_hds_url = response.meta["roadshow_hds_url"]
        pageNo = int(response.meta["pageNo"])
        # 保存返回的 response.body  content
        # 数据保存路径
        path = dirname(dirname(dirname(dirname(__file__)))) + '\\data\\ircs\\roadshow_hds\\'

        with open(path + random_str() + '&' + str(hd_id) + '&' + stockcode + '&' +
                          time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.xml', "w") as f:
            f.write(content)

        all_question = Etree.fromstring(content)
        pagerowno = 1
        for qr in all_question.iter(tag='q_and_r'):
            newzsptbbs = NewzsptBBSItem()
            newzsptbbs["hd_id"] = hd_id
            newzsptbbs["stockcode"] = stockcode
            newzsptbbs["roadshow_hds_url"] = roadshow_hds_url
            newzsptbbs["pageNo"] = pageNo
            newzsptbbs["pagerowNo"] = pagerowno
            pagerowno += 1

            question = qr[0]
            for item in question:
                newzsptbbs[item.tag] = item.text
            if len(qr) > 1:
                reply = qr[1]
                for item in reply:
                    newzsptbbs[item.tag] = item.text
            yield newzsptbbs

        if pageNo == 1:
            pagecount = int(all_question.find("q_page").text)
            # print pagecount
            for pageNo in range(1, pagecount + 1):
                yield FormRequest(url=roadshow_hds_url,
                                  meta={"hd_id": hd_id, "stockcode": stockcode, "pageNo": str(pageNo),
                                        "roadshow_hds_url": roadshow_hds_url},
                                  formdata={'pageNo': str(pageNo)},
                                  callback=self.parse_newzspt_bbs)
