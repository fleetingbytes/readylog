from logging import getLogger
from logging.config import dictConfig as configure_logging
from pathlib import Path

from logging_conf import create_dict_config


my_logging_configuration = create_dict_config(Path("."), "debug.log", "info.log", "error.log")
configure_logging(my_logging_configuration)

logger = getLogger(__name__)
# logger = getLogger("custom_logger")  # <-- This makes info log entries double and I don't know why


logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
try:
    42/0
except Exception as err:
    logger.exception(f"{err.args[0]} occurred")
logger.critical("critical error message")
