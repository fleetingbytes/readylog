"""
This is to easily set the logfile name for the root logger's
file handler from the module where logging_conf
is imported. Like this:

    from logging import getLogger
    from logging.config import dictConfig as configure_logging
    from platformdirs import user_log_dir

    from ..logging_conf import create_dict_config


    my_app_name = "<YOUR_APP_NAME_HERE>"
    logging_dir = Path(user_log_dir(my_app_name))
    logger_configuration = create_dict_config(logging_dir, "debug.log")
    configure_logging(logger_configuration)

    logger = getLogger(__name__)


If you want an additional custom logger, get it like this:

    logger = logging.getLogger("custom_logger")

The custom logger is configured to propagate its log records to the root logger
"""


from pathlib import Path


def create_dict_config(directory: Path, logfile_name: str) -> dict:
    """
    Creates a logging configuration with path to logfiles set as
    given by the arguments
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    logfile = directory / logfile_name

    custom_file_formatter_conf = {
        "format": "{message:<50s} {levelname:>9s} {asctime}.{msecs:03.0f} {module}({lineno}) {funcName}",
        "style": "{",
        "datefmt": "%a %H:%M:%S",
    }

    custom_console_formatter_conf = {
        "format": "{message:<50s} {levelname:>9s} {module}({lineno}) {funcName}",
        "style": "{",
        "datefmt": "%a %H:%M:%S",
    }

    root_file_formatter_conf = {
        "format": f"[ROOT LOG] {custom_file_formatter_conf["format"]},
        "style": "{",
        "datefmt": "%a %H:%M:%S",
    }

    root_console_formatter_conf = {
        "format": f"[ROOT LOG] {custom_console_formatter_conf["format"]},
        "style": "{",
        "datefmt": "%a %H:%M:%S",
    }

    formatters_dict = {
        "root_file_formatter": root_file_formatter_conf,
        "root_console_formatter": root_console_formatter_conf,
        "custom_file_formatter": custom_file_formatter_conf,
        "custom_console_formatter": custom_console_formatter_conf,
    }

    root_console_handler_conf = {
        "class": "logging.StreamHandler",
        "level": "DEBUG",
        "formatter": "root_console_formatter",
        "stream": "ext://sys.stderr",
    }

    root_file_handler_conf = {
        "class": "logging.FileHandler",
        "level": "DEBUG",
        "formatter": "root_file_formatter",
        "filename": logfile.with_stem(f"{logfile.stem}_root"),
        "mode": "w",
        "encoding": "utf-8",
    }

    custom_console_handler_conf = {
        "class": "logging.StreamHandler",
        "level": "DEBUG",
        "formatter": "custom_console_formatter",
        "stream": "ext://sys.stderr",
    }

    custom_file_handler_conf = {
        "class": "logging.FileHandler",
        "level": "DEBUG",
        "formatter": "custom_file_formatter",
        "filename": logfile,
        "mode": "w",
        "encoding": "utf-8",
    }

    handlers_dict = {
        "root_console_handler": root_console_handler_conf,
        "root_file_handler": root_file_handler_conf,
        "custom_console_handler": custom_console_handler_conf,
        "custom_file_handler": custom_file_handler_conf,
    }

    custom_logger_conf = {
        "propagate": False,
        "handlers": ["custom_file_handler", "custom_console_handler"],
        "level": "DEBUG",
    }

    root_logger_conf = {
        "handlers": ["root_file_handler", "root_console_handler"],
        "level": "WARNING",
    }

    loggers_dict = {
        "<YOUR_APP_NAME_HERE>": custom_logger_conf,
        "<YOUR_LIBRARY_NAME_HERE>": custom_logger_conf,
        "__main__": custom_logger_conf,
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

