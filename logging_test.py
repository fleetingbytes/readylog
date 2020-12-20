import logging
import logging.config
import logging_conf
import pathlib

logging.config.dictConfig(logging_conf.create_dict_config(pathlib.Path("."), "debug.log", "info.log", "error.log"))
logger = logging.getLogger()
# logger = logging.getLogger("custom_logger") <-- This makes info log entries double and I don't know why

logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
try:
    42/0
except Exception as err:
    logger.exception(f"{err.args[0]} occurred")
logger.critical("critical error message")
