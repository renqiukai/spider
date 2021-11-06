'''
@author: renqiukai
@Date: 2020-06-05 11:45:23
@Description: cjdg tools api main
@LastEditTime: 2020-06-12 20:52:50
'''
import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.api.routes.api import router as api_router
from app.core.config import (ALLOWED_HOSTS, API_PREFIX, DEBUG, PROJECT_NAME,
                             VERSION, OPENAPI_PREFIX)
from app.core.logging import logger
from fastapi.responses import JSONResponse


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG,
                          version=VERSION, openapi_url="/openapi.json",
                          openapi_prefix=OPENAPI_PREFIX,
                          )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # application.add_event_handler("startup", create_start_app_handler(application))
    # application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    with open("doc/main.md", encoding="utf8") as f:
        s = f.read()
    application.description = s
    application.include_router(api_router, prefix=API_PREFIX)
    application.mount(
        "/static", StaticFiles(directory="static"), name="static")
    return application


app = get_application()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["API-Process-Time"] = str(process_time)
    return response