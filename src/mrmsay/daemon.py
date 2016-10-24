#!/usr/bin/env python3

import argparse
import logging
import os
import time

import daemonize

from mrmsay import logger
from mrmsay.__version__ import __version__
from mrmsay.paths import CACHE_DIR, RUNTIME_DIR

LOGFILE = os.path.join(CACHE_DIR, 'mrmd.log')
PIDFILE = os.path.join(RUNTIME_DIR, 'mrmd.pid')

def fetch_loop():
    from mrmsay import remote
    while True:
        remote.fetch_comments(force=True)
        time.sleep(600)

def main():
    description = "Collect Mrm's wisdom nonstop."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-v', '--version', action='version',
                        version='MrMsay %s' % __version__)
    parser.parse_args()

    fd = logger.logger_init(logfile=LOGFILE, level=logging.DEBUG)
    daemonize.Daemonize(
        app='mrmd',
        pid=PIDFILE,
        action=fetch_loop,
        keep_fds=[fd],
        logger=logger.logger,
    ).start()

if __name__ == '__main__':
    main()
