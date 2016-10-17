#!/usr/bin/env python3

import logging
import os

__all__ = [
    'logger',
    'logger_init',
]

logger = logging.getLogger('MrMsay')

# logfile: if specified, log to the file; otherwise, log to stderr.
# Returns the file descriptor of the logfile (or that of stderr if
# logfile is unspecified).
def logger_init(logfile=None, level=logging.ERROR):
    formatter = logging.Formatter(
        fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%y-%m-%d %H:%M:%S',
    )
    if logfile:
        os.makedirs(os.path.dirname(logfile), exist_ok=True)
        handler = logging.FileHandler(logfile)
    else:
        handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(handler)
    return handler.stream.fileno()
