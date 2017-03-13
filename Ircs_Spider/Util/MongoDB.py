# coding:utf-8
import re
from random import Random

import pymongo


class MongoDBUtil(object):
    db = None
    dbname = "ircs"

    def getmongodb(self):
        if not self.db:
            clinet = pymongo.MongoClient("localhost", 27017)
            self.db = clinet[self.dbname]
        return self.db

    # 返回所有company 的 index url
    @staticmethod
    def get_all_company__index_url():
        db = MongoDBUtil().getmongodb()
        # print db
        table_company = db["company"]
        items = table_company.find({}, {'id': 1, 'url': 1})
        companys_id_url = list()
        for item in items:
            id_url = list()
            id_url.append(item["id"])
            id_url.append(item["url"])
            companys_id_url.append(id_url)
        return companys_id_url

    @staticmethod
    def get_hd_type_topic():
        db = MongoDBUtil().getmongodb()
        table_hd = db["huodong"]
        items = table_hd.find({"hd_url": {"$regex": "topicInteraction/bbs.do"}})
        topic_hds = list()
        for item in items:
            hd = list()
            hd.append(item["_id"])
            hd.append(item["hd_url"])
            hd.append(item["stockcode"])
            topic_hds.append(hd)
        return topic_hds

    @staticmethod
    def get_hd_type_bbs():
        db = MongoDBUtil().getmongodb()
        table_hd = db["huodong"]
        items_newzspt = table_hd.find({"hd_url": {"$regex": "newzspt.*bbs.asp"}})
        newzspt_bbs_hds = list()
        for item in items_newzspt:
            hd = list()
            hd.append(item["_id"])
            hd.append(item["hd_url"])
            hd.append(item["stockcode"])
            newzspt_bbs_hds.append(hd)
        items_zsptbs = table_hd.find({"hd_url": {"$regex": "zsptbs.*bbs.asp"}})
        zsptbs_bbs_hds = list()
        for item in items_zsptbs:
            hd = list()
            hd.append(item["_id"])
            hd.append(item["hd_url"])
            hd.append(item["stockcode"])
            zsptbs_bbs_hds.append(hd)
        return newzspt_bbs_hds, zsptbs_bbs_hds

    @staticmethod
    def get_hd_type_roadshow():
        db = MongoDBUtil().getmongodb()
        table_hd = db["huodong"]
        items_yh = table_hd.find({"hd_url": {"$regex": "yh.asp"}})
        roadshow_hds = list()
        for item in items_yh:
            hd = list()
            hd.append(item["_id"])
            hd_url = item["hd_url"]
            hd.append(hd_url[0:hd_url.find("yh.asp")] + "bbs/bbs.asp")
            hd.append(item["stockcode"])
            roadshow_hds.append(hd)
        items_yhcq = table_hd.find({"hd_url": {"$regex": "yhcq.asp"}})
        for item in items_yhcq:
            hd = list()
            hd.append(item["_id"])
            hd_url = item["hd_url"]
            hd.append(hd_url[0:hd_url.find("yhcq.asp")] + "bbs/bbs.asp")
            hd.append(item["stockcode"])
            roadshow_hds.append(hd)
        return roadshow_hds

    @staticmethod
    def get_hd_type_rsc():
        db = MongoDBUtil().getmongodb()
        table_hd = db["huodong"]
        rid_items = table_hd.find({"hd_url": {"$regex": "irm.p5w.net/rsc.*rid"}})
        rsc_rid_hds = list()
        for item in rid_items:
            hd = list()
            hd.append(item["_id"])
            hd_url = item["hd_url"]
            suburl = "http://ircs.p5w.net/ircs/topicInteraction/bbsForRoadshow.do?"
            hd.append(suburl + hd_url[hd_url.find("rid="):len(hd_url)])
            hd.append(item["stockcode"])
            rsc_rid_hds.append(hd)

        bbsfor_item = table_hd.find({"hd_url": {"$regex": "topicInteraction.*bbsFor"}})
        for item in bbsfor_item:
            hd = list()
            hd.append(item["_id"])
            hd.append(item["hd_url"])
            hd.append(item["stockcode"])
            rsc_rid_hds.append(hd)

        rsc_no_rid_hds = list()
        yh_item = table_hd.find({"hd_url": {"$regex": "irm.p5w.net/rsc.*.htm$"}})
        for item in yh_item:
            hd = list()
            hd.append(item["_id"])
            hd.append(item["hd_url"])
            hd.append(item["stockcode"])
            rsc_no_rid_hds.append(hd)
        return rsc_rid_hds, rsc_no_rid_hds

    @staticmethod
    def test_ecoding():
        db = MongoDBUtil().getmongodb()
        table_hd = db["qr_bbs_zsptbs"]
        items = table_hd.find()
        for item in items:
            hd = list()
            hd.append(item["reply_id"])
            hd.append(item["content"])
            print hd

    @staticmethod
    def test_mongodb_insert():
        db = MongoDBUtil().getmongodb()
        table_hd = db["qr_topic"]
        items = table_hd.find({'r_date': {'$exists': True}})
        print "开始复制"
        table_new = db["qr_topic_with_date"]
        table_new.insert_many(items)


# 随机生成32 位 字符串
def random_str(randomlength=32):  # 固定长度8
    str = ''  # str初始为空
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()  # random模块用于生成随机数
    for i in range(randomlength):  # 循环生成随机字符串
        str += chars[random.randint(0, length)]
    return str


def test_1():
    hds = MongoDBUtil.get_hd_type_topic()
    for hd in hds[0:1]:
        print hd[0]
    print len(hds)


def test_2():
    hds1, hds2 = MongoDBUtil.get_hd_type_bbs()
    for index, hd in enumerate(hds1):
        print index, hd[1]
        # for hd in hds2:
        #     print hd
        # print len(hds1), len(hds2)


def test_3():
    hds = MongoDBUtil.get_hd_type_roadshow()
    for hd in hds:
        print hd
    print len(hds)


def test_4():
    rsc_rid_hds, rsc_no_rid_hds = MongoDBUtil.get_hd_type_rsc()
    for hd in rsc_rid_hds:
        print hd
    for hd in rsc_no_rid_hds:
        print hd
    print len(rsc_rid_hds), len(rsc_no_rid_hds)


# MongoDBUtil.test_ecoding()
def test_ecode():
    strl = '\xd3\xc9\xd3\xda\xb8\xd6\xb2\xc4\xb2\xfa\xc6\xb7\xb2\xbb\xcd\xac'
    print strl.decode("gbk")
    lis = list()
    lis.append(strl)
    print lis
    # lis.append(strl.encode('utf-8').encode('raw_unicode_escape').decode("gbk"))
    # print lis


MongoDBUtil.test_mongodb_insert()
# test_ecode()
# hd_url = 'http://irm.p5w.net/rsc/2016/002838/01/index.htm?rid=18268'
# suburl = "http://ircs.p5w.net/ircs/topicInteraction/bbsForRoadshow.do?"
# print suburl + hd_url[hd_url.find("rid="):len(hd_url)]
# hds = MongoDBUtil.get_hd_type_topic()
# print len(hds)
# rid_set = set()
# for hd in hds:
#     hd_url = hd[1]
#     rid_pattern = re.findall("=\d+", hd_url)[0]
#     rid = rid_pattern[1:len(rid_pattern)]
#     rid_set.add(rid)
# print len(rid_set)

# newzspt_bbs_hds, zsptbs_bbs_hds = MongoDBUtil.get_hd_type_bbs()
# print len(zsptbs_bbs_hds)
# hds_no_id_url = []
# for hd in zsptbs_bbs_hds:
#     hd_id = hd[0]
#     hd_url = hd[1]
#     stockcode = hd[2]
#     rid_pattern = re.findall("selcode=\d+", hd_url)
#     if len(rid_pattern) == 0:
#         hds_no_id_url.append(hd_url)
#     else:
#         boardid = rid_pattern[0][8:len(rid_pattern[0])]
#         print boardid
# print len(hds_no_id_url)
# print hds_no_id_url
# test_4()
