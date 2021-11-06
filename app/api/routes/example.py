'''
@author: renqiukai
@Date: 2020-06-05 11:46:31
@Description: cjdg user tools
@LastEditTime: 2020-06-17 01:33:25
'''
from starlette.responses import JSONResponse
from app.api.models.response_base import rqkResponse
import time
import pandas as pd
from cjdg_open_api.base import request_accesstoken
# from cjdg_open_api.cjdg_user import cjdgUser
from fastapi import APIRouter, File, Query, UploadFile
from fastapi.responses import FileResponse
from app.api.utils.excel import save_excel
from app.core.logging import logger
from app.db.mysql_api import execSql

router = APIRouter()


@router.post("/file_export", summary="文件读取导出")
async def batch_switch_user_id(file: UploadFile = File(...),
                               app_id: str = Query("xtep")):
    """
    - 批量转换USERID。
    - 上传excel文件，excel文件中有一列为【登录名】。
    - 输入对应的appid。
    - 返回excel文件。
    """
    df = pd.read_excel(file.file)
    accounts_list = [login_name[1] for login_name in enumerate(df["登录名"])]
    accounts_list = list(map(str, accounts_list))
    accounts_str = "','".join(accounts_list)
    logger.info(accounts_str)
    sql = f"""
    select
    login_name '登录名'
    ,sys_user_id '用户ID' from sys_user
    where login_name in ('{accounts_str}');
    """
    rows = execSql(sql)
    filename = f"超导_用户ID列表"
    params = {
        "data": rows,
        "filepath": None,
        "filename": filename,
        "sheet_name": "userids",
        "file_type": "xlsx",
    }
    result = save_excel(**params)
    file_path = result.get("file_full_path")
    filename = result.get("file_name")
    return FileResponse(file_path, filename=filename, media_type="application/msexcel")


@router.get("/login", summary="登录")
async def batch_switch_user_id(
    username: str = Query(..., description="用户名"),
    password: str = Query(..., description="密码"),
):
    data = rqkResponse().http_200(data=[20000])

    return data
