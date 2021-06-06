# -*- coding: utf-8 -*-
import scrapy
from loguru import logger
from copy import deepcopy


class DoutulaSpider(scrapy.Spider):
    name = 'doutula'
    allowed_domains = ['doutula.com']
    start_urls = ['https://www.doutula.com/article/list/?page=1']
    host_name = "https://www.doutula.com"
    custom_settings = {
        'LOG_LEVEL': 'WARN',
        # 'LOG_FILE': '*.txt',
        "DEFAULT_REQUEST_HEADERS": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_page = kwargs.get('max_page')
        if not self.max_page:
            self.max_page = 1000

    def start_requests(self):
        page = 1
        for page in range(1, int(self.max_page)):
            url = f"https://www.doutula.com/article/list/?page={page}"
            logger.critical({
                "msg": f"正在处理第{page}页",
                "url": url,
            })
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        photos = response.xpath("//a[@class='list-group-item random_list']")
        for photo in photos[:]:
            item = {}
            item["title"] = photo.xpath("./div[1]/text()").extract_first()
            item["url"] = photo.xpath("./@href").extract_first()
            yield scrapy.Request(
                item["url"],
                callback=self.parse_detail,
                meta={"item": deepcopy(item)}
            )

    def parse_detail(self, response):
        # 小贴士
        photos = response.xpath("//img[@referrerpolicy='no-referrer']")
        item = response.meta["item"]
        if "photo_url" not in item:
            item["photo_url"] = []
        for idx, photo in enumerate(photos[:]):
            item["photo_url"].append(photo.xpath('./@src').extract_first())
            logger.debug(item)
            yield item
