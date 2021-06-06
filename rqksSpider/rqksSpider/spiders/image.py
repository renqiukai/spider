import scrapy
from loguru import logger
from rqksSpider.items import ImagespiderItem


class BtSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['1080pgqzz.info']
    start_urls = ['https://z1.1080pgqzz.info/pw/thread.php?fid=14&page=1']
    custom_settings = {
        'LOG_LEVEL': 'WARNING',
        "DEFAULT_REQUEST_HEADERS": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        }
    }
    host_name = "https://z1.1080pgqzz.info/pw/"

    def __init__(self, parms=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fid = kwargs.get('fid')
        self.max_page = kwargs.get('max_page')
        if not self.max_page:
            self.max_page = 1000

    def start_requests(self):
        page = 1
        for page in range(1, int(self.max_page)):
            url = f"https://z1.1080pgqzz.info/pw/thread.php?fid={self.fid}&page={page}"
            logger.critical({
                "msg": f"正在处理第{page}页",
                "url": url,
            })
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = ImagespiderItem()
        rows = response.xpath(
            '//table[@id="ajaxtable"]//tr[@class="tr3 t_one"]/td/h3/a')
        for row in rows:
            href = row.xpath("@href").extract_first()
            if href[-4:] == 'html':
                item["title"] = row.xpath("text()").extract_first()
                item["url"] = f"{self.host_name}{href}"
                yield scrapy.Request(
                    url=item["url"],
                    meta=item,
                    callback=self.parse_detail,
                )

    def parse_detail(self, response):
        item = response.meta
        imgs = response.xpath('//div[@class="tpc_content"]//img')
        if "photo_url" not in item:
            item["photo_url"] = []

        for img in imgs:
            img_url = img.xpath('@src').extract_first()
            item["photo_url"].append(img_url)
        logger.debug(item)
        yield item
