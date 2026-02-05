from __future__ import annotations

from logging import FileHandler, StreamHandler, _checkLevel, getLevelName
from pathlib import Path
from sys import modules
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

DEFAULT_CORE_LOG_FORMAT = "{levelname} {name} {message} {module}({lineno}) {funcName}"
DEFAULT_CONSOLE_LOG_FORMAT = DEFAULT_CORE_LOG_FORMAT
DEFAULT_FILE_LOG_FORMAT = "{} {}".format("{asctime}.{msecs:03.0f} ", DEFAULT_CORE_LOG_FORMAT)


def create_dict_config(
    logfile: Path | str,
    app_name: str,
    console_log_level: str | int = "WARNING",
    console_log_format: str = DEFAULT_CONSOLE_LOG_FORMAT,
    file_log_level: str | int = "DEBUG",
    file_log_format: str = DEFAULT_FILE_LOG_FORMAT,
    console_handler_factory: Callable = StreamHandler,
    file_handler_factory: Callable = FileHandler,
    additional_logger_names: tuple[str] = (),
    root_logger_level: str | int = "WARNING",
) -> dict[str, str]:
    """
    create_dict_config(
    logfile: Path | str,
    app_name: str,
    console_log_level: str | int = "WARNING",
    console_log_format: str = DEFAULT_CONSOLE_LOG_FORMAT,
    file_log_level: str | int = "DEBUG",
    file_log_format: str = DEFAULT_FILE_LOG_FORMAT,
    console_handler_factory: Callable = StreamHandler,
    file_handler_factory: Callable = FileHandler,
    additional_logger_names: tuple[str] = (),
    root_logger_level: str | int = "WARNING",
    )

    Arguments:
        logfile: name of the log file where to save the logs
        app_name: name of your app (will be used as a logger name)

    Keyword Arguments:
        console_log_level: minimum log level for the console log
        console_log_format: console log line format in "{" style
        file_log_level: minimum log level for the file log
        file_log_format: file log line format in "{" style
        console_handler_factory: the factory for the stream handler
        file_handler_factory: the factory for the file handler
        additional_logger_names: here you can put all the other logger names
            which you want to include in your log. Use this
            when you have projects with uv workspaces and want to
            see logs from workspace members rather than just from
            you main app.
        root_logger_lever: minimum level to display in you root log

    root log will be output to console and to a file.
    The path and name of the root log file is derived from the
    logfile path, but the file name stem has a "_root" suffix.

    For example if logfile path is `/home/my_user/my_app/debug.log`,
    then the root log will be in `/home/my_user/my_app/debug_root.log`.
    """
    logfile = Path(logfile)
    console_log_level = _checkLevel(console_log_level)
    file_log_level = _checkLevel(file_log_level)
    min_level = getLevelName(min(console_log_level, file_log_level))
    root_logger_level = getLevelName(_checkLevel(root_logger_level))

    custom_file_formatter_conf = {
        "format": file_log_format,
        "style": "{",
        "datefmt": "%a %H:%M:%S",
    }

    custom_console_formatter_conf = {
        "format": console_log_format,
        "style": "{",
        "datefmt": "%a %H:%M:%S",
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
