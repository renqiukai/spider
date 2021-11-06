from pydantic import BaseModel
import time
from datetime import datetime
from typing import Optional

import pandas as pd
from fastapi import APIRouter, File, Query, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse

from app.api.utils.excel import save_excel
from app.core.logging import logger
from app.db.mysql_api import execSql
from decimal import Decimal
from app.core.jwt_api import create_access_token, check_jwt_token
from app.core.config import APPID, SECRET_KEY
from app.api.errors.http_error import *
router = APIRouter()


def check_appid_secret(appid, secret):
    sql = f"""
    select appid,secret from t_sys_user
    where appid='{appid}';
    """
    rows = execSql(sql)
    if not rows:
        logger.error("找不到appid.")
        raise ACCESS_FAIL
    row = rows[0]
    if secret != row.get("secret"):
        logger.error("secret错误。")
        raise ACCESS_FAIL


@router.get("/token", summary="取得TOKEN",)
async def get_token(
    appid: str = Query(..., description="应用ID"),
    secret: str = Query(..., description="应用密钥"),
):
    """
    ### 请求参数：
    ----
    |参数名|是否必填|描述|备注|
    |----|----|----|----|
    |appid|是|应用ID||
    |secret|是|应用密钥||

    ### 返回值：
    ----
    |字段名 |描述|备注|
    |----|----|----|
    |token|安全令牌||
    |expires|过期时间|时间戳，有效时间为7天，注意保存。|

    ### 状态码(根据status_code进行判断请求是否成功，不单独提供code字段)
    ----
    |status_code|是否成功|detail(描述)
    |----|----|----|
    |200|是|成功|
    |501|否|授权失败，请检查APPID/SECRET|
    """
    check_appid_secret(appid, secret)
    data = {
        "appid": appid,
        "secret": secret,
    }
    logger.debug(data)
    token = create_access_token(data)
    result = check_jwt_token(token)
    exp = result.get("exp")
    logger.debug(result)
    return {"token": token, "expires": exp}
