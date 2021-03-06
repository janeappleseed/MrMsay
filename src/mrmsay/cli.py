#!/usr/bin/env python3

import argparse
import logging
import sys

from mrmsay import (
    config,
    logger,
    say,
)
from mrmsay.__version__ import __version__

# Maximum number of recent comments to pick a random one from
NUM_RECENT_COMMENTS_TO_PICK_FROM = 300

def main():
    description = "MrM's wisdom, right in your terminal."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--auth', metavar='USER:TOKEN',
                        help="""GitHub credentials for higher API rate
                        limit (USER is your GitHub handle and TOKEN is a
                        personal access token); credentials are
                        automatically saved, so you only need to path
                        --auth once""")
    parser.add_argument('--offline', action='store_true',
                        help="""do not attempt to fetch new comments; by
                        default the program fetches new comments if it
                        hasn't done so in the last ten minutes""")
    parser.add_argument('-v', '--version', action='version',
                        version='MrMsay %s' % __version__)
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

    logger.logger_init(level=logging.DEBUG if args.debug else logging.ERROR)

    try:
        # Delay several internal imports so that --debug could take effect
        from mrmsay import (
            db,
            remote,
        )

        print('Querying MrM...')

        if not args.offline:
            remote.fetch_comments()

        comment = db.pick_random_comment(NUM_RECENT_COMMENTS_TO_PICK_FROM,
                                         ensure_short_url=not args.offline)
        print(say.say(comment.body))
        print(comment.short_url)
    except KeyboardInterrupt:
        sys.stderr.write('Interrupted.\n')
        sys.exit(1)
    except Exception as e:
        if not args.debug:
            sys.stderr.write('[ERROR] Got %s: %s\n' % (type(e).__name__, e))
        else:
            raise

if __name__ == '__main__':
    main()
