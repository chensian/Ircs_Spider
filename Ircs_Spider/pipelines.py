# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from Ircs_Spider.items import QuesReplyItem, HuoDongItem, InteractionItem, NewzsptBBSItem, ZsptbsBBSItem


class MongoDBPipleline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["ircs"]
        self.QuesReply = db["quesreply_with_questioner"]
        self.HuoDong = db["huodong"]
        self.QRTopic = db["qr_topic"]
        self.QRNewzsptBBS = db["qr_bbs_newzspt_new"]
        self.QRZsptbs = db["qr_bbs_zsptbs"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, QuesReplyItem):
            try:
                self.QuesReply.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, HuoDongItem):
            try:
                self.HuoDong.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, InteractionItem):
            try:
                self.QRTopic.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, NewzsptBBSItem):
            try:
                self.QRNewzsptBBS.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, ZsptbsBBSItem):
            try:
                self.QRZsptbs.insert(dict(item))
            except Exception:
                pass
        return item
