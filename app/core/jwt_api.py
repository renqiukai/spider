from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt
from fastapi import Header, HTTPException
# 导入配置文件
from app.core import config

ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """
    # 生成token
    :param subject: 保存到token的值
    :param expires_delta: 过期时间
    :return:
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "data": subject}
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def check_jwt_token(
    token: Optional[str] = Header(None)
) -> Union[str, Any]:
    """
    解析验证 headers中为token的值 当然也可以用 Header(None, alias="Authentication") 或者 alias="X-token"
    :param token:
    :return:
    """

    try:
        payload = jwt.decode(
            token,
            config.SECRET_KEY, algorithms=[ALGORITHM]
        )
        return payload
    except (jwt.JWTError, jwt.ExpiredSignatureError, AttributeError):
        # 抛出自定义异常， 然后捕获统一响应
        raise HTTPException(status_code=500, detail="TOKEN不正确")
