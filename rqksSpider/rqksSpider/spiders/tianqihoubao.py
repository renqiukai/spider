# -*- coding: utf-8 -*-
import scrapy
import logging
import time
import re

logger = logging.getLogger(__name__)


class TianqihoubaoSpider(scrapy.Spider):
    name = 'tianqihoubao'
    allowed_domains = ['tianqihoubao.com']
    start_urls = ['http://www.tianqihoubao.com/lishi/']
    host_name = 'http://www.tianqihoubao.com'
    custom_settings = {
        'LOG_LEVEL': 'WARNING',
        "FEED_EXPORT_ENCODING": 'ISO 8859-1',
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "www.tianqihoubao.com",
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        }
    }

    def parse(self, response):
        # 处理省份和城市
        dl_list = response.xpath("//div[@class='citychk']/dl")
        for dl in dl_list[:]:
            item = weatherItem()
            item["province_name"] = dl.xpath(
                "./dt/a/b/text()").extract_first()
            item["province_name"] = item["province_name"].encode(
                "ISO 8859-1").decode("gb2312")
            item["province_url"] = self.host_name + \
                dl.xpath("./dt/a/@href").extract_first()
            dd_list = dl.xpath("./dd/a")
            for dd in dd_list:
                item["city_name"] = dd.xpath(
                    "./text()").extract_first().encode(
                    "ISO 8859-1").decode("gb2312").strip()
                item["city_url"] = self.host_name + \
                    dd.xpath("./@href").extract_first()
                # logger.warn(item)
                yield scrapy.Request(
                    item["city_url"],
                    callback=self.parse_month,
                    meta={"item": item}
                )

    def parse_month(self, response):
        # 处理城市到月的页面
        item = response.meta["item"]
        ul_list = response.xpath("//div[@class='wdetail']/div/ul")
        for ul in ul_list:
            li_list = ul.xpath("./li")[1:]
            for li in li_list:
                item["month_url"] = li.xpath("./a/@href").extract_first()
                item["year"] = item["month_url"].split(".")[0][-6:][:4]
                item["month"] = item["month_url"].split(".")[0][-6:][-2:]
                if item["month_url"][0] == "/":
                    item["month_url"] = self.host_name + item["month_url"]
                else:
                    item["month_url"] = self.host_name + \
                        'lishi/' + item["month_url"]
                # logger.warn(item)
                yield scrapy.Request(
                    item["month_url"],
                    callback=self.parse_date,
                    meta={"item": item}
                )

    def parse_date(self, response):
        # 处理城市到天的页面
        item = response.meta["item"]
        tr_list = response.xpath("//table/tr")[1:]
        pattern = r""
        for tr in tr_list:
            url = tr.xpath("./td[1]/a/@href").extract_first()
            date_str = url.split(".")[0][-8:]
            item["date"] = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
            item["code"] = item["city_name"] + date_str
            if url[0] == "/":
                item["date_url"] = self.host_name + url
            else:
                item["date_url"] = self.host_name + \
                    'lishi/' + url
            item["condition"] = tr.xpath(
                "./td[2]/text()").extract_first().strip().replace(" ", "").replace("\r\n", "")
            item["temperature"] = tr.xpath(
                "./td[3]/text()").extract_first().strip().replace(" ", "").replace("\r\n", "")
            item["wind_force"] = tr.xpath(
                "./td[4]/text()").extract_first().strip().replace(" ", "").replace("\r\n", "")
            logger.warn(item)
            yield item
