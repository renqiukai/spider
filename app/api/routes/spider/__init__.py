from fastapi.param_functions import Body
from pydantic import BaseModel
import time
from datetime import datetime
from typing import Optional
import requests
import pandas as pd
from fastapi import (APIRouter, File, Query, UploadFile,
                     HTTPException, BackgroundTasks)
from fastapi.responses import FileResponse, JSONResponse
from .models import SpiderInfo
from app.core.logging import logger
import json
from app.api.models.response_base import rqkResponse
import os
from rqksSpider.rqksSpider.spiders.image import image_type_list
router = APIRouter()







@router.get("/list", summary="爬虫列表",)
async def list(
    title: str = Query(None, description="标题"),
    pageNo: int = Query(1),
    pageSize: int = Query(10),
):
    c = SpiderInfo()
    condition = {}
    if title:
        condition["title"] = {"$regex": f"{title}"}

    total = c.collection.count_documents(condition)
    rows = c.list(condition=condition, page_num=pageNo,
                  page_size=pageSize)
    # rows = c.collection.find({"delete_flag":0})
    data = []
    for index, row in enumerate(rows, start=1):
        logger.debug(row)
        row["_id"] = str(row["_id"])
        data.append(row)
    logger.debug(data)
    return rqkResponse().sucess(message="查询成功", data=data)


@router.get("/info", summary="详情",)
async def info(
    _id: str = Query(None, description="_id"),
):
    c = SpiderInfo()
    row = c.read(_id)
    # todo:异步任务，下载图片，存入自己的CDN服务，替换URL，这个功能未实现。
    if not row:
        raise HTTPException(500, "查询失败")
    row["_id"] = str(row["_id"])
    return rqkResponse().sucess(message="查询成功", data=row)


@router.post("/add", summary="增加",)
async def add(
    spider_name: str = Query(..., description="spider_name"),
    params: str = Query("", description="params"),
):
    c = SpiderInfo()
    data = {
        "spider_name": spider_name,
        "params": params,
    }
    result = c.create(data)
    result["_id"] = str(result["_id"])
    return rqkResponse().sucess(message="创建成功", data=result)


@router.delete("/delete", summary="删除",)
async def delete(
    _id: str = Query(None, description="_id"),
):
    c = SpiderInfo()
    result = c.delete(_id)
    result["_id"] = str(result["_id"])
    return rqkResponse().sucess(message="删除成功", data=result)


@router.get("/image/exec", summary="执行",)
async def exec(
    # spider_name: str = Query(None, description="爬虫名字"),
    # params: str = Query(None, description="参数字符串"),
):
    for fid, name in image_type_list.items():
        max_page = 10
        base_command = f"cd rqksSpider && scrapy crawl image  -a fid={fid} -a max_page={max_page}"
        logger.debug(base_command)
        os.system(base_command)
    return rqkResponse().sucess(message="删除成功", data=[])
