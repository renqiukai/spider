"""
输入根目录

1，当前目录取得所有的目录 文件
2，是目录，返回1
3，是文件，判断文件类型
4，是图片，判断当前文件夹图片是否超过10张，如超过则表示为图片类型，记录图片地址

"""

import scrapy
from loguru import logger
from rqksSpider.items import ImagespiderItem
from scrapy.utils.response import get_base_url
import urllib.parse


def get_file_type(file_type_str):
    file_type = dict(
        image=["jpg", "jpeg", "png"],
        video=["mp4", "mpeg", "mkv", "wmv"]
    )
    for k, v in file_type.items():
        if file_type_str in v:
            return k


class ossSpider(scrapy.Spider):
    name = 'oss'
    allowed_domains = ['renqiukai.com']
    start_urls = ['http://oss.renqiukai.com:11111/temp/s_20220128/']
    custom_settings = {
        'LOG_LEVEL': 'WARNING',
        "DEFAULT_REQUEST_HEADERS": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        }
    }
    host_name = "http://oss.renqiukai.com:11111/temp/"

    def __init__(self, parms=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fid = int(kwargs.get('fid'))
        self.url = kwargs.get('url')
        self.encoding = kwargs.get('encoding')
        # self.max_page = kwargs.get('max_page', 1000)

    def start_requests(self):
        if not self.url:
            exit()
        # logger.error(self.url)

        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        rows = response.xpath('//a')
        image_num = 0
        for row in rows:
            item = {}
            href = row.xpath("@href").extract_first()
            title = row.xpath("text()").extract_first()
            url = f"{get_base_url(response)}{href}"

            item["href"] = href
            item["url"] = url
            if title == "../":
                # 上一级
                continue
            if href[-1] != "/":
                # 文件
                encoding_url = urllib.parse.unquote(
                url, encoding=self.encoding, errors="replace")
                item["title"] = encoding_url.split("/")[-1]
                item["file"] = url
                item.pop("url")
                item.pop("href")
                file_type_str = url.split(".")[-1]
                file_type = get_file_type(file_type_str)
                if file_type == "image":
                    image_num += 1
                if file_type == "video":
                    print(url)
                    yield item
            else:
                # 目录
                # pass
                # logger.critical(item["url"])
                yield scrapy.Request(
                    url=item["url"],
                    meta=item,
                    callback=self.parse,
                )
            # logger.error(item)
