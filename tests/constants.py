from logging import getLevelNamesMapping

IGNORED_LEVEL = "NOTSET"

USABLE_LEVELS = {k: v for k, v in getLevelNamesMapping().items() if k != IGNORED_LEVEL}
USABLE_LEVEL_NAMES = tuple(key for key in USABLE_LEVELS)
