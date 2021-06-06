# -*- coding: utf-8 -*-
import scrapy
import logging
# from mySpider.items import jzmItem
import re
from loguru import logger

class ImdbSpider(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/chart/top']
    host_name = "https://www.imdb.com"
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
        tr_list = response.xpath(
            "//table[@data-caller-name='chart-top250movie']/tbody/tr")
        for tr in tr_list:
            item = {}
            item["image"] = tr.xpath("./td[1]/a/img/@src").extract_first()
            item["rank"] = tr.xpath(
                "./td[2]/text()").extract_first().strip().replace(".", "")
            item["title"] = tr.xpath("./td[2]/a/text()").extract_first()
            item["created"] = tr.xpath("./td[2]/span/text()").extract_first()
            item["rate"] = tr.xpath("./td[3]/strong/text()").extract_first()
            logger.debug(item)
            yield item
