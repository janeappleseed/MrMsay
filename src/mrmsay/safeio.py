#!/usr/bin/env python3

"""Safe file I/O with flock(2) locking."""

import fcntl
import os

# Returns None if path does not exist
def read(path):
    try:
        fd = os.open(path, os.O_RDONLY)
    except OSError:
        return None
    fcntl.flock(fd, fcntl.LOCK_EX)
    buffer = b''
    while True:
        chunk = os.read(fd, 32768)
        if chunk:
            buffer += chunk
        else:
            break
    fcntl.flock(fd, fcntl.LOCK_UN)
    os.close(fd)
    return buffer.decode('utf-8')

def write(path, content):
    fd = os.open(path, os.O_CREAT | os.O_WRONLY)
    fcntl.flock(fd, fcntl.LOCK_EX)
    os.write(fd, content.encode('utf-8'))
    fcntl.flock(fd, fcntl.LOCK_UN)
    os.close(fd)
