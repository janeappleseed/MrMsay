#!/usr/bin/env python3

import logging

__all__ = [
    'logger',
    'enable_warning',
    'enable_debug',
]

logger = logging.getLogger('MrMsay')

def logger_init():
    formatter = logging.Formatter(
        fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%y-%m-%d %H:%M:%S',
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    logger_initialized = True

def enable_warning():
    logger.setLevel(logging.WARNING)

def enable_debug():
    logger.setLevel(logging.DEBUG)

logger_init()
