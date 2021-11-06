'''
@author: renqiukai
@Date: 2020-06-17 01:22:21
@Description: db conf
@LastEditTime: 2020-06-17 01:31:56
'''
from app.core.config import DB
from app.core.logging import logger
# 外网正式
db_connect = {
    "prod": {
        "host": "sh-cdb-ie4c3glo.sql.tencentcdb.com",
        "user": "root",
        "password": "Sw-Cjdg-EK-I10!",
        "port": 62056,
        "db": "xtep_club",
        "charset": "utf8",
    },

    "test": {
        "host": "sh-cdb-ie4c3glo.sql.tencentcdb.com",
        "user": "root",
        "password": "Sw-Cjdg-EK-I10!",
        "port": 62056,
        "db": "xtep_club_test",
        "charset": "utf8",
    },

    # 内网正式
    "prod_inner": {
        "host": "172.17.16.36",
        "user": "root",
        "password": "Sw-Cjdg-EK-I10!",
        "port": 3306,
        "db": "xtep_club",
        "charset": "utf8",
    },
    "test_inner": {
        "host": "172.17.16.36",
        "user": "root",
        "password": "Sw-Cjdg-EK-I10!",
        "port": 3306,
        "db": "xtep_club_test",
        "charset": "utf8",
    }
}

try:
    default = db_connect[DB]
except KeyError:
    default = db_connect["test"]
    logger.error({"error": f"环境变量DB取得的值为：{DB}，采用test环境。"})