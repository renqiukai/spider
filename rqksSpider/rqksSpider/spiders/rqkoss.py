import scrapy
from loguru import logger
from rqksSpider.items import ImagespiderItem
from scrapy.utils.response import get_base_url
import urllib.parse
image_type_list = {
    14: "唯美写真",
    15: "网友自拍",
    16: "露出激情",
    49: "街拍偷拍",
    21: "丝袜美腿",
    106: "卡通漫画",
    114: "欧美风情",
}

image_type_name = ["jpg","jpeg","png"]
video_type_name = ["mp4","mpeg","mkv"]


class ossSpider(scrapy.Spider):
    name = 'oss'
    allowed_domains = ['renqiukai.com']
    start_urls = ['http://oss.renqiukai.com:11111/temp/']
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
        # self.min_page = kwargs.get('min_page', 1)
        # self.max_page = kwargs.get('max_page', 1000)

    def start_requests(self):
        url = "http://oss.renqiukai.com:11111/temp/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        response.body.encoding('utf-8')
        rows = response.xpath('//a')
        for row in rows:
            item = {}
            href = row.xpath("@href").extract_first()
            title = row.xpath("text()").extract_first()
            url = f"{get_base_url(response)}{href}"
            # 字符集要把我弄死
            item["title"] = title
            # item["title_utf8"] = title.decode()
            item["title_charset"] = urllib.parse.unquote(title)
            
            item["href"] = href
            item["url"] = url
            # logger.success(item)
            if title == "..":
                continue
            if href[-1] != "/":
                item["file"] = url
                item.pop("url")
                item.pop("href")
                logger.debug(item)
                yield item
            else:
                yield scrapy.Request(
                    url=item["url"],
                    meta=item,
                    callback=self.parse,
                )

