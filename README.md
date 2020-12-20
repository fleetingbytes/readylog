# logging_conf
Logging_conf is a ready-to-use configuration dictionary for python's logger.

## Files
This repository contains two files, of which you actually only need one. The other is just an example code to show how the configuration module is used in actual code.

### logging_conf.py
This is the actual module you should copy into your project folder and import it in your code's modules. Its main purpose is to give you the configuration dictionary `dict_config` with which you can configure all your logging in just few line of code:

> Import python's standard logging and its configuration module
```
import logging
import logging.config
```

> Import my module with a ready-to-use logging configuration
```
import logging_conf
```

> Let the logger use the configuration preset in my module
```
logging.config.dictConfig(logging_conf.create_dict_config(pathlib.Path("."), "debug.log", "info.log", "error.log"))
```

> Get the root logger
```
logger = logging.getLogger(__name__)
```

and you are ready to go.

### logging_test.py
This is an example code file with which you can test the logger configuration. It outputs one line of each error level and shows an exception treatment generating the corresponding log output.

## What is the configuration
The `root` logger is configured to ouptut records into a log file and also into the console. It outputs everything from error level `DEBUG` to `CRITICAL`.

There is some infrastructure ready for a custom logger, but I never really use it, so feel free to experiment with it, if you want

> Get the custom logger
```
logger = logging.getLogger("custom_logger")
```
