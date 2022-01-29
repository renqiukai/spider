import scrapy
from loguru import logger


class ecSpider(scrapy.Spider):
    name = 'ec'
    allowed_domains = ['echangwang.com']
    start_urls = ['http://www.echangwang.com/pic/listpic_1.html']
    custom_settings = {
        'LOG_LEVEL': 'WARNING',
        "DEFAULT_REQUEST_HEADERS": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        }
    }
    host_name = "http://www.echangwang.com/pic/"

    def __init__(self, parms=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_page = kwargs.get('min_page', 1)
        self.max_page = kwargs.get('max_page', 1)

    def start_requests(self):
        for page in range(int(self.min_page), int(self.max_page)+1):
            item = {
                # "page": page,
            }
            url = f"{self.host_name}listpic_{page}.html"
            logger.critical({
                "msg": f"正在处理第{page}页",
                "url": url,
            })
            yield scrapy.Request(url=url, callback=self.parse, meta=item)

    def parse(self, response):
        item = response.meta
        rows = response.xpath(
            '//div[@class="bm_c xld"]//dt//a')
        for row in rows:
            href = row.xpath("@href").extract_first()
            if href[-4:] == 'html':
                item["title"] = row.xpath("text()").extract_first()
                item["url"] = f"{self.host_name}{href}"
                item["tid"] = self.tid(item["url"])
                # logger.debug(item)
            yield scrapy.Request(
                url=item["url"],
                meta=item,
                callback=self.parse_detail,
            )

    def parse_detail(self, response):
        item = response.meta
        imgs = response.xpath('//table[@class="vwtb"]//img')
        # if "photo_url" not in item:
        item["photo_url"] = []
        for img in imgs:
            img_url = img.xpath('@src').extract_first()
            item["photo_url"].append(img_url)
        logger.debug(item)
        yield item

    def tid(self, url):
        a = url.split("/")
        if a:
            b = a[-1].split(".")
            if b:
                return b[0]
