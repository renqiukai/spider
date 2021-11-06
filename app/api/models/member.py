from pydantic import BaseModel
from datetime import datetime


class rawMember(BaseModel):
    name: str = ""
    mobile: str
    discount: float
    parent_name: str
    parent_mobile: str
    parent_discount: float
    effective_time: datetime

    class Config:
        schema_extra = {
            "example":
            {
                "name": "任秋锴",
                "mobile": "13801587423",
                "discount": 0.7,
                "parent_name": "张三",
                "parent_mobile": "13801587424",
                "parent_discount": 0.95,
                "effective_time": "2020-07-25T05:47:41.927Z"
            }
        }
