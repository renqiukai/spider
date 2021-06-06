# -*- coding: utf-8 -*-
import scrapy
import logging

logger = logging.getLogger(__name__)


class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['sun0769.com']
    start_urls = [
        'https://wz.sun0769.com/political/index/politicsNewest?id=1&page=1']

    def parse(self, response):
        # 处理start_urls
        ul_list = response.xpath(
            "//ul[@class='title-state-ul']/li")
        # logger.warn(tr_list)
        for ul in ul_list:
            item = {}
            # item = {}
            item["tid"] = tr.xpath("./td[1]/text()").extract_first()
            item["ttype"] = tr.xpath(
                "./td[2]/a[@class='red14']/text()").extract_first()
            item["title"] = tr.xpath(
                "./td[2]/a[@class='news14']/text()").extract_first()
            item["area"] = tr.xpath(
                "./td[2]/a[@class='t12h']/text()").extract_first()
            item["url"] = tr.xpath(
                "./td[2]/a[@class='news14']/@href").extract_first()
            item["status"] = tr.xpath("./td[3]/span/text()").extract_first()
            item["author"] = tr.xpath("./td[4]/text()").extract_first()
            item["pub_time"] = tr.xpath("./td[5]/text()").extract_first()
            # logger.warn(item)
            yield scrapy.Request(
                item["url"],
                callback=self.parse_detail,
                meta={"item": item}
            )

        next_url = response.xpath("//a[text()='>']/@href").extract_first()
        if next_url:
            resp = scrapy.Request(next_url, callback=self.parse)
            yield resp

    def parse_detail(self, response):
        item = response.meta["item"]
        t_detail = response.xpath("//td[@class='txt16_3']")
        item["content"] = response.xpath(
            "//td[@class='txt16_3']/text()").extract_first()
        if not item["content"]:
            item["content"] = t_detail.xpath(
                "./div[@class='contentext']/text()").extract_first()
            item["content_img"] = t_detail.xpath(
                "./div[@class='textpic']/img/@src").extract_first()
        logger.warn(item)
        yield item
