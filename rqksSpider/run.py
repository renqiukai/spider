from prettytable import PrettyTable
import os
from loguru import logger

spiders = [
    {"name": "古诗文", "spider_name": "gushiwen", },
    {"name": "图片", "spider_name": "image", },
    {"name": "imdb top250", "spider_name": "imdb", },
    {"name": "鸡汤", "spider_name": "jt", },
    {"name": "磁力链接", "spider_name": "magnet", },
    {"name": "斗图啦", "spider_name": "doutula", },
    {"name": "灯迷", "spider_name": "dm", },
]


tb = PrettyTable()
tb.field_names = ["name", "spider_name", ]

for spider in spiders:
    tb.add_row(spider.values())
logger.debug(f"\n{tb}")
spider_name = input("pls enter spider_name:")
base_command = f"scrapy crawl {spider_name}"
encoding = f"-s FEED_EXPORT_ENCODING=UTF-8"
output = f"-o {spider_name}.json"
params = ""
max_page = input("pls enter max page:")
if spider_name == "image":
    fid = input("pls enter fid:")
    output = f"-o {spider_name}-{fid}.json"
    params = f"-a fid={fid}"
if max_page:
    params += f" -a max_page={max_page}"
command = f"cd rqksSpider && {base_command} {output} {encoding} {params}"
logger.debug(command)
os.system(command)
