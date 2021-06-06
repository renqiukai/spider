# -*- coding: utf-8 -*-
import scrapy
import logging
import time
import re
from copy import deepcopy
from loguru import logger



class JtSpider(scrapy.Spider):
    name = 'jt'
    allowed_domains = ['59xihuan.cn']
    start_urls = ['http://www.59xihuan.cn/']
    host_name = 'http://www.59xihuan.cn'
    custom_settings = {
        'LOG_LEVEL': 'WARNING',
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "bdshare_ty=0x18; PHPSESSID=elc848ekaou9r8k9uknqg15di7; Hm_lvt_58553e6d81fbcb1bbbf47c3c42a8b484=1552714223; Hm_lpvt_58553e6d81fbcb1bbbf47c3c42a8b484=1552714223",
            "Host": "www.59xihuan.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        }
    }

    def parse(self, response):
        chickenSoups = response.xpath(
            "//div[@class='mLeft']/div[@class='post']")
        for chickenSoup in chickenSoups[:]:
            item = {}
            title = chickenSoup.xpath(".//div[@class='pic_text1']/text()").extract_first()
            if title:
                item["title"] = title.strip()
                logger.debug(item)
                yield item
        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url:
            next_url = f"{self.host_name}{next_url}"
            resp = scrapy.Request(next_url, callback=self.parse)
            yield resp
