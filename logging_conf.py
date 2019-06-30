# Logger Configuration module
# Import this for easy logger configuration
# See example in the comment of the set_logfile_path function below

# Author: Sven Siegmund
# Version 1

file_formatter_conf = {
    "format": "{asctime},{msecs:03.0f} {levelname:>9s} {module} {funcName}: {message}",
    "style": "{",
    "datefmt": "%Y-%m-%d %H:%M:%S",
}

console_formatter_conf = {
    "format": "{asctime}.{msecs:03.0f} {levelname:>9s} {module} {funcName}: {message}",
    "style": "{",
    "datefmt": "%a %H:%M:%S",
}

formatters_dict = {
    "file_formatter": file_formatter_conf,
    "console_formatter": console_formatter_conf,
}

console_handler_conf = {
    "class": "logging.StreamHandler",
    "level": "DEBUG",
    "formatter": "console_formatter",
    "stream": "ext://sys.stdout",
}

file_handler_conf = {
    "class": "logging.FileHandler",
    "level": "DEBUG",
    "formatter": "file_formatter",
    "filename": "logfile.txt",
    "mode": "w",
    "encoding": "utf-8",
}

handlers_dict = {
    "console_handler": console_handler_conf,
    "file_handler": file_handler_conf,
}

console_logger_conf = {
    "propagate": True,
    "handlers": ["console_handler"],
    "level": "DEBUG",
}

file_logger_conf = {
    "handlers": ["file_handler"],
    "level": "DEBUG",
}

loggers_dict = {
    "console_logger": console_logger_conf
}

dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": formatters_dict,
    "handlers": handlers_dict,
    "loggers": loggers_dict,
    "root": file_logger_conf,
    "incremental": False,
}

def set_logfile_path(log_file_path: str) -> None:
    """
    This is to easily set the logfile name from the module where logging_conf
    is imported. Like this:

    import logging_conf
    
    logging_conf.set_logfile_path("custom_logfile_name.txt")
    logging.config.dictConfig(logging_conf.dict_config)
    # use this if you only need the root logger which only logs into a file of the chosen name:
    # logging.getLogger()
    # use this instead if you also want an additional console logger:
    # logger = logging.getLogger("console_logger")
    """
    global dict_config
    dict_config["handlers"]["file_handler"]["filename"] = log_file_path