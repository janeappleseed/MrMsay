#!/usr/bin/env python3

import os

__all__ = [
    'CONFIG_DIR',
    'CACHE_DIR',
]

if os.getenv('XDG_CONFIG_HOME'):
    CONFIG_DIR = os.path.join(os.getenv('XDG_CONFIG_HOME'), 'mrmsay')
else:
    CONFIG_DIR = os.path.expanduser('~/.config/mrmsay')

if os.getenv('XDG_CACHE_HOME'):
    CACHE_DIR = os.path.join(os.getenv('XDG_CACHE_HOME'), 'mrmsay')
else:
    CACHE_DIR = os.path.expanduser('~/.cache/mrmsay')

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)
