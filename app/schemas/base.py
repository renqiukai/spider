from fastapi import UploadFile
from pydantic import BaseModel


class SchemasBase(BaseModel):
    """
    返回模型基类
    """
    acc: str
    pwd: str
    app_secret: str
    file: UploadFile



class Success(BaseModel):
    code: int = 200
    msg: str = 'success'
