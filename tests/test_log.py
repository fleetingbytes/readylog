from logging import Logger
from logging import getLogger as get_logger
from logging.config import dictConfig as configure_logging
from pathlib import Path

from pytest import CaptureFixture, mark, param
from watchdog.observers import Observer

from readylog import create_dict_config
from tests.constants import USABLE_LEVEL_NAMES, USABLE_LEVELS


def produce_log_messages_on_all_levels(logger: Logger) -> None:
    for level_name, level in USABLE_LEVELS.items():
        message = f"this is a {level_name.lower()} message"
        logger.log(level, message)


def expected_number_of_log_lines(limit: int) -> int:
    number_of_levels_at_or_above_limit = len(tuple(filter(lambda n: n >= limit, USABLE_LEVELS.values())))
    return number_of_levels_at_or_above_limit


@mark.parametrize("log_level", USABLE_LEVEL_NAMES, ids=str.lower)
def test_console_log(tmp_log_file: Path, app_name: str, log_level, capsys: CaptureFixture):
    config = create_dict_config(tmp_log_file, app_name, console_log_level=log_level)
    configure_logging(config)
    logger = get_logger(app_name)

    produce_log_messages_on_all_levels(logger)

    captured = capsys.readouterr()
    lines = captured.err.strip().split("\n")
    number_of_lines = len(lines)

    limit = USABLE_LEVELS[log_level]
    assert number_of_lines == expected_number_of_log_lines(limit)


@mark.parametrize(
    "log_file_observer, log_level_name",
    (
        *(
            param(expected_number_of_log_lines(level), level_name, id=level_name.lower())
            for level_name, level in USABLE_LEVELS.items()
        ),
    ),
    indirect=["log_file_observer"],
)
def test_file_log(tmp_log_file: Path, app_name: str, log_file_observer: Observer, log_level_name):
    config = create_dict_config(tmp_log_file, app_name, file_log_level=log_level_name)
    configure_logging(config)
    logger = get_logger(app_name)

    produce_log_messages_on_all_levels(logger)
