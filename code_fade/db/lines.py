from code_fade.db.collections import Collections
import code_fade.db.core as db


def bulk_push_lines(data, chunk_size=100):
    db.bulk_push(Collections.LINES, data, chunk_size)


def delete_all_repo_lines(repo_name):
    db.delete_many(Collections.LINES, {"repo": repo_name})
