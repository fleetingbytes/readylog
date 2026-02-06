# readylog

Readylog is a logging configuration template for Python's logging.

## Usage

Basic example:

```python
# my_app.py

from logging.config import dictConfig as configure_logging
from logging import getLogger
from pathlib import Path

from platformdirs import user_log_dir
from readylog import create_dict_config


def setup_logging() -> None:
    app_name = "my_app"
    author = "Me"

    log_dir = Path(user_log_dir(app_name, author))
    log_dir.mkdir(parents=True, exist_ok=True)

    logging_config = create_dict_config(log_dir / "debug.log", app_name)
    configure_logging(logging_config)


logger = getLogger(__name__)
setup_logging()

logger.debug("This should be logged")
```

## Documentation

### readylog's public objects

```python
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
```

### Arguments:

- *logfile:* name of the log file where to save the logs
- *app_name:* name of your app (will be used as a logger name)

### Keyword Arguments:
- *console_log_level:* minimum log level for the console log
- *console_log_format:* console log line format in "{" style
- *file_log_level:* minimum log level for the file log
- *file_log_format:* file log line format in "{" style
- *console_handler_factory:* the factory for the stream handler
- *file_handler_factory:* the factory for the file handler
- *additional_logger_names:* here you can put all the other logger names which you want to include in your log. Use this when you have projects with uv workspaces and want to see logs from workspace members rather than just from you main app.
- *root_logger_lever:* minimum level to display in you root log

### Root Log file

Root log will be output to console and to a file.
The path and name of the root log file is derived from the
logfile path, but the file name stem has a "_root" suffix.

For example if logfile path is `/home/my_user/my_app/debug.log`,
then the root log will be in `/home/my_user/my_app/debug_root.log`.
