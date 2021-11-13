# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from loguru import logger
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from datetime import datetime


def get_now_str():
    dt = datetime.now()
    return dt.strftime('%Y-%m-%d %H:%M:%S')

class RqksspiderPipeline:
    def __init__(self) -> None:
        connection_string = 'mongodb://admin:cjdg123456@cloud.renqiukai.com:27017/rqk?authSource=admin'
        self.client = MongoClient(connection_string)
        self.db = self.client["spider"]

    def process_item(self, item, spider):
        # db.jita.createIndex({tid:1},{unique:true}) 
        if spider.name == "image":
            try:
                item["create_time"] = get_now_str()
                item["update_time"] = get_now_str()
                item["delete_flag"] = 0
                self.db["images"].insert_one(item)
            except DuplicateKeyError:
                pass

        elif spider.name == "tianqihoubao":
            item.pop("_id") if "_id" in item else None
            self.db["tianqihoubao"].insert_one(item)
        elif spider.name == "jita":
            item.pop("_id") if "_id" in item else None
            try:
                item["create_time"] = get_now_str()
                item["update_time"] = get_now_str()
                item["delete_flag"] = 0
                self.db["jita"].insert_one(item)
            except DuplicateKeyError:
                pass
        else:
            pass
        return item


# class ImagespiderPipeline(RqksspiderPipeline):

#     def get_media_requests(self, item, info):
#         # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield
#         for image_url in item['photo_url']:
#             yield scrapy.Request(image_url)
