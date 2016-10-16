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

    try:
        print('Querying MrM...')
        remote.fetch_comments()
        comment = db.pick_random_comment(60)
        try:
            print(sh.cowsay(f='turkey', W='72', _in=comment.body))
        except sh.ErrorReturnCode:
            # There's bug in older versions of Perl, e.g. system Perl (5.18.2) on
            # macOS 10.12 which could lead to cowsay spitting an error like
            #
            #     This shouldn't happen at /System/Library/Perl/5.18/Text/Wrap.pm
            #     line 84, <STDIN> line 1.
            #
            # in certain cases. The bug is in Text::Wrap 2012.0818 and was fixed in
            # 2013.0523. See http://www.perlmonks.org/?node_id=1070469#1070721.
            print(sh.cowsay(f='turkey', W='72', _in='...'))
        print(comment.short_url)
    except KeyboardInterrupt:
        sys.stderr.write('Interrupted.\n')
        sys.exit(1)
    except Exception as e:
        if not args.debug:
            sys.stderr.write('[ERROR] Got %s: %s\n' % (type(e).__name__, e))

if __name__ == '__main__':
    main()
