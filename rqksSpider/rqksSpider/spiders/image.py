import scrapy
from loguru import logger
from rqksSpider.items import ImagespiderItem


image_type_list = {
    106: "卡通漫画",
    114: "欧美风情",
    15: "网友自拍",
    14: "唯美写真",
    16: "露出激情",
    49: "街拍偷拍",
}


class BtSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['f238605b.net']
    start_urls = ['https://w1.f238605b.net/pw/thread.php?fid=14&page=1']
    custom_settings = {
        'LOG_LEVEL': 'WARNING',
        "DEFAULT_REQUEST_HEADERS": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        }
    }
    host_name = "https://w1.f238605b.net/pw/"

    def __init__(self, parms=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fid = int(kwargs.get('fid'))
        self.min_page = kwargs.get('min_page', 1)
        self.max_page = kwargs.get('max_page', 1000)

    def start_requests(self):
        page = 1
        for page in range(int(self.min_page), int(self.max_page)):
            url = f"{self.host_name}thread.php?fid={self.fid}&page={page}"
            logger.critical({
                "msg": f"正在处理第{page}页",
                "url": url,
            })
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = {}
        rows = response.xpath(
            '//table[@id="ajaxtable"]//tr[@class="tr3 t_one"]/td/h3/a')
        for row in rows:
            href = row.xpath("@href").extract_first()
            if href[-4:] == 'html':
                item["title"] = row.xpath("text()").extract_first()
                item["url"] = f"{self.host_name}{href}"
                logger.debug(item)

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
        item["tid"] = self.tid(item["url"])
        item["image_type"] = image_type_list.get(self.fid)
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
