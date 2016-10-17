#!/usr/bin/env python3

import os

__all__ = [
    'CONFIG_DIR',
    'CACHE_DIR',
    'RUNTIME_DIR'
]

if os.getenv('XDG_CONFIG_HOME'):
    CONFIG_DIR = os.path.join(os.getenv('XDG_CONFIG_HOME'), 'mrmsay')
else:
    CONFIG_DIR = os.path.expanduser('~/.config/mrmsay')

if os.getenv('XDG_CACHE_HOME'):
    CACHE_DIR = os.path.join(os.getenv('XDG_CACHE_HOME'), 'mrmsay')
else:
    CACHE_DIR = os.path.expanduser('~/.cache/mrmsay')

if os.getenv('XDG_RUNTIME_DIR'):
    RUNTIME_DIR = os.path.join(os.getenv('XDG_RUNTIME_DIR'), 'mrmsay')
else:
    RUNTIME_DIR = '/tmp/mrmsay%d' % os.getuid()

os.makedirs(CACHE_DIR, mode=0o700, exist_ok=True)
os.makedirs(CONFIG_DIR, mode=0o700, exist_ok=True)
os.makedirs(RUNTIME_DIR, mode=0o700, exist_ok=True)
