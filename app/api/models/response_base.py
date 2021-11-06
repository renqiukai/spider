from typing import Union
from pydantic import BaseModel
from datetime import datetime, date
from fastapi.responses import JSONResponse, Response  # , ORJSONResponse
import json
import http


class CJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


class rqkResponse:
    status_code = 0

    def _base(self, status_code,  message, data, code=None):
        if not code:
            code = status_code
        # data = json.dumps(data, cls=CJsonEncoder)
        return JSONResponse(
            status_code=status_code,
            content={
                'code': code,
                'msg': message,
                'data': data,
            }
        )

    def http_200(self, data, status_code=200, message="请求成功"):
        return self._base(status_code=status_code, message=message, data=data)

    def http_404(self, data, status_code=404, message="请求的页面不存在"):
        return self._base(status_code=status_code, message=message, data=data)

    def http_500(self, data, status_code=500, message="数据请求失败"):
        return self._base(status_code=status_code, message=message, data=data)

    def sucess(self, message, data, code=200):
        return self._base(status_code=200, message=message, data=data, code=code)

    def fail(self, message, data, code=500):
        return self._base(status_code=200, message=message, data=data, code=code)
