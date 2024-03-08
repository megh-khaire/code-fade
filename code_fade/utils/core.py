import hashlib


def hash_line(line):
    return hashlib.sha1(line.encode("utf-8")).hexdigest()
