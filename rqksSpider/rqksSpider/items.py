# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RqksspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ImagespiderItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    photo_url = scrapy.Field()
