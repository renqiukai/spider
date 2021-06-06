# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
from loguru import logger

class DmSpider(scrapy.Spider):
    name = 'dm'
    allowed_domains = ['cmiyu.com']
    start_urls = ['http://www.cmiyu.com/etmy/mytid%7D1.html']
    host_name = "http://www.cmiyu.com"
    custom_settings = {
        'LOG_LEVEL': 'WARN',
        # 'LOG_FILE': '*.txt',
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
        }
    }

    def parse(self, response):
        cats = response.xpath("//div[@class='miyuheader']/ul/li")
        for cat in cats[:]:
            item = {}
            item["cat_title"] = cat.xpath("./a/text()").extract_first()
            item["cat_url"] = self.host_name + \
                cat.xpath("./a/@href").extract_first()
            logger.debug(item)
            yield scrapy.Request(
                item["cat_url"],
                callback=self.parse_list,
                meta={"item": deepcopy(item)}
            )

    def parse_list(self, response):
        dm_list = response.xpath("//div[@class='list']/ul/li")
        for dm in dm_list[:]:
            item = response.meta["item"]
            item["title"] = dm.xpath("./a/@title").extract_first()
            item["url"] = self.host_name + \
                dm.xpath("./a/@href").extract_first()
            logger.debug(item)
            yield scrapy.Request(
                item["url"],
                callback=self.parse_detail,
                meta={"item": deepcopy(item)}
            )
        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        logger.debug(next_url)
        if next_url:
            next_url = item["cat_url"] + next_url
            logger.debug(f"next_url:{next_url}")
            yield scrapy.Request(
                next_url,
                callback=self.parse_list,
                meta={"item": deepcopy(item)}
            )

    def parse_detail(self, response):
        # 小贴士
        zy = response.xpath("//div[@class='zy']/p/text()").extract_first()
        md = response.xpath("//div[@class='md']/h3[2]/text()").extract_first()
        item = response.meta["item"]
        item["zy"] = zy
        item["md"] = md

        logger.debug(item)
        yield item
