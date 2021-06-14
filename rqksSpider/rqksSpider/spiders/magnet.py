import scrapy
from loguru import logger


class BtSpider(scrapy.Spider):
    name = 'magnet'
    allowed_domains = ['1080pgqzz.info', 'downsx.net']
    start_urls = ['https://z1.1080pgqzz.info/pw/thread.php?fid=18&page=1']
    custom_settings = {
        'LOG_LEVEL': 'WARNING',
        "DEFAULT_REQUEST_HEADERS": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        }
    }
    host_name = "https://z1.1080pgqzz.info/pw/"
    max_page = 10
    fid = 3

    def start_requests(self):
        page = 1
        self.max_page = int(self.max_page)
        for page in range(1, self.max_page):
            url = f"https://z1.1080pgqzz.info/pw/thread.php?fid={self.fid}&page={page}"
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
                # item["href"] = href
                item["url"] = f"{self.host_name}{href}"
                yield scrapy.Request(
                    url=item["url"],
                    meta=item,
                    callback=self.parse_detail,
                )

    def parse_detail(self, response):
        item = response.meta
        item["title"] = response.xpath("//span[@id='subject_tpc']/text()").extract_first()
        dl_list = response.xpath('//div[@class="tpc_content"]//a')
        for dl in dl_list:
            dl_url = dl.xpath('@href').extract_first()
            if "downsx" in dl_url:
                item["dl_url"] = dl_url
                yield scrapy.Request(url=dl_url, callback=self.magnet_url, meta=item, errback=self.error)

    def magnet_url(self, response):
        item = response.meta
        href = response.xpath(
            '//a[text()="磁力連結"]/@href').extract_first()
        item["magnet_url"] = href
        logger.debug(item)
        yield item

    def error(self, response):
        logger.error(response)
