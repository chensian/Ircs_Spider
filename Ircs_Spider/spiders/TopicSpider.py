# -*- coding: utf-8 -*-
"""
Created on 2017-01-06 18:33
@author : chen
"""
import json
import re

from os.path import dirname

import time
from scrapy import Request, FormRequest
from scrapy import Selector
from scrapy.spiders import CrawlSpider

from Ircs_Spider.Util.MongoDB import MongoDBUtil
from Ircs_Spider.items import QuesReplyItem, InteractionItem


class TopicSpider(CrawlSpider):
    name = "topicSpider"
    start_urls = [
        "http://irm.p5w.net/gszz/coplatform.html"
    ]

    def start_requests(self):
        """
        从数据库中获取所有活动的id 跟 index url
        """

        # topic_hds = MongoDBUtil.get_hd_type_topic()
        # for hd in topic_hds:
        #     hd_id = hd[0]
        #     hd_url = hd[1]
        #     rid_pattern = re.findall("=\d+", hd_url)[0]
        #     rid = rid_pattern[1:len(rid_pattern)]
        #     question_url = "http://ircs.p5w.net/ircs/topicInteraction/questionPage.do"
        #     yield FormRequest(url=question_url, meta={"hd_id": hd_id, "pageNo": '1'},
        #                       formdata={'pageNo': str(1), 'rid': rid},
        #                       callback=self.parseIndex)
        rsc_rid_hds, rsc_no_rid_hds = MongoDBUtil.get_hd_type_rsc()
        for hd in rsc_rid_hds:
            hd_id = hd[0]
            hd_url = hd[1]
            rid_pattern = re.findall("=\d+", hd_url)[0]
            rid = rid_pattern[1:len(rid_pattern)]
            question_url = "http://ircs.p5w.net/ircs/topicInteraction/questionPage.do"
            yield FormRequest(url=question_url, meta={"hd_id": hd_id, "pageNo": '1'},
                              formdata={'pageNo': str(1), 'rid': rid},
                              callback=self.parseIndex)
        for no_rid_hd in rsc_no_rid_hds:
            hd_id = no_rid_hd[0]
            hd_url = no_rid_hd[1]
            yield FormRequest(url=hd_url, meta={"hd_id": hd_id}, callback=self.parse_no_rid)

    def parseIndex(self, response):
        hd_id = response.meta["hd_id"]
        pageNo = int(response.meta["pageNo"])

        # json数据保存路径
        jsonpath = dirname(dirname(dirname(dirname(__file__)))) + '\\data\\ircs\\topic\\'
        # print jsonpath
        content = response.body
        json.dump(content, open(jsonpath + str(hd_id) + '&' +
                                time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.json', 'w'))
        # print content
        # 加载post 返回的数据
        content = json.loads(content)
        status = content["status"]
        if status == 'Y':
            value = json.loads(content["value"])
            hd_id = hd_id
            all_question = value["q_all"]
            rid = value["rid"]
            pageNo = value["pageNo"]

            pageSize = value["pageSize"]
            stocktype = value["type"]

            if len(all_question) > 0:
                for question in all_question:

                    interaction = InteractionItem()
                    interaction["hd_id"] = hd_id
                    interaction["rid"] = rid

                    interaction["stockcode"] = question["stockcode"]
                    if "score" in question:
                        interaction["score"] = question["score"]
                    if "q_loginId" in question:
                        interaction["q_loginId"] = question["q_loginId"]
                    if "q_date" in question:
                        interaction["q_date"] = question["q_date"]
                    if "q_isclosecomment" in question:
                        interaction["q_isclosecomment"] = question["q_isclosecomment"]
                    if "q_name" in question:
                        interaction["q_name"] = question["q_name"]
                    if "c_isclosecomment" in question:
                        interaction["c_isclosecomment"] = question["c_isclosecomment"]
                    if "q_isguest" in question:
                        interaction["q_isguest"] = question["q_isguest"]
                    if "q_id" in question:
                        interaction["q_id"] = question["q_id"]
                    if "q_jblb" in question:
                        interaction["q_jblb"] = question["q_jblb"]
                    if "reply" in question:
                        reply = question["reply"][0]
                        if reply:
                            interaction["r_officename"] = reply["r_officename"]
                            interaction["r_id"] = reply["r_id"]
                            interaction["r_content"] = reply["r_content"]
                            interaction["isCheck"] = reply["isCheck"]
                            interaction["r_name"] = reply["r_name"]
                            interaction["r_date"] = reply["r_date"]

                    if "hasCancel" in question:
                        interaction["hasCancel"] = question["hasCancel"]
                    if "q_iscloseappraise" in question:
                        interaction["q_iscloseappraise"] = question["q_iscloseappraise"]
                    if "stocktype" in question:
                        interaction["stocktype"] = question["stocktype"]
                    if "q_content" in question:
                        interaction["q_content"] = question["q_content"]
                    if "c_iscloseappraise" in question:
                        interaction["c_iscloseappraise"] = question["c_iscloseappraise"]

                    yield interaction

            if pageNo == 1:
                pagecount = int(value["pagecount"])
                for pageNo in range(1, pagecount + 1):
                    question_url = "http://ircs.p5w.net/ircs/topicInteraction/questionPage.do"
                    yield FormRequest(url=question_url, meta={"hd_id": hd_id, "pageNo": str(pageNo)},
                                      formdata={'pageNo': str(pageNo), 'rid': str(rid)},
                                      callback=self.parseIndex)

    def parse_no_rid(self, response):
        hd_id = response.meta["hd_id"]
        sel = Selector(response)
        rid_pattern = sel.re("rid=\d+")
        rid = rid_pattern[0][4:len(rid_pattern[0])]
        question_url = "http://ircs.p5w.net/ircs/topicInteraction/questionPage.do"
        yield FormRequest(url=question_url, meta={"hd_id": hd_id, "pageNo": '1'},
                          formdata={'pageNo': str(1), 'rid': rid},
                          callback=self.parseIndex)
