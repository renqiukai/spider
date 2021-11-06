from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"msg": [exc.detail]}, status_code=exc.status_code)

# 授权
ACCESS_FAIL = HTTPException(501, detail="授权失败，请检查APPID/SECRET")


# 会员
CHANGE_INFO_FAIL = HTTPException(400, detail="会员原始数据未修改成功",)
CHANGE_LEVEL_FAIL = HTTPException(401, detail="会员等级信息未修改成功",)
CHANGE_USER_FAIL = HTTPException(402, detail="导购数据未修改成功",)
GET_CUSTOMER_FAIL = HTTPException(403, detail="无法查询到此会员信息")
CUSTOMER_DATA_ERROR = HTTPException(404, detail="会员原始数据错误")
BRANCH_NOT_FOUND = HTTPException(405, detail="查找不到分会信息或分会提成未变化")
GUIDE_SYNC_FAIL = HTTPException(406, detail="草动虚拟导购写入失败")

# 虚拟导购
NOT_FIND_USER = HTTPException(400, detail="虚拟导购在有效时间范围内不存在提成记录或虚拟导购不存在")
NOT_CHANGE_USER = HTTPException(401, detail="导购和消费者为同一人时，不允许提成。")
SAVE_TAKE_AMOUNT_FAIL = HTTPException(402, detail="插入分账记录失败")
APP_TYPE_FAIL = HTTPException(403, detail="订单类型为代客下单,不允许提成.")

# 分会
NOT_FIND_COMMISSIN_USER = HTTPException(400, detail="查找不到提成导购手机")

