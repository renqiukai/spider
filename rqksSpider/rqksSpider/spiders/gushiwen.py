# -*- coding: utf-8 -*-
import scrapy
import logging
import re
from copy import deepcopy
from loguru import logger



class GushiwenSpider(scrapy.Spider):
    name = 'gushiwen'
    allowed_domains = ['gushiwen.org']
    start_urls = ['https://www.gushiwen.org']
    host_name = "https://so.gushiwen.org"
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
        poem_type_list = response.xpath(
            "//div[@class='main3']/div[2]/div[1]/div[2]/a")
        logger.debug(poem_type_list)
        for poem_type in poem_type_list[-3:]:
            item = {}
            item["poem_type"] = poem_type.xpath('./text()').extract_first()
            item["poem_type_url"] = poem_type.xpath('./@href').extract_first()
            yield scrapy.Request(
                item["poem_type_url"],
                callback=self.parse_list,
                meta={"item": deepcopy(item)}
            )

    def parse_list(self, response):
        item = response.meta["item"]
        poem_type_list = response.xpath("//div[@class='typecont']")
        for poem_type in poem_type_list:
            item["poem_label"] = poem_type.xpath(
                './div[1]/strong/text()').extract_first()
            for poem in poem_type.xpath("./span"):
                item["poem"] = poem.xpath('./a/text()').extract_first()
                item["author"] = poem.xpath('./text()').extract_first()
                poem_url = poem.xpath('./a/@href').extract_first()
                item["poem_url"] = f"{self.host_name}{poem_url}" if "http" not in  poem_url else poem_url
                yield scrapy.Request(
                    item["poem_url"],
                    callback=self.parse_detail,
                    meta={"item": deepcopy(item)}
                )

    def parse_detail(self, response):
        item = response.meta["item"]
        content1 = response.xpath(
            "//div[@class='contson']/text()[1]").extract_first()
        content2 = response.xpath(
            "//div[@class='contson']/text()[2]").extract_first()
        item["content"] = f"{content1}{content2}".strip()
        logger.debug(item)
        yield item
