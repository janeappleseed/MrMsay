#!/usr/bin/env python3

import os
import random
import time

import peewee
import playhouse.migrate

from mrmsay import remote
from mrmsay.logger import logger
from mrmsay.paths import CACHE_DIR

__all__ = [
    'dump_comments',
    'dump_comments_smart',
    'insert_new_comments',
    'pick_random_comment',
]

DB_SCHEMA_VERSION = 2
DB_PATH = os.path.join(CACHE_DIR, 'comments.db')

# Blacklisted words, phrases or sentences
BLACKLIST = [
    'You rock!',
    'READ THIS: https://git.io/brew-troubleshooting',
]

# Avoid the following number of recently picked comments (so that MrM does not
# repeat himself too often)
NUM_RECENTLY_PICKED_TO_AVOID = 5

db = peewee.SqliteDatabase(DB_PATH)

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
    # Timestamp when the comment was last picked
    last_picked = peewee.IntegerField(default=0)

    class Meta(object):
        database = db

def db_schema_1_to_2():
    migrator = playhouse.migrate.SqliteMigrator(db)
    playhouse.migrate.migrate(migrator.add_column('comment', 'last_picked', Comment.last_picked))

def db_init():
    db.connect()
    try:
        db.create_table(Comment, safe=True)
    except peewee.OperationalError:
        pass

    schema_version = db.execute_sql('PRAGMA user_version;').fetchone()[0]
    if schema_version == 0:
        # New database
        schema_version = DB_SCHEMA_VERSION
        db.execute_sql('PRAGMA user_version = %s;' % schema_version)

    logger.info('Database schema version: %d', schema_version)
    if schema_version < DB_SCHEMA_VERSION:
        # Migrate schema
        migrators = [None, db_schema_1_to_2]
        for increment, migrator in enumerate(migrators[schema_version:]):
            current_version = schema_version + increment
            logger.info('Migrating from schema version %d to %d' %
                        (current_version, current_version + 1))
            migrator()
        db.execute_sql('PRAGMA user_version = %s;' % DB_SCHEMA_VERSION)

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

# Returns a dummy comment which is an object with the schema fields, a dummy
# save() method, and no more.
def dummy_comment():
    import datetime

    class DummyObject(object):
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return DummyObject(
        url='https://github.com/404',
        short_url='https://git.io/jedi',
        created_at=datetime.datetime.fromtimestamp(0),
        body='...',
        blacklisted=True,
        last_picked=0,
        save=lambda: None,
    )

# Smartly dump comments:
# - Avoid blacklisted comments;
# - Avoid recently picked comments;
# if possible.
#
# If there's no comment in the database, return a dummy comment. Therefore, the
# returned list is always nonempty.
def dump_comments_smart(limit=None):
    # First, try to avoid blacklisted and recently picked comments
    recently_picked_ids = [
        comment.id for comment in
        (Comment.select().order_by(Comment.last_picked.desc(), Comment.created_at)
         .limit(NUM_RECENTLY_PICKED_TO_AVOID))
    ]
    comments = (Comment.select()
                .where((Comment.blacklisted == False) &
                       (Comment.id.not_in(recently_picked_ids)))
                .order_by(Comment.created_at.desc()).limit(limit))
    if comments:
        return comments
    # Next, try to avoid blacklisted comments only
    comments = (Comment.select().where(Comment.blacklisted == False)
                .order_by(Comment.created_at.desc()).limit(limit))
    if comments:
        return comments
    # Next, return whatever comment is available
    comments = Comment.select().order_by(Comment.created_at.desc()).limit(limit)
    if comments:
        return comments
    # If everything fails, return a dummy comment
    logger.debug('No comments found, using dummy comment')
    return [dummy_comment()]

# limit is the maximum number of most recent comments to pick from (default: None)
# ensure_short_url determines whether to ensure the comment has a shortened url on file
def pick_random_comment(limit=None, ensure_short_url=True):
    comments = dump_comments_smart(limit=limit)
    comment = comments[random.randrange(len(comments))]
    if not comment.short_url and ensure_short_url:
        comment.short_url = remote.shorten_url(comment.url)
        comment.save()
    comment.last_picked = int(time.time())
    comment.save()
    return comment

db_init()
