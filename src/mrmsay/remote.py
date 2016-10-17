#!/usr/bin/env python3

import base64
import json
import os
import time

import arrow
import requests

from mrmsay import (
    config,
    db,
)
from mrmsay.logger import logger
from mrmsay.paths import CACHE_DIR

__all__ = [
    'fetch_comments',
    'shorten_url',
]

GITHUB_USER = base64.b64decode('TWlrZU1jUXVhaWQ=').decode('utf-8')
API_ENDPOINT = 'https://api.github.com/users/%s/events' % GITHUB_USER
API_HEADERS = {'Accept': 'application/vnd.github.v3+json'}
MAX_NUM_EVENTS = 300 # API limit
MAX_NUM_PAGES = 10 # API limit
UPDATE_TIMESTAMP_FILE = os.path.join(CACHE_DIR, 'update_timestamp')

def outdated():
    last_update = 0
    if os.path.isfile(UPDATE_TIMESTAMP_FILE):
        with open(UPDATE_TIMESTAMP_FILE) as fp:
            try:
                last_update = int(fp.read())
            except ValueError:
                pass
    return time.time() >= last_update + 600 # Ten minutes since the last update

def write_timestamp():
    with open(UPDATE_TIMESTAMP_FILE, 'w') as fp:
        fp.write(str(int(time.time())))

def fetch_comments():
    if not outdated():
        logger.debug('Not outdated, skip fetching')
        return

    session = requests.Session()
    session.headers.update(API_HEADERS)

    auth_user, auth_token = config.get_credentials()
    if auth_user and auth_token:
        session.auth = (auth_user, auth_token)

    url = API_ENDPOINT
    page = 0
    while url and page < MAX_NUM_PAGES:
        logger.debug('Fetching %s', url)
        try:
            response = session.get(url)
        except Exception as e:
            logger.debug('Got %s: %s', type(e).__name__, e)
            break

        code = response.status_code
        if code != 200:
            try:
                reason = response.json()['message']
            except (json.JSONDecodeError, KeyError):
                reason = ''
            logger.debug('Got HTTP %d: %s' % (code, reason))
            break

        if page == 0:
            write_timestamp()

        comments = []
        for event in response.json():
            if 'payload' not in event:
                continue
            payload = event['payload']
            if 'comment' not in payload:
                continue
            comment = payload['comment']
            if comment['user']['login'] != GITHUB_USER:
                continue
            comment_url = comment['html_url']
            comment_created_at = arrow.get(comment['created_at'])
            comment_body = comment['body']
            comments.append({
                'url': comment_url,
                'created_at': comment_created_at,
                'body': comment_body,
            })

        if not db.insert_comments(comments):
            # We're getting old comments already, stop fetching
            break

        try:
            url = response.links['next']['url']
        except (AttributeError, KeyError):
            break

        page += 1

def shorten_url(url):
    logger.debug('git.io %s', url)
    try:
        response = requests.post('https://git.io', data={'url': url})
    except Exception as e:
        logger.debug('Got %s: %s', type(e).__name__, e)
        return ''

    if response.status_code == 201:
        try:
            short_url = response.headers['Location']
            logger.debug('Shortened %s as %s', url, short_url)
            return short_url
        except KeyError:
            pass
    logger.debug('Failed to shorten %s', url)
    return ''
