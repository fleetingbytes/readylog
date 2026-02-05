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

```python
from readylog import create_dict_confg

print create_dict_config.__doc__
```
