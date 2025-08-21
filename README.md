# logging_conf
Logging_conf is a logging configuration template for Python's logging.

## Files
This repository contains two files, of which you actually only need the `logging_conf.py`.
The other is just an example code to showcase the usage of the configuration.

### `logging_conf.py`
Copy this into your project folder and import the `create_dict_config` function from it in your app's entrypoint.

Usage Example:
```py
from logging import getLogger
from logging.config import dictConfig as configure_logging

from .logging_conf import logging_configuration


configure_logging(logging_configuration)

logger = getLogger(__name__)
```

and you are ready to go.

