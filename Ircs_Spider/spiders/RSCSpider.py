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
from scrapy import Request
from scrapy import Selector
from scrapy.spiders import CrawlSpider

from Ircs_Spider.Util.MongoDB import MongoDBUtil, random_str
from Ircs_Spider.items import NewzsptBBSItem, ZsptbsBBSItem


class RSCSpider(CrawlSpider):
    name = "rscSpider"

    def start_requests(self):
        """
        从数据库中获取所有活动的id 跟 index url
        """
        rsc_rid_hds, rsc_no_rid_hds = MongoDBUtil.get_hd_type_rsc()
        print len(rsc_rid_hds)
        for hd in rsc_rid_hds:
            hd_id = hd[0]
            hd_url = hd[1]
            stockcode = hd[2]
            rid_pattern = re.findall("selcode=\d+", hd_url)
            if len(rid_pattern) == 0:
                yield Request(url=hd_url,
                              meta={"hd_id": hd_id, "stockcode": stockcode},
                              callback=self.parse_zsptbs_bbs_no_boardid)
            else:
                boardid = rid_pattern[0][8:len(rid_pattern[0])]
                # print boardid
                zsptbs_url = "http://zsptbs.p5w.net/bbs/chatbbs/left.asp?boardid=%s&pageNo=1" % boardid
                yield Request(url=zsptbs_url,
                          meta={"hd_id": hd_id, "pageNo": '1', "boardid": boardid, "stockcode": stockcode},
                          callback=self.parse_zsptbs_bbs)

    def parse_newzspt_bbs(self, response):
        content = response.body

        if content.find("gbk"):
            content = content.decode('gbk').encode('utf-8')
            content = content.replace('gbk', 'utf-8')
        # print content

        hd_id = response.meta["hd_id"]
        stockcode = response.meta["stockcode"]
        pageNo = int(response.meta["pageNo"])
        boardid = int(response.meta["boardid"])
        # 保存返回的 response.body  content
        # 数据保存路径
        path = dirname(dirname(dirname(dirname(__file__)))) + '\\data\\ircs\\bbs_newzspt\\'

        with open(path + random_str() + '&' + str(hd_id) + '&' + stockcode + '&' +
                          time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.xml', "w") as f:
            f.write(content)

        all_question = Etree.fromstring(content)
        pagerowno = 1
        for qr in all_question.iter(tag='q_and_r'):
            newzsptbbs = NewzsptBBSItem()
            newzsptbbs["hd_id"] = hd_id
            newzsptbbs["stockcode"] = stockcode
            newzsptbbs["boardid"] = boardid
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
                newzspt_bbs_url = "http://newzspt.p5w.net/bbs/question_page.asp?boardid=%s&bbs=1&pageNo=%s" % (
                    boardid, pageNo)
                # print pageNo, newzspt_bbs_url
                yield Request(url=newzspt_bbs_url,
                              meta={"hd_id": hd_id, "stockcode": stockcode, "pageNo": str(pageNo),
                                    "boardid": boardid},
                              callback=self.parse_newzspt_bbs)

    def parse_zsptbs_bbs(self, response):
        hd_id = response.meta["hd_id"]
        stockcode = response.meta["stockcode"]
        pageNo = int(response.meta["pageNo"])
        boardid = int(response.meta["boardid"])

        path = dirname(dirname(dirname(dirname(__file__)))) + '\\data\\ircs\\bbs_zsptbs\\'

        content = response.body.decode('gbk').encode("utf-8")
        with open(path + random_str() + '&' + str(hd_id) + '&' + stockcode + '&' +
                          time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.html', "w") as f:
            f.write(content)

        sel = Selector(text=content)
        items = sel.xpath("//table[@bordercolor='#cc0000']")[0].xpath("tr")

        pagerowno = 1
        for item in items[1:len(items)]:
            zsptbs = ZsptbsBBSItem()
            zsptbs["hd_id"] = hd_id
            zsptbs["stockcode"] = stockcode
            zsptbs["boardid"] = boardid
            zsptbs["pageNo"] = pageNo
            zsptbs["pagerowNo"] = pagerowno
            pagerowno += 1

            quest_id = item.xpath("td")[0].xpath("text()").extract_first()
            reply_id = item.xpath("td")[1].xpath("text()").extract_first()
            spokesman = item.xpath("td")[2].xpath("font/text()").extract_first()
            content = item.xpath("td")[3].xpath("font").extract_first()

            if quest_id:
                zsptbs["quest_id"] = quest_id
            if reply_id:
                zsptbs["reply_id"] = reply_id
            if spokesman:
                zsptbs["spokesman"] = spokesman
            if content:
                zsptbs["content"] = content
            yield zsptbs

        if pageNo == 1:
            pagecount = int(sel.xpath("//td[@align='Center']/font[@color='red']/text()").extract_first())
            print "pagecount", pagecount
            for pageNo in range(1, pagecount + 1):
                zsptbs_url = "http://zsptbs.p5w.net/bbs/chatbbs/left.asp?boardid=%s&pageNo=%s" % (boardid, pageNo)
                yield Request(url=zsptbs_url,
                              meta={"hd_id": hd_id, "pageNo": str(pageNo), "boardid": boardid, "stockcode": stockcode},
                              callback=self.parse_zsptbs_bbs)

    def parse_zsptbs_bbs_no_boardid(self, response):
        hd_id = response.meta["hd_id"]
        stockcode = response.meta["stockcode"]
        content = response.body.decode('gbk').encode("utf-8")
        sel = Selector(text=content)
        rid_pattern = sel.re("boardid=\d+']")
        boardid = rid_pattern[0][8:len(rid_pattern[0])]
        zsptbs_url = "http://zsptbs.p5w.net/bbs/chatbbs/left.asp?boardid=%s&pageNo=1" % boardid
        yield Request(url=zsptbs_url,
                      meta={"hd_id": hd_id, "pageNo": '1', "boardid": boardid, "stockcode": stockcode},
                      callback=self.parse_zsptbs_bbs)
