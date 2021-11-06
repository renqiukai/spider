'''
@author: renqiukai
@Date: 2020-04-08 10:07:37
@Description: 
@LastEditTime: 2020-06-18 11:23:23
'''

import time
from fastapi import APIRouter

from fastapi import Depends, FastAPI, Header, HTTPException
from app.api.routes import spider
from app.core.jwt_api import check_jwt_token
from app.core.logging import logger

TOKEN_NOT_FOUND = HTTPException(
    status_code=502, detail="请检查TOKEN是否存放在headers中")


async def get_token_header(token: str = Header(None, description="安全令牌")):
    if not token:
        raise TOKEN_NOT_FOUND
    result = check_jwt_token(token)
    logger.debug(result)
    return result

router = APIRouter()
router.include_router(
    spider.router,
    prefix="/spider",
    tags=["爬虫"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
