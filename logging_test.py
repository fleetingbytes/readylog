import logging
import logging.config
import logging_conf
import pathlib

logging_conf.set_logfile_path(pathlib.Path("my_favourite_logfile_name.txt"))
logging.config.dictConfig(logging_conf.dict_config)
# logger = logging.getLogger()
logger = logging.getLogger("custom_logger")

logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
try:
    42/0
except Exception as err:
    logger.exception(f"{err.args[0]} occurred")
logger.critical("critical error message")
