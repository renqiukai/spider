# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
from loguru import logger


class DoSpider(scrapy.Spider):
    name = 'do1'
    allowed_domains = ['do1.com.cn']
    start_urls = ['https://wbg.do1.com.cn/jxal/page/2']
    host_name = "https://wbg.do1.com.cn"
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
        for page in range(1, int(self.max_page)):
            url = f"https://wbg.do1.com.cn/jxal/page/{page}"
            logger.critical({
                "msg": f"正在处理第{page}页",
                "url": url,
            })
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        cards = response.xpath("//div[@class='card-content']/a")
        for card in cards[:]:
            item = {}
            item["card_title"] = card.xpath("./div/text()").extract_first()
            item["card_url"] = card.xpath("./@href").extract_first()
            yield scrapy.Request(
                url=item["card_url"],
                meta=item,
                callback=self.parse_detail)

    def parse_detail(self, response):
        item = response.meta
        subtitle = response.xpath("//div[@class='article-subtitle clearfix']")
        source, create_date, read_num = subtitle.xpath(
            "./span/text()").extract()
        source = source.replace("来源：", "")
        read_num = read_num.replace("阅读：", "")
        abstract = response.xpath(
            "//div[@class='article-abstract']/p/text()").extract_first()
        text = response.xpath(
            "//article[@class='article-container']//p//text()").extract()
        item["source"] = source
        item["create_date"] = create_date
        item["read_num"] = read_num
        item["abstract"] = abstract
        # item["text"] = "\n".join(text)
        item["text"] = text
        logger.debug(item)
        yield item
