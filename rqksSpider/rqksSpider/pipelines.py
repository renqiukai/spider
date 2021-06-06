# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy


class RqksspiderPipeline:
    def process_item(self, item, spider):
        if spider.name == "image":
            for image_url in item['photo_url']:
                yield image_url
        return item


# class ImagespiderPipeline(RqksspiderPipeline):

#     def get_media_requests(self, item, info):
#         # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield
#         for image_url in item['photo_url']:
#             yield scrapy.Request(image_url)
