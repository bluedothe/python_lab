#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/7/15
'''

import pymongo
from bson.objectid import ObjectId

import spider_ths.shares_data.settings as settings
from spider_ths.shares_data.items import Company

class SharesDataPipeline(object):

    def open_spider(self, spider):
        self.dbClient = pymongo.MongoClient(settings.MONGO_URI)
        self.db = self.dbClient[settings.MONGO_DB]

    def close_spider(self, spider):
        self.dbClient.close()

    def process_item(self, item, spider):
        if isinstance(item, Company):
            company = self.db.company.find_one({"share_id": item['share_id']})
            self.db.company.update_one(
                {"share_id": item['share_id']},
                {"$set": dict(item)}, upsert=True
            )
            # if company == None:
            #     # print('不存在该公司')
            #     result = self.db.company.update_one(
            #         {"share_id": item['share_id']},
            #         {"$set": dict(item)}, upsert=True
            #     )
            # else:
            #     print(item['share_id'], '公司已存在')


        return item

if __name__ == '__main__':
    pass