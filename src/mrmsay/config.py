#!/usr/bin/env python3

import json
import os

from mrmsay.paths import CONFIG_DIR

CREDENTIALS_PATH = os.path.join(CONFIG_DIR, 'auth.json')

def get_credentials():
    if os.path.isfile(CREDENTIALS_PATH):
        with open(CREDENTIALS_PATH) as fp:
            try:
                credentials = json.load(fp)
                return credentials['user'], credentials['token']
            except (json.JSONDecodeError, KeyError):
                pass
    return None, None

def set_credentials(user, token):
    with open(CREDENTIALS_PATH, 'w') as fp:
        json.dump({
            'user': user,
            'token': token,
        }, fp, indent=4)
