"""
怎么爬全站
1，爬分类
2，分类对应的列表页，取得最大页数
3，取详情页
31，是图片，爬取图片URL
32，是magnet取磁力链接
33，是文章取text
"""
import scrapy
from loguru import logger
from rqksSpider.items import ImagespiderItem


class BtSpider(scrapy.Spider):
    name = 'bt'
    allowed_domains = ['f238605b.net']
    start_urls = ['https://w1.f238605b.net/pw/index.php']
    custom_settings = {
        'LOG_LEVEL': 'WARNING',
        "DEFAULT_REQUEST_HEADERS": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        }
    }
    host_name = "https://w1.f238605b.net/pw/"

    def __init__(self, parms=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fid = kwargs.get('fid')
        self.max_page = kwargs.get('max_page')
        if not self.max_page:
            self.max_page = 1000

    def start_requests(self):
        url = "https://w1.f238605b.net/pw/index.php"
        yield scrapy.Request(url=url, callback=self.cat)

    def cat(self, response):
        item = {}
        rows = response.xpath(
            '//table//tr//span//a')
        for row in rows:
            href = row.xpath("@href").extract_first()
            item["fid"] = href.split("=")[-1]
            item["cat_first_url"] = f"{self.host_name}thread.php?fid={item['fid']}&page=1"
            item["cat_title"] = row.xpath("text()").extract_first()
            yield scrapy.Request(url=item["cat_first_url"], callback=self.max_id, meta=item)

    def max_id(self, response):
        item = response.meta
        if item:
            page_text = response.xpath(
                "//span[@class='pagesone']/text()").extract_first()
            page_text = page_text.replace("\xa0", "")
            page_text = page_text.split("/")[-1]
            max_page = page_text.replace("  Go ", "")
            item["max_page"] = max_page
            for page in range(1, int(max_page)):
                url = f"https://w1.f238605b.net/pw/thread.php?fid={item['fid']}&page={page}"
                logger.critical({
                    "msg": f"正在处理第{page}页",
                    "url": url,
                    "max_page": max_page,
                })
                yield scrapy.Request(url=url, callback=self.parse, meta=item)

    def parse(self, response):
        item = response.meta
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
