# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
from loguru import logger


class DoSpider(scrapy.Spider):
    name = 'ren'
    allowed_domains = ['resgain.net']
    start_urls = ['http://ren.resgain.net/name_list.html']
    host_name = "http://ren.resgain.net"
    custom_settings = {
        'LOG_LEVEL': 'WARN',
        # 'LOG_FILE': '*.txt',
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
        }
    }

    def start_requests(self):
        page = 1
        for page in range(1, 19):
            url = f"http://ren.resgain.net/name_list_{page}.html"
            logger.critical({
                "msg": f"正在处理第{page}页",
                "url": url,
            })
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        names = response.xpath("//div[@class='col-xs-12']/div[@class='btn btn-default btn-lg namelist']/div[1]/text()").extract()
        for name in names[:]:
            item = {}
            item["name"] = name
            logger.debug(item)
            yield item
