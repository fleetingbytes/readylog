from pytest import mark, param, raises

from readylog import create_dict_config


def test_config_creation(tmp_log_file, app_name):
    _ = create_dict_config(tmp_log_file, app_name)


@mark.parametrize(
    "kwargs",
    (
        param({"console_log_level": "TRACE"}, id="console"),
        param({"file_log_level": "TRACE"}, id="file"),
        param({"console_log_level": "TRACE", "file_log_level": "IMPORTANT"}, id="console, file"),
    ),
)
def test_config_creation_with_wrong_level(tmp_log_file, app_name, kwargs):
    with raises(AssertionError):
        _ = create_dict_config(tmp_log_file, app_name, **kwargs)


@mark.parametrize(
    "kwargs, expected",
    (
        param({"console_log_level": "DEBUG", "file_log_level": "INFO"}, "DEBUG", id="debug, info"),
        param({"console_log_level": "INFO", "file_log_level": "DEBUG"}, "DEBUG", id="info, debug"),
    ),
)
def test_logger_level(tmp_log_file, app_name, kwargs, expected):
    d = create_dict_config(tmp_log_file, app_name, **kwargs)
    actual = d["loggers"][app_name]["level"]
    assert actual == expected
