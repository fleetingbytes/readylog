from collections.abc import Callable
from logging import DEBUG
from logging.config import dictConfig as configure_logging
from pathlib import Path

from pytest import CaptureFixture, mark, param

from readylog import create_dict_config
from readylog.decorators import (
    critical,
    critical_in,
    critical_out,
    debug,
    debug_in,
    debug_out,
    error,
    error_in,
    error_out,
    info,
    info_in,
    info_out,
    warning,
    warning_in,
    warning_out,
)

decorators = {
    "debug": debug,
    "debug_in": debug_in,
    "debug_out": debug_out,
    "info": info,
    "info_in": info_in,
    "info_out": info_out,
    "warning": warning,
    "warning_in": warning_in,
    "warning_out": warning_out,
    "error": error,
    "error_in": error_in,
    "error_out": error_out,
    "critical": critical,
    "critical_in": critical_in,
    "critical_out": critical_out,
}


@mark.parametrize(
    "decorated_function, expect_function_entry_logged, expect_function_return_logged",
    (
        *(
            param(
                decorator,
                not decorator_name.endswith("_out"),
                not decorator_name.endswith("_in"),
                id=decorator_name,
            )
            for decorator_name, decorator in decorators.items()
        ),
    ),
    indirect=["decorated_function"],
)
def test_decorators(
    tmp_log_file: Path,
    app_name: str,
    decorated_function: Callable,
    expect_function_entry_logged: bool,
    expect_function_return_logged: bool,
    capsys: CaptureFixture,
) -> None:
    name_of_the_module_where_the_inner_decorated_function_lives = "tests.conftest"
    logger_of_the_inner_decorated_function = name_of_the_module_where_the_inner_decorated_function_lives

    config = create_dict_config(
        tmp_log_file,
        app_name,
        console_log_level=DEBUG,
        additional_logger_names=(logger_of_the_inner_decorated_function,),
    )
    configure_logging(config)

    decorated_function("some_arg", some_kwarg="some_value")

    captured = capsys.readouterr()
    lines = captured.err.strip()

    if expect_function_entry_logged:
        assert "Calling function_under_test" in lines
        if not expect_function_return_logged:
            assert "function_under_test returned" not in lines

    if expect_function_return_logged:
        assert "function_under_test returned" in lines
        if not expect_function_entry_logged:
            assert "Calling function_under_test" not in lines
