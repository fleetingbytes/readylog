from logging import getLogger
from logging.config import dictConfig as configure_logging

from .logging_conf import logging_configuration


configure_logging(logging_configuration)

logger = getLogger(__name__)


logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
try:
    42/0
except Exception as err:
    logger.exception(f"{err.args[0]} occurred")
logger.critical("critical error message")
