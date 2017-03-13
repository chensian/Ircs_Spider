# -*- coding: utf-8 -*-
"""
Created on 2017-01-06 18:33
@author : chen
"""
import re

from scrapy import Request, FormRequest
from scrapy import Selector
from scrapy.spiders import CrawlSpider

from Ircs_Spider.Util.MongoDB import MongoDBUtil
from Ircs_Spider.items import QuesReplyItem


class IrcsSpider(CrawlSpider):
    name = "IrcsSpider"
    start_urls = [
        "http://irm.p5w.net/gszz/coplatform.html"
    ]

    def start_requests(self):
        """
        从数据库中获取所有公司的id 跟 index url
        """

        companys_id_url = MongoDBUtil.get_all_company__index_url()
        for id_url in companys_id_url:
            stockcode = id_url[0]
            # print stockcode
            interaction_url = "http://ircs.p5w.net/ircs/interaction/allQuestionForSsgs.do?condition.type=0& " \
                              "condition.stockcode=%s&condition.stocktype=S" % stockcode
            # print interaction_url
            yield FormRequest(url=interaction_url, meta={"stockcode": stockcode, "pageNo": '1'},
                              formdata={'pageNo': str(1)},
                              callback=self.parseIndex)

    def parseIndex(self, response):
        """
        处理company 第一页 index url
        """
        stockcode = response.meta["stockcode"]
        pageNo = int(response.meta["pageNo"])

        sel = Selector(response)

        qtables = sel.xpath("//table[@class='req_box2']")
        for qtable in qtables:
            tr = qtable.xpath("tr")

            question = tr[0].xpath("td")

            company_name = question[1].xpath("text()").extract()[0]
            company_id = question[1].xpath("text()").extract()[1]
            questioner = question[2].xpath("a/text()").extract_first()
            if questioner:
                questioner_account = question[2].xpath("a/@onclick").extract_first()
            else:
                questioner = question[2].xpath("text()").extract_first()
                questioner_account = None

            question_content = question[3].xpath("a/text()").extract_first()
            question_like = question[4].xpath("div/dl/dt[@class='text_sm']/span/text()").extract()[0]
            question_unlike = question[4].xpath("div/dl/dt[@class='text_sm']/span/text()").extract()[1]
            question_comment_num = question[5].xpath("dt[@class='text_sm']/span/text()").extract_first()
            question_date = question[6].xpath("text()").extract_first()
            question_state = question[7].xpath("text()").extract_first()

            quesreply = QuesReplyItem()

            if company_name:
                quesreply["company_name"] = company_name.strip()
            if company_id:
                quesreply["company_id"] = company_id.strip()
            if questioner:
                quesreply["questioner"] = questioner.strip()
            if questioner_account:
                quesreply["questioner_account"] = questioner_account.strip()
            if question_content:
                quesreply["question_content"] = question_content.strip()
            if question_like:
                quesreply["question_like"] = int(question_like.strip())
            if question_unlike:
                quesreply["question_unlike"] = int(question_unlike.strip())
            if question_comment_num:
                quesreply["question_comment_num"] = int(question_comment_num.strip())
            if question_date:
                quesreply["question_date"] = question_date.strip()
            if question_state:
                quesreply["question_state"] = question_state.strip()

            if len(tr) == 2:
                reply = tr[1].xpath("td")
                replyer = reply[2].xpath("text()").extract_first()
                reply_content = reply[3].xpath("text()").extract_first()
                reply_date = reply[6].xpath("text()").extract_first()
                reply_like = reply[4].xpath("div/dl/dt[@class='text_sm']/span/text()").extract()[0]
                reply_unlike = reply[4].xpath("div/dl/dt[@class='text_sm']/span/text()").extract()[1]
                reply_comment_num = reply[5].xpath("dt[@class='text_sm']/span/text()").extract_first()

                if replyer:
                    quesreply["replyer"] = replyer.strip()
                if reply_content:
                    quesreply["reply_content"] = reply_content.strip()
                if reply_date:
                    quesreply["reply_date"] = reply_date.strip()
                if reply_like:
                    quesreply["reply_like"] = int(reply_like.strip())
                if reply_unlike:
                    quesreply["reply_unlike"] = int(reply_unlike.strip())
                if reply_comment_num:
                    quesreply["reply_comment_num"] = int(reply_comment_num.strip())

            yield quesreply
        # 如果为首页获取 total_pages 遍历获取
        # print pageNo
        if pageNo == 1:
            content = response.body
            # print content
            total_pages = re.findall("共.*?页", content)[0]
            # print total_pages
            for pageNo in range(1, int(total_pages[3:len(total_pages)-3]) + 1):

                interaction_url = "http://ircs.p5w.net/ircs/interaction/allQuestionForSsgs.do?condition.type=0& " \
                                  "condition.stockcode=%s&condition.stocktype=S" % stockcode
                yield FormRequest(interaction_url, meta={"stockcode": stockcode, "pageNo": pageNo},
                                  formdata={'pageNo': str(pageNo)}, callback=self.parseIndex)
