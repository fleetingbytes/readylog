#!/usr/bin/env -S uv run --quiet --script
#
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "readylog",
# ]
#
# [tool.uv.sources]
# readylog = { path = "..", editable = true }
# ///

from logging import getLogger
from logging.config import dictConfig

from readylog import create_dict_config
from readylog.decorators import debug

logging_configuration = create_dict_config(
    "e2e-test-logfile.log", "e2e-test-app", console_log_level="DEBUG"
)
dictConfig(logging_configuration)

logger = getLogger(__name__)


@debug
def greet(greeting: str, name: str) -> None:
    return f"{greeting.title()}, {name.title()}"


logger.debug("e2e-test-app runs")

greet("hello", "world")
