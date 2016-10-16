#!/usr/bin/env python3

import argparse
import sys

import sh

from mrmsay import (
    config,
    db,
    logger,
    remote,
)

def main():
    description = "MrM's wisdom, right in your terminal."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--auth', metavar='USER:TOKEN',
                        help="""GitHub credentials for higher API rate
                        limit (USER is your GitHub handle and TOKEN is a
                        personal access token); credentials are
                        automatically saved, so you only need to path
                        --auth once""")
    parser.add_argument('--debug', action='store_true',
                        help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.auth:
        try:
            user, token = args.auth.split(':')
        except ValueError:
            sys.stderr.write('[ERROR] Invalid --auth argument.\n')
            sys.exit(1)

        config.set_credentials(user, token)

    if args.debug:
        logger.enable_debug()

    print('Querying MrM...')
    remote.fetch_comments()
    comment = db.pick_random_comment(60)
    print(sh.cowsay(f='turkey', W='72', _in=comment.body))
    print(comment.short_url)

if __name__ == '__main__':
    main()
