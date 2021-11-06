import logging
from loguru import logger
from app.core.config import PROJECT_NAME


logger.add(f"/home/log/{PROJECT_NAME}-{{time}}.log",
           encoding="utf8", rotation='00:00')

class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        logger_opt = logger.opt(depth=7, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())
