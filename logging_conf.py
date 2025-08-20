"""
This is to easily set the loging like this:

    from logging import getLogger
    from logging.config import dictConfig as configure_logging
    from pathlib import Path

    from logging_conf import create_dict_config


    my_logging_configuration = create_dict_config(Path("."), "debug.log", "info.log", "error.log")
    configure_logging(my_logging_configuration)

    logger = getLogger(__name__)

If you want an additional custom logger, get it like this:

    logger = getLogger("custom_logger")

The custom logger is configured to propagate its log records to the root logger
"""


from pathlib import Path


def create_dict_config(directory: Path, all_log: str, info_log: str, error_log: str) -> dict:
    """
    Creates a logging configuration with path to logfiles set as
    given by the arguments
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)

    file_formatter_conf = {
        "format": "{message:<50s} {levelname:>9s} {asctime}.{msecs:03.0f} {module} {funcName} ",
        "style": "{",
        # "datefmt": "%Y-%m-%d %H:%M:%S",
        "datefmt": "%H:%M:%S",
    }

    console_formatter_conf = {
        "format": "{message:<50s} {levelname:>9s} {module} {funcName}",
        # "format": "{asctime},{msecs:03.0f} {levelname:>9s} {module} {funcName}: {message}",
        "style": "{",
        "datefmt": "%a %H:%M:%S",
    }

    formatters_dict = {
        "file_formatter": file_formatter_conf,
        "console_formatter": console_formatter_conf,
    }

    root_console_handler_conf = {
        "class": "logging.StreamHandler",
        "level": "DEBUG",
        "formatter": "console_formatter",
        "stream": "ext://sys.stdout",
    }

    root_file_handler_conf = {
        "class": "logging.FileHandler",
        "level": "DEBUG",
        "formatter": "file_formatter",
        "filename": directory / all_log,
        "mode": "w",
        "encoding": "utf-8",
    }

    custom_error_file_handler_conf = {
        "class": "logging.FileHandler",
        "level": "ERROR",
        "formatter": "file_formatter",
        "filename": directory / error_log,
        "mode": "w",
        "encoding": "utf-8",
    }

    custom_info_file_handler_conf = {
        "class": "logging.FileHandler",
        "level": "INFO",
        "formatter": "file_formatter",
        "filename": directory / info_log,
        "mode": "w",
        "encoding": "utf-8",
    }

    handlers_dict = {
        "root_console_handler": root_console_handler_conf,
        "root_file_handler": root_file_handler_conf,
        "custom_error_file_handler": custom_error_file_handler_conf,
        "custom_info_file_handler": custom_info_file_handler_conf,
    }

    custom_logger_conf = {
        "propagate": True,
        "handlers": ["custom_error_file_handler", "custom_info_file_handler"],
        "level": "DEBUG",
    }

    root_logger_conf = {
        "handlers": ["root_file_handler", "root_console_handler", "custom_error_file_handler", "custom_info_file_handler"],
        "level": "DEBUG",
    }

    loggers_dict = {
        "custom_logger": custom_logger_conf,
    }

    dict_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": formatters_dict,
        "handlers": handlers_dict,
        "loggers": loggers_dict,
        "root": root_logger_conf,
        "incremental": False,
    }
    return dict_config

