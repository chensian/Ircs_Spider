# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


# 在线提问数据
class QuesReplyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 公司的名称
    company_name = Field()
    # 公司id == stockcode
    company_id = Field()
    # 提问者
    questioner = Field()

    # 是否注册用户
    questioner_account = Field()

    # 提问内容
    question_content = Field()

    question_like = Field()
    question_unlike = Field()
    question_comment_num = Field()

    # 提问日期
    question_date = Field()
    # 提问状态 是否回答
    question_state = Field()

    # 回复者
    replyer = Field()
    # 回复内容
    reply_content = Field()
    # 回复日期
    reply_date = Field()

    reply_like = Field()
    reply_unlike = Field()
    reply_comment_num = Field()


# 活动交流会
class HuoDongItem(Item):
    # stockcode
    stockcode = Field()
    hd_title = Field()
    hd_url = Field()
    hd_picture_url = Field()


# eg: http://ircs.p5w.net/ircs/topicInteraction/questionPage.do POST {pageNo, rid}
# topic  rsc
class InteractionItem(Item):

    hd_id = Field()
    rid = Field()
    stockcode = Field()
    q_loginId = Field()
    score = Field()
    q_date = Field()
    q_isclosecomment = Field()
    q_name = Field()
    c_isclosecomment = Field()
    q_isguest = Field()
    q_id = Field()
    q_jblb = Field()
    r_officename = Field()
    r_id = Field()
    r_content = Field()
    isCheck = Field()
    r_name = Field()
    r_date = Field()
    hasCancel = Field()
    q_iscloseappraise = Field()
    stocktype = Field()
    q_content = Field()
    c_iscloseappraise = Field()


# eg:  http://newzspt.p5w.net/bbs/question_page.asp?boardid=3763&bbs=1&pageNo=1
# BBS  newzspt
class NewzsptBBSItem(Item):
    # 交流会 id
    hd_id = Field()
    # 请求参数 id
    boardid = Field()
    # url
    roadshow_hds_url = Field()
    # 股票代码
    stockcode = Field()

    q_name = Field()
    q_content = Field()
    q_loginuserid = Field()
    q_wtly = Field()
    q_jblb = Field()
    q_ofname = Field()

    r_name = Field()
    r_officename = Field()
    r_content = Field()

    # 页码
    pageNo = Field()
    # 记录页内行号
    pagerowNo = Field()


# eg: http://zsptbs.p5w.net/bbs/chatbbs/left.asp?boardid=1153&pageNo=2
# BBS  zsptbs
class ZsptbsBBSItem(Item):
    # 交流会 id
    hd_id = Field()
    # 请求参数 id
    boardid = Field()
    # 股票代码
    stockcode = Field()

    quest_id = Field()
    reply_id = Field()
    spokesman = Field()
    content = Field()

    # 页码
    pageNo = Field()
    # 记录页内行号
    pagerowNo = Field()
