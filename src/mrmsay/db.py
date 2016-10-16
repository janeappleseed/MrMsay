#!/usr/bin/env python3

import os
import random

import peewee

from mrmsay.paths import CACHE_DIR
from mrmsay import remote

__all__ = [
    'dump_comments',
    'insert_new_comments',
    'pick_random_comment',
]

DB_SCHEMA_VERSION = 1
DB_PATH = os.path.join(CACHE_DIR, 'comments.db')

# Blacklisted words, phrases or sentences
BLACKLIST = [
    'You rock!',
    'READ THIS: https://git.io/brew-troubleshooting',
]

db = peewee.SqliteDatabase(DB_PATH, pragmas=[
    ('user_version', DB_SCHEMA_VERSION)
])

class Comment(peewee.Model):
    # Full comment URL
    url = peewee.TextField()
    # Shortened git.io URL (optional)
    short_url = peewee.TextField()
    # Comment creation date
    created_at = peewee.DateTimeField()
    # Full comment body
    body = peewee.TextField()
    # Blacklisted or not
    blacklisted = peewee.BooleanField()

    class Meta(object):
        database = db

def db_init():
    db.connect()
    db.create_table(Comment, safe=True)
    db_initialized = True

def insert_new_comments(comments):
    for comment in comments:
        Comment.create(
            url=comment['url'],
            short_url='',
            created_at=comment['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
            body=comment['body'],
            blacklisted=any([entry in comment['body'] for entry in BLACKLIST]),
        )

# limit is the maximum number of most recent comments to dump (default: None)
def dump_comments(limit=None):
    return Comment.select().order_by(Comment.created_at.desc()).limit(limit)

# limit is the maximum number of most recent comments to pick from (default: None)
# ensure_short_url determines whether to ensure the comment has a shortened url on file
# Blacklisted comments are excluded.
def pick_random_comment(limit=None, ensure_short_url=True):
    comments = (Comment
                .select().where(Comment.blacklisted == False)
                .order_by(Comment.created_at.desc()).limit(limit))
    comment = comments[random.randrange(len(comments))]
    if not comment.short_url and ensure_short_url:
        comment.short_url = remote.shorten_url(comment.url)
        comment.save()
    return comment

db_init()
