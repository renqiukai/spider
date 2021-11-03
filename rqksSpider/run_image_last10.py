import os
from loguru import logger
from rqksSpider.spiders.image import image_type_list

for fid, name in image_type_list.items():
    max_page = 10
    base_command = f"cd rqksSpider && scrapy crawl image  -a fid={fid} -a max_page={max_page}"
    logger.debug(base_command)
    os.system(base_command)


