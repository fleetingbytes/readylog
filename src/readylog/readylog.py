from __future__ import annotations

from logging import FileHandler, StreamHandler, _checkLevel, getLevelName
from pathlib import Path
from sys import modules
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

DEFAULT_CORE_LOG_FORMAT = "{levelname} {name}({lineno}), {funcName}: {message}"
DEFAULT_CONSOLE_LOG_FORMAT = DEFAULT_CORE_LOG_FORMAT
DEFAULT_FILE_LOG_FORMAT = "{} {}".format("{asctime}.{msecs:03.0f} ", DEFAULT_CORE_LOG_FORMAT)
DEFAULT_CONSOLE_LOG_TIME_FORMAT = "%H:%M:%S"
DEFAULT_FILE_LOG_TIME_FORMAT = DEFAULT_CONSOLE_LOG_TIME_FORMAT


def create_dict_config(
    logfile: Path | str,
    app_name: str,
    console_log_level: str | int = "WARNING",
    console_log_format: str = DEFAULT_CONSOLE_LOG_FORMAT,
    console_log_time_format: str = DEFAULT_CONSOLE_LOG_TIME_FORMAT,
    file_log_level: str | int = "DEBUG",
    file_log_format: str = DEFAULT_FILE_LOG_FORMAT,
    file_log_time_format: str = DEFAULT_CONSOLE_LOG_TIME_FORMAT,
    console_handler_factory: Callable = StreamHandler,
    file_handler_factory: Callable = FileHandler,
    additional_logger_names: tuple[str] = (),
    root_logger_level: str | int = "WARNING",
) -> dict[str, str]:
    logfile = Path(logfile)
    console_log_level = _checkLevel(console_log_level)
    file_log_level = _checkLevel(file_log_level)
    min_level = getLevelName(min(console_log_level, file_log_level))
    root_logger_level = getLevelName(_checkLevel(root_logger_level))

    custom_file_formatter_conf = {
        "format": file_log_format,
        "style": "{",
        "datefmt": DEFAULT_CONSOLE_LOG_TIME_FORMAT,
    }

    custom_console_formatter_conf = {
        "format": console_log_format,
        "style": "{",
        "datefmt": DEFAULT_FILE_LOG_TIME_FORMAT,
    }

    root_file_formatter_conf = {
        "format": f"[ROOT LOG] {custom_file_formatter_conf['format']}",
        "style": "{",
        "datefmt": "%a %H:%M:%S",
    }

    root_console_formatter_conf = {
        "format": f"[ROOT LOG] {custom_console_formatter_conf['format']}",
        "style": "{",
        "datefmt": "%a %H:%M:%S",
    }

    formatters_dict = {
        "custom_file_formatter": custom_file_formatter_conf,
        "custom_console_formatter": custom_console_formatter_conf,
        "root_file_formatter": root_file_formatter_conf,
        "root_console_formatter": root_console_formatter_conf,
    }

    custom_console_handler_conf = {
        "()": console_handler_factory,
        "level": console_log_level,
        "formatter": "custom_console_formatter",
        "stream": "ext://sys.stderr",
    }

    custom_file_handler_conf = {
        "()": file_handler_factory,
        "level": file_log_level,
        "formatter": "custom_file_formatter",
        "filename": logfile,
        "mode": "w",
        "encoding": "utf-8",
    }

    root_console_handler_conf = {
        "()": console_handler_factory,
        "level": "DEBUG",
        "formatter": "root_console_formatter",
        "stream": "ext://sys.stderr",
    }

    root_file_handler_conf = {
        "()": file_handler_factory,
        "level": "DEBUG",
        "formatter": "root_file_formatter",
        "filename": logfile.with_stem(f"{logfile.stem}_root"),
        "mode": "w",
        "encoding": "utf-8",
    }

    handlers_dict = {
        "custom_console_handler": custom_console_handler_conf,
        "custom_file_handler": custom_file_handler_conf,
        "root_console_handler": root_console_handler_conf,
        "root_file_handler": root_file_handler_conf,
    }

    custom_logger_conf = {
        "propagate": False,
        "handlers": ["custom_file_handler", "custom_console_handler"],
        "level": min_level,
    }

    root_logger_conf = {
        "handlers": ["root_file_handler", "root_console_handler"],
        "level": root_logger_level,
    }

    loggers_dict = {
        app_name: custom_logger_conf,
        "__main__": custom_logger_conf,
        f"{modules[__name__].__spec__.parent}.decorators": custom_logger_conf,
    }
    loggers_dict.update({logger_name: custom_logger_conf for logger_name in additional_logger_names})

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
