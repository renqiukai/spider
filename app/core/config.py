'''
@author: renqiukai
@Date: 2020-06-05 11:45:23
@Description: env settings.
@LastEditTime: 2020-06-17 01:26:12
'''
import os

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS")
DB = os.getenv("DB") or "test"
API_PREFIX = os.getenv("API_PREFIX") or "/api"
DEBUG = os.getenv("DEBUG") or True
PROJECT_NAME = os.getenv("PROJECT_NAME", "测试")
VERSION = os.getenv("VERSION") or "1.0.0"
TOKEN = os.getenv("TOKEN") or "ad899664-44d0-4b56-b1c0-739c7ce946ac"
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv(
    "ACCESS_TOKEN_EXPIRE_MINUTES") or 10080
SECRET_KEY = os.getenv("SECRET_KEY") or "renqiukai"
APPID = os.getenv("APPID") or "xrc"
OPENAPI_PREFIX = os.getenv("OPENAPI_PREFIX") or ""
# OPENAPI_PREFIX =  "ft"
